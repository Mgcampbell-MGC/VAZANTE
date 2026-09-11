"""One-trade arithmetic on the reference book (docs/01 Part 7.1). Every number here is MODEL. Nothing here is a bid.

The 1.20× rule with tax inside the basis:
    L ÷ (bid + C + t·(L − bid − C)) = cover
    ⇒ bid = (L·(1/cover − t)) ÷ (1 − t) − C
Locked after-tax contribution = (L − bid − C)·(1 − t) = L·(1 − 1/cover) = L ÷ 6 at cover 1.20, in any tax regime.
Tax does not cut margin; it cuts the bid, and therefore the deal count.

Symbols: L = locked onward proceeds (FIRM only), C = non-purchase costs, t = tax rate on the spread, all in R$m.
"""
from __future__ import annotations

from dataclasses import dataclass

# Reference book, R$m (docs/01 Part 7.1) — MODEL
REFERENCE_L = 13.953          # 9.30¢ documented, 6.64¢ informe
REFERENCE_C = 0.578           # R$0.781m on deals 1–3 (×1.35)
REFERENCE_T1 = 0.371          # Lucro Real, spread as receita financeira
REFERENCE_MAX_BID = 9.679
REFERENCE_AFTER_TAX = 2.325
REFERENCE_BASIS = 11.627
COVER = 1.20

# Tax rate on the spread by characterisation. T1 and the FIDC wrapper are stated in the doc; T2 and T3 are
# inferido — the rates that reproduce the doc's R$9.49m and R$8.56m max bids.
TAX_RATES = {"T1_lucro_real": 0.371, "FIDC_NP_wrapper": 0.15, "T2_factoring_inferido": 0.40, "T3_adverse_gross_inferido": 0.517}


def max_bid(L: float, C: float, t: float, cover: float = COVER) -> float:
    """Maximum firm seller bid such that L covers the all-in basis (bid + C + tax) by `cover`."""
    return (L * (1.0 / cover - t)) / (1.0 - t) - C


def spread(bid: float, L: float, C: float) -> float:
    return L - bid - C


def tax(bid: float, L: float, C: float, t: float) -> float:
    return t * spread(bid, L, C)


def basis(bid: float, L: float, C: float, t: float) -> float:
    """All-in cash basis: bid + non-purchase costs + tax on the spread."""
    return bid + C + tax(bid, L, C, t)


def cover_ratio(bid: float, L: float, C: float, t: float) -> float:
    return L / basis(bid, L, C, t)


def after_tax_contribution(bid: float, L: float, C: float, t: float) -> float:
    return spread(bid, L, C) * (1.0 - t)


def payout_ratio(bid: float, C: float, L: float) -> float:
    """(bid + C) ÷ L — the '≈73¢ per R$1 of FIRM proceeds' ceiling as the doc's numbers imply it (inferido)."""
    return (bid + C) / L


def bid_at_gross_contribution(L: float, C: float, gross: float) -> float:
    """Bid that leaves a given pre-tax contribution; the doc's 'hurdle alone would allow R$11.87m' uses R$1.5m gross (inferido)."""
    return L - C - gross


@dataclass(frozen=True)
class Trade:
    L: float
    C: float
    t: float
    cover: float = COVER

    @property
    def max_bid(self) -> float:
        return max_bid(self.L, self.C, self.t, self.cover)

    @property
    def tax(self) -> float:
        return tax(self.max_bid, self.L, self.C, self.t)

    @property
    def basis(self) -> float:
        return basis(self.max_bid, self.L, self.C, self.t)

    @property
    def gross_contribution(self) -> float:
        return spread(self.max_bid, self.L, self.C)

    @property
    def after_tax_contribution(self) -> float:
        return after_tax_contribution(self.max_bid, self.L, self.C, self.t)

    @property
    def payout_ratio(self) -> float:
        return payout_ratio(self.max_bid, self.C, self.L)

    def as_dict(self) -> dict[str, float]:
        return {
            "L": self.L,
            "C": self.C,
            "t": self.t,
            "cover": self.cover,
            "max_bid": self.max_bid,
            "tax": self.tax,
            "basis": self.basis,
            "gross_contribution": self.gross_contribution,
            "after_tax_contribution": self.after_tax_contribution,
            "payout_ratio": self.payout_ratio,
        }


def reference_trade(t: float = REFERENCE_T1) -> Trade:
    return Trade(L=REFERENCE_L, C=REFERENCE_C, t=t)
