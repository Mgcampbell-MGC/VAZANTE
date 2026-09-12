"""Cut a FIDC carteira into lots, each of which has one natural buyer.

The premise of the lot sale is that a broken multicedente book does not have a
buyer.  Its pieces do.  A buyer shown the whole book has to price the worst line
in it, so he bids the worst line, the seller refuses, and nothing trades.  That
is not a theory: across the twenty-five target funds the CVM informe reports
R$0 of ``alienacoes a terceiros`` for the whole period.  Not one real has been
sold to a third party.  The only money leaving these books is the cedente's
contractual ``recompra``.

The lot boundary is drawn where the *buyer's* model breaks, not where the
seller's book breaks.  Four boundaries are already tagged in the fund's own
monthly filing and need no tape to draw:

1. **Recourse.**  Read the CVM field names carefully, because they say the
   opposite of what they look like.  The split is *aquisicao substancial dos
   riscos* — who took the loss, not who granted recourse.  ``dircred_com_risco``
   (I.2.a) means the **fund** took the credit risk, so that paper is a **true
   sale with no recourse**.  ``dircred_sem_risco`` (I.2.b) means the risk stayed
   with the cedente, which is **where the recourse lives**.  The frozen mapping
   says so in terms; this module got it backwards on 12 September 2026 and the
   error reversed the buyer for three quarters of the book.  Paper with
   coobrigacao is credit risk on the originator; a true sale is credit risk on
   the debtor.  Two different products, two different buyers.
2. **Ageing.**  Tabela IV splits not-yet-due, 1-90, 90-180 and 180-plus.  Each
   bucket has its own pricing method and its own buyer class.
3. **Cedente status.**  A cedente in recuperacao judicial turns recourse paper
   into a claim in that recovery, which trades in a different market again.
4. **Size.**  A lot under a buyer's single-signature limit closes in days; a lot
   over it goes to a committee and closes in months.

What the informe cannot do is cross ageing against recourse — Tabela I and
Tabela IV are reported separately.  That cross is the first thing the tape has
to answer, and :func:`carve_fund` flags it rather than guessing.

Sizes here are *gross face by bucket*, never a price.  Nothing in this module
produces a price, an opinion of value or a recommendation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

__all__ = ["LOTS", "Carve", "LotSpec", "carve_fund", "carve_universe"]


@dataclass(frozen=True)
class LotSpec:
    """One lot: what it is, who its natural buyer is, why that buyer wants it."""

    key: str
    name_en: str
    name_pt: str
    risk: str
    buyer_type: str


#: The lot vocabulary.  Buyer names are deliberately absent: the named buyer
#: list is a separate, sourced artefact and does not belong in the carve.
LOTS: tuple[LotSpec, ...] = (
    LotSpec(
        key="A",
        name_en="Not yet due",
        name_pt="A vencer, sem parcela inadimplente",
        risk="sacado (debtor) credit risk, short remaining term",
        buyer_type="factoring houses, securitizadoras, FIDCs filling allocation, "
        "risco-sacado desks, and the original cedente buying its own paper back",
    ),
    LotSpec(
        key="B",
        name_en="Early overdue",
        name_pt="Vencidos ate 90 dias",
        risk="recent delinquency; often a cash-flow problem, not an insolvency",
        buyer_type="early-stage recovery buyers, the cedente under recourse, "
        "and the sacado himself settling his own payable (CC art. 381)",
    ),
    LotSpec(
        key="C",
        name_en="Mid overdue",
        name_pt="Vencidos de 90 a 180 dias",
        risk="migrating; too impaired for performing bids, too fresh for the NPL curve",
        buyer_type="specialist mid-stage buyers, or bundled into D",
    ),
    LotSpec(
        key="D",
        name_en="Deep NPL",
        name_pt="Vencidos acima de 180 dias",
        risk="classic corporate non-performing",
        buyer_type="corporate NPL funds — the one liquid, competitive bid in this market",
    ),
    LotSpec(
        key="E",
        name_en="Claims on failed cedentes",
        name_pt="Creditos contra cedentes em recuperacao judicial",
        risk="claim in a judicial recovery, or a warranty claim under CC art. 295",
        buyer_type="claims traders, litigation finance, and the debtor's own group",
    ),
    LotSpec(
        key="F",
        name_en="The vehicle",
        name_pt="As cotas do fundo",
        risk="the whole fund, bought as a security rather than as receivables",
        buyer_type="a house that wants the book without the assignment mechanics",
    ),
)


@dataclass
class Carve:
    """The lot plan for one fund, built from public data alone."""

    cnpj: str
    name: str
    carteira: float
    provision: float
    a_vencer: float
    a_vencer_impaired: float
    inadimplentes: float
    in_recovery: float
    buckets: dict[str, float]
    recourse_face: float
    true_sale_face: float
    recourse_share: float | None
    cedentes_named: int
    cedentes_in_rj: int
    cotistas: float | None
    flags: list[str] = field(default_factory=list)

    @property
    def gross_face(self) -> float:
        """Gross face from Tabela I, which is the identity that ties.

        Deliberately *not* the sum of :attr:`buckets`.  Bucket E (credits against
        companies in judicial recovery) is a status overlay that also appears in
        the age buckets, so summing them double-counts it; and the age ladder
        comes from Tabelas V and VI, which do not tie exactly to Tabela I.
        """
        return self.a_vencer + self.a_vencer_impaired + self.inadimplentes

    def as_row(self) -> dict[str, Any]:
        row: dict[str, Any] = {
            "cnpj": self.cnpj,
            "name": self.name,
            "carteira": self.carteira,
            "provision": self.provision,
            "gross_face": self.gross_face,
            "a_vencer": self.a_vencer,
            "a_vencer_impaired": self.a_vencer_impaired,
            "inadimplentes": self.inadimplentes,
            "in_recovery": self.in_recovery,
            "recourse_face": self.recourse_face,
            "true_sale_face": self.true_sale_face,
            "recourse_share": self.recourse_share,
            "cedentes_named": self.cedentes_named,
            "cedentes_in_rj": self.cedentes_in_rj,
            "cotistas": self.cotistas,
            "flags": "; ".join(self.flags),
        }
        row.update({f"lot_{k}": v for k, v in self.buckets.items()})
        return row


def _f(row: pd.Series, col: str) -> float:
    v = row.get(col)
    if v is None or pd.isna(v):
        return 0.0
    return float(v)


def carve_fund(row: pd.Series, *, single_signature_ceiling: float = 10_000_000.0) -> Carve:
    """Build the lot plan for one fund from its latest informe row.

    ``single_signature_ceiling`` is the size above which a lot stops being one
    person's decision and becomes a committee's.  It is a working assumption,
    not a measured number, and every lot above it is flagged.
    """
    # Tabela I — the identity that ties.
    a_vencer_gross = _f(row, "cred_a_vencer")
    a_vencer_impaired = _f(row, "cred_a_vencer_com_parcela_inad")
    inadimplentes = _f(row, "cred_inadimplentes")
    in_recovery = _f(row, "cred_empresa_recuperacao")
    # I.2.a.1/b.1 is already "a vencer E ADIMPLENTES"; the impaired block
    # I.2.a.2/b.2 is a separate item, not a subset.  Do not subtract it.
    a_vencer = a_vencer_gross

    # Tabelas V and VI — the age ladder.  A different source from Tabela I, so it
    # does not tie exactly; the gap is flagged below rather than reconciled away.
    inad_total = _f(row, "inad_total")
    inad_90 = _f(row, "inad_90_mais")
    inad_180 = _f(row, "inad_180_mais")

    buckets = {
        "A": a_vencer,
        "A2": a_vencer_impaired,  # not yet due, but already missing an instalment
        "B": max(inad_total - inad_90, 0.0),
        "C": max(inad_90 - inad_180, 0.0),
        "D": inad_180,
        "E": in_recovery,  # overlay, not a partition — also counted in B/C/D
    }

    # Do not swap these.  com_risco = the fund took the risk = true sale.
    # sem_risco = risk stayed with the cedente = the paper that carries recourse.
    true_sale = _f(row, "dircred_com_risco")
    recourse = _f(row, "dircred_sem_risco")
    share = recourse / (recourse + true_sale) if (recourse + true_sale) > 0 else None

    flags: list[str] = []
    if share is None:
        flags.append("recourse split not reported — ask the tape")
    flags.append("ageing is not crossed against recourse in the informe — first tape question")

    if buckets["A"] > 0 and _f(row, "pdd") > 0 and _f(row, "carteira") > 0:
        pdd_share = _f(row, "pdd") / _f(row, "carteira")
        if pdd_share > 0.50 and buckets["A"] > buckets["D"]:
            flags.append(
                f"provision {pdd_share:.0%} of carteira while the largest bucket is not yet due — "
                "either over-provisioned or about to migrate; the tape decides"
            )

    big = [k for k, v in buckets.items() if v > single_signature_ceiling]
    if big:
        flags.append("lots above one signature: " + ", ".join(sorted(big)))

    n_rj = int(_f(row, "n_rj"))
    if n_rj and in_recovery == 0:
        flags.append(
            f"{n_rj} cedente(s) in recuperacao judicial but no credit reported against "
            "companies in recovery — the claim may sit unmarked"
        )

    cot = row.get("cotistas")
    gap = inad_total - inadimplentes
    if inadimplentes > 0 and abs(gap) / inadimplentes > 0.02:
        flags.append(
            f"age ladder and Tabela I disagree on the overdue block by R${gap / 1e6:,.1f}m "
            f"({gap / inadimplentes:+.0%}) — Tabela I is the one that ties"
        )

    return Carve(
        cnpj=str(row.get("CNPJ_FUNDO_CLASSE", "")),
        name=str(row.get("DENOM_SOCIAL", "")),
        carteira=_f(row, "carteira"),
        provision=_f(row, "pdd"),
        a_vencer=a_vencer,
        a_vencer_impaired=a_vencer_impaired,
        inadimplentes=inadimplentes,
        in_recovery=in_recovery,
        buckets=buckets,
        recourse_face=recourse,
        true_sale_face=true_sale,
        recourse_share=share,
        cedentes_named=int(_f(row, "n_ced")),
        cedentes_in_rj=n_rj,
        cotistas=None if cot is None or pd.isna(cot) else float(cot),
        flags=flags,
    )


def carve_universe(df: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
    """Carve every fund in ``df`` and return one row per fund."""
    return pd.DataFrame([carve_fund(r, **kwargs).as_row() for _, r in df.iterrows()])
