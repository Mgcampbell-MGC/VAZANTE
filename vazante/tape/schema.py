"""Map a seller's columns onto ours, without asking the seller to change anything.

Sellers export from whatever system they run, in Portuguese, with inconsistent accents, abbreviations and
spacing. Refusing a file because a column is called "vlr_nominal" instead of "valor_face" costs a week of
calendar for no reason. This scores every incoming column against a synonym list and reports what it could not
place, so a human resolves the handful that matter instead of the whole file.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# Canonical field -> the spellings sellers actually use. Order does not matter; matching is by score.
SYNONYMS: dict[str, list[str]] = {
    "position_id": ["id", "identificador", "codigo", "cod titulo", "num titulo", "numero titulo", "id operacao",
                    "contrato", "num documento", "documento", "titulo"],
    "sacado_cnpj": ["cnpj sacado", "cpf cnpj sacado", "documento sacado", "cnpj devedor", "sacado cnpj",
                    "cnpj do sacado", "doc sacado", "cnpj cpf sacado", "devedor cnpj"],
    "sacado_nome": ["sacado", "nome sacado", "razao social sacado", "devedor", "nome devedor", "cliente"],
    "cedente_cnpj": ["cnpj cedente", "cpf cnpj cedente", "documento cedente", "cedente cnpj", "cnpj do cedente",
                     "doc cedente", "cnpj cpf cedente", "originador cnpj"],
    "cedente_nome": ["cedente", "nome cedente", "razao social cedente", "originador", "nome originador"],
    "face": ["valor face", "valor nominal", "vlr face", "vlr nominal", "face", "valor titulo", "valor bruto",
             "valor original", "vl face", "valor presente bruto", "nominal"],
    "book_value": ["valor contabil", "vlr contabil", "valor presente", "valor liquido", "vl contabil",
                   "valor provisionado", "valor atual", "saldo devedor", "saldo"],
    "provision": ["provisao", "pdd", "provisionamento", "valor provisao", "perda esperada", "reducao recuperavel"],
    "issue_date": ["data emissao", "dt emissao", "emissao", "data de emissao", "dt emiss", "data titulo"],
    "due_date": ["data vencimento", "dt vencimento", "vencimento", "data de vencimento", "dt venc", "venc"],
    "assignment_date": ["data cessao", "dt cessao", "cessao", "data aquisicao", "dt aquisicao", "data compra",
                        "data de cessao"],
    "payment_date": ["data pagamento", "dt pagamento", "data liquidacao", "dt liquidacao", "data baixa",
                     "dt baixa", "data recebimento"],
    "paid_amount": ["valor pago", "vlr pago", "valor recebido", "valor liquidado", "vl pago", "montante pago"],
    "status": ["situacao", "status", "situacao titulo", "estado", "situacao do titulo", "condicao"],
    "nfe_key": ["chave nfe", "chave acesso", "chave de acesso", "chave nf e", "nfe", "chave", "chave danfe",
                "chave de acesso nfe"],
    "doc_number": ["numero duplicata", "num duplicata", "duplicata", "numero documento", "num doc", "nota fiscal",
                   "numero nf", "num nf", "nf"],
    "doc_series": ["serie", "serie documento", "serie nf", "serie duplicata"],
    "recourse_flag": ["coobrigacao", "com coobrigacao", "coobrigado", "recompra", "direito regresso", "regresso",
                      "garantia cedente", "solidario"],
    "days_late": ["dias atraso", "atraso", "dias em atraso", "dpd", "dias vencido"],
    "protest_flag": ["protesto", "protestado", "em protesto", "cartorio"],
    "legal_flag": ["acao judicial", "judicial", "em acao", "juridico", "cobranca judicial", "processo"],
}

# Canonical fields the tape cannot be worked without.
TIER1 = ["sacado_cnpj", "cedente_cnpj", "face", "due_date"]


def normalize(s: str) -> str:
    """Lowercase, strip accents, collapse separators. 'Vlr. Nominal (R$)' -> 'vlr nominal r'."""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _score(candidate: str, synonym: str) -> float:
    """How well one incoming column name matches one synonym. 1.0 is exact."""
    if candidate == synonym:
        return 1.0
    cw, sw = set(candidate.split()), set(synonym.split())
    if not cw or not sw:
        return 0.0
    if sw <= cw:                       # every synonym word present, e.g. 'cnpj do sacado' vs 'cnpj sacado'
        return 0.9 - 0.01 * (len(cw) - len(sw))
    overlap = len(cw & sw) / len(sw)
    if candidate.startswith(synonym) or synonym.startswith(candidate):
        return max(overlap, 0.75)
    return overlap * 0.8


@dataclass
class Mapping:
    """The result of mapping one tape's columns."""

    resolved: dict[str, str] = field(default_factory=dict)      # canonical -> the seller's column name
    scores: dict[str, float] = field(default_factory=dict)
    unmapped: list[str] = field(default_factory=list)           # seller columns we could not place
    missing_tier1: list[str] = field(default_factory=list)
    ambiguous: dict[str, list[str]] = field(default_factory=dict)

    @property
    def workable(self) -> bool:
        return not self.missing_tier1

    def report(self) -> str:
        lines = [f"mapped {len(self.resolved)} of {len(SYNONYMS)} canonical fields"]
        for canon, col in sorted(self.resolved.items()):
            lines.append(f"  {canon:18s} <- {col!r}  (confidence {self.scores.get(canon, 0):.2f})")
        if self.ambiguous:
            lines.append("AMBIGUOUS, a human should confirm:")
            for canon, cands in self.ambiguous.items():
                lines.append(f"  {canon:18s} could be any of {cands}")
        if self.unmapped:
            lines.append(f"UNMAPPED seller columns ({len(self.unmapped)}): {self.unmapped[:12]}")
        if self.missing_tier1:
            lines.append(f"BLOCKING - tape cannot be worked without: {self.missing_tier1}")
        return "\n".join(lines)


def map_columns(columns: list[str], threshold: float = 0.62) -> Mapping:
    """Best-scoring assignment of incoming columns to canonical fields, each column used at most once."""
    norm = {c: normalize(c) for c in columns}
    pairs = []
    for canon, syns in SYNONYMS.items():
        for col, n in norm.items():
            best = max((_score(n, normalize(s)) for s in syns), default=0.0)
            if best >= threshold:
                pairs.append((best, canon, col))
    pairs.sort(reverse=True, key=lambda p: p[0])

    m = Mapping()
    used_cols: set[str] = set()
    for score, canon, col in pairs:
        if canon in m.resolved or col in used_cols:
            if canon in m.resolved and score >= m.scores[canon] - 0.05 and col not in used_cols:
                m.ambiguous.setdefault(canon, [m.resolved[canon]]).append(col)
            continue
        m.resolved[canon] = col
        m.scores[canon] = round(score, 3)
        used_cols.add(col)
    m.unmapped = [c for c in columns if c not in used_cols]
    m.missing_tier1 = [f for f in TIER1 if f not in m.resolved]
    return m
