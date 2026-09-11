"""Tier 0 — 100% offline structural checks, run before any paid or credentialed query (docs/03 — 100% STRUCTURAL SWEEP).

Implemented here: CPF and CNPJ check digits (CNPJ numeric and alphanumeric, IN RFB 2.229/2024 — the alphanumeric
CNPJ exists since July 2026); the NF-e 44-digit chave de acesso structure and check digit; the parse of the key's
embedded UF, issue month, emitter CNPJ, model, series, number and emission type.

Not yet: the sweep over a tape — duplicates (exact and fuzzy), impossible date sequences, same NF-e behind several
receivables, round-number and terminal-digit clustering, paid-before-assigned, unexplained replacements/recompras.
It needs the tape schema, and the tape schema needs Deal 0's first real tape. Never silently delete duplicates:
flag them and quantify affected face.

Open point: how the chave de acesso encodes an ALPHANUMERIC emitter CNPJ — confirm against the current SEFAZ Nota
Técnica before the first tape with issuers registered after July 2026.
"""
from __future__ import annotations

import re
from typing import Any

UF_CODES = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL", 28: "SE", 29: "BA",
    31: "MG", 32: "ES", 33: "RJ", 35: "SP",
    41: "PR", 42: "SC", 43: "RS",
    50: "MS", 51: "MT", 52: "GO", 53: "DF",
}
NFE_MODELS = {"55": "NF-e", "65": "NFC-e"}

_CNPJ_W1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_CNPJ_W2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def digits_only(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def cpf_normalize(cpf: str) -> str:
    return digits_only(cpf)


def cpf_valid(cpf: str) -> bool:
    d = cpf_normalize(cpf)
    if len(d) != 11 or len(set(d)) == 1:
        return False
    nums = [int(c) for c in d]

    def dv(slice_: list[int], start_weight: int) -> int:
        total = sum(n * w for n, w in zip(slice_, range(start_weight, 1, -1)))
        r = total % 11
        return 0 if r < 2 else 11 - r

    return dv(nums[:9], 10) == nums[9] and dv(nums[:10], 11) == nums[10]


def cnpj_normalize(cnpj: str) -> str:
    """Keep [0-9A-Z]; letters are legal in the twelve base positions since July 2026."""
    return re.sub(r"[^0-9A-Z]", "", (cnpj or "").upper())


def _cnpj_char_value(c: str) -> int:
    return ord(c) - 48  # '0'..'9' → 0..9, 'A'..'Z' → 17..42 (Receita's alphanumeric rule)


def cnpj_check_digits(base12: str) -> str:
    vals = [_cnpj_char_value(c) for c in base12]
    r1 = sum(v * w for v, w in zip(vals, _CNPJ_W1)) % 11
    d1 = 0 if r1 < 2 else 11 - r1
    r2 = sum(v * w for v, w in zip(vals + [d1], _CNPJ_W2)) % 11
    d2 = 0 if r2 < 2 else 11 - r2
    return f"{d1}{d2}"


def cnpj_valid(cnpj: str) -> bool:
    n = cnpj_normalize(cnpj)
    if len(n) != 14 or not n[12:].isdigit() or len(set(n)) == 1:
        return False
    if not re.fullmatch(r"[0-9A-Z]{12}", n[:12]):
        return False
    return cnpj_check_digits(n[:12]) == n[12:]


def cnpj_root(cnpj: str) -> str:
    """The raiz (first eight characters) — the corporate-group key used for CNAB payer identity."""
    return cnpj_normalize(cnpj)[:8]


def nfe_key_check_digit(first43: str) -> int:
    """Mod-11 over the first 43 digits, weights 2..9 cycling from the right."""
    if len(first43) != 43 or not first43.isdigit():
        raise ValueError("expected 43 digits")
    total, w = 0, 2
    for c in reversed(first43):
        total += int(c) * w
        w = 2 if w == 9 else w + 1
    r = total % 11
    return 0 if r < 2 else 11 - r


def nfe_key_valid(key: str) -> bool:
    k = digits_only(key)
    if len(k) != 44:
        return False
    try:
        return nfe_key_check_digit(k[:43]) == int(k[43])
    except ValueError:
        return False


def nfe_key_parse(key: str) -> dict[str, Any]:
    """cUF(2) AAMM(4) CNPJ(14) mod(2) série(3) nNF(9) tpEmis(1) cNF(8) cDV(1)."""
    k = digits_only(key)
    if len(k) != 44:
        raise ValueError("chave de acesso must have 44 digits")
    cuf = int(k[0:2])
    return {
        "chave": k,
        "cUF": cuf,
        "uf": UF_CODES.get(cuf),
        "aamm": k[2:6],
        "issue_year": 2000 + int(k[2:4]),
        "issue_month": int(k[4:6]),
        "cnpj_emitente": k[6:20],
        "cnpj_emitente_valid": cnpj_valid(k[6:20]),
        "modelo": k[20:22],
        "modelo_nome": NFE_MODELS.get(k[20:22]),
        "serie": int(k[22:25]),
        "nNF": int(k[25:34]),
        "tpEmis": int(k[34]),
        "cNF": k[35:43],
        "cDV": int(k[43]),
        "dv_ok": nfe_key_valid(k),
        "uf_ok": cuf in UF_CODES,
        "month_ok": 1 <= int(k[4:6]) <= 12,
    }


def structural_sweep(tape: Any) -> Any:
    """Tier 0 over a position-level tape. Needs the tape schema (Deal 0). Flags, never deletes."""
    raise NotImplementedError("structural sweep: build on Deal 0's first real tape (docs/BACKLOG.md)")
