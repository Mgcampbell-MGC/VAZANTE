"""The forensic bridge — the subtraction ladder every book walks before routing and pricing (docs/01 Part 4.2;
docs/03 FINAL FORENSIC BRIDGE). Each step is a subtraction a buyer can recompute from the retained evidence.

seller-reported → canonical → existence-supported → title-supported → third-party-cash-supported → buyer-eligible
→ FIRM take-out. What falls out is zero / unresolved. No unverified asset enters LOCKED_PROCEEDS merely because
its inclusion is necessary for the transaction to pass.
"""
from __future__ import annotations

from dataclasses import dataclass

STAGES = (
    "seller_reported",
    "canonical",
    "existence_supported",
    "title_supported",
    "third_party_cash_supported",
    "buyer_eligible",
    "firm_takeout",
)


@dataclass(frozen=True)
class ForensicBridge:
    seller_reported: float
    canonical: float
    existence_supported: float
    title_supported: float
    third_party_cash_supported: float
    buyer_eligible: float
    firm_takeout: float
    unit: str = "BRL"

    def values(self) -> list[float]:
        return [getattr(self, s) for s in STAGES]

    @property
    def zero_unresolved(self) -> float:
        return self.seller_reported - self.firm_takeout

    def steps(self) -> list[tuple[str, str, float]]:
        """(from_stage, to_stage, amount subtracted) for each consecutive pair."""
        v = self.values()
        return [(STAGES[i], STAGES[i + 1], v[i] - v[i + 1]) for i in range(len(STAGES) - 1)]

    def problems(self) -> list[str]:
        out = []
        for s, x in zip(STAGES, self.values()):
            if x < 0:
                out.append(f"{s} is negative ({x})")
        for a, b, d in self.steps():
            if d < 0:
                out.append(f"{b} ({getattr(self, b)}) exceeds {a} ({getattr(self, a)}) — a stage can only subtract")
        return out

    def reconciled(self) -> bool:
        return not self.problems()

    def as_rows(self) -> list[dict]:
        rows = [{"stage": s, "face": x} for s, x in zip(STAGES, self.values())]
        rows.append({"stage": "zero_unresolved", "face": self.zero_unresolved})
        return rows
