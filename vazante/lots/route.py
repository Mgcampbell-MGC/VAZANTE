"""Route a house's lots to the buyers who can actually take them.

The point of the carve is that a buyer shown one risk prices it with the model he
already has.  This module closes that loop: given what a house actually holds, it
names the firms whose stated appetite covers those lots, and rejects the ones
whose cheque floor the lot cannot reach.

Two filters do the work, and the second is the one people forget.

**Appetite.**  A buyer takes certain lots and underwrites either the cedente (on
recourse paper) or the sacado (on a true sale).  A firm that underwrites
originators has no way to price a true-sale block and will not bid on it.

**The cheque, not the face.**  Every serious buyer has a size below which he does
not open a file, and it is denominated in what he *pays*, not in face value.  A
R$10m lot at five centavos is a R$500k cheque, which is below every floor in the
registry.  The same R$10m of performing paper is a multi-million cheque and clears
most of them.  So the estimated price band, not the lot size, decides who can bid.

Bands are research estimates carried in :data:`BANDS`, tagged MODEL.  They exist
to route, never to quote: nothing here is a price, and no number from this module
goes to a seller.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

__all__ = ["BANDS", "Buyer", "Match", "load_registry", "route"]

REGISTRY = Path(__file__).resolve().parents[2] / "config" / "buyer_registry.yaml"

#: Low and high price per unit of face, by lot.  MODEL — from the lot-by-lot buyer
#: research, used only to size a cheque so the floor test means something.
BANDS: dict[str, tuple[float, float]] = {
    "A": (0.55, 0.75),
    "A2": (0.20, 0.40),
    "B": (0.20, 0.40),
    "C": (0.06, 0.12),
    "D": (0.03, 0.08),
    "E": (0.03, 0.09),
}


@dataclass(frozen=True)
class Buyer:
    name: str
    lots: tuple[str, ...]
    risk: str
    ticket_floor_brl: float
    speed_days: int
    signs: str
    tag: str
    note: str = ""
    ticket_ceiling_brl: float | None = None

    def takes(self, lot: str, *, recourse_share: float | None) -> bool:
        """Whether this buyer's appetite covers ``lot`` given the house's mix."""
        if lot not in self.lots:
            return False
        if self.risk == "either" or recourse_share is None:
            return True
        # A house that is overwhelmingly one kind of paper cannot feed a buyer who
        # only underwrites the other kind.
        if self.risk == "cedente":
            return recourse_share >= 0.25
        return recourse_share <= 0.75


@dataclass(frozen=True)
class Match:
    buyer: Buyer
    lots: tuple[str, ...]
    face: float
    cheque_low: float
    cheque_high: float

    @property
    def clears_floor(self) -> bool:
        return self.cheque_high >= self.buyer.ticket_floor_brl


def load_registry(path: Path | str = REGISTRY) -> list[Buyer]:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return [
        Buyer(
            name=b["name"],
            lots=tuple(b["lots"]),
            risk=b["risk"],
            ticket_floor_brl=float(b.get("ticket_floor_brl", 0)),
            ticket_ceiling_brl=(
                float(b["ticket_ceiling_brl"]) if b.get("ticket_ceiling_brl") else None
            ),
            speed_days=int(b["speed_days"]),
            signs=b["signs"],
            tag=b["tag"],
            note=(b.get("note") or "").strip(),
        )
        for b in raw["buyers"]
    ]


def route(
    lot_face: dict[str, float],
    *,
    recourse_share: float | None,
    registry: list[Buyer] | None = None,
    include_below_floor: bool = False,
) -> list[Match]:
    """Name the buyers who can take these lots, fastest to a firm bid first.

    ``lot_face`` maps lot key to gross face.  A buyer is matched on every lot his
    appetite covers; the cheque is the sum of those lots at the research band, and
    a buyer whose floor that cheque cannot reach is dropped unless
    ``include_below_floor`` is set.
    """
    buyers = registry if registry is not None else load_registry()
    out: list[Match] = []
    for b in buyers:
        lots = tuple(
            k for k, v in lot_face.items() if v > 0 and b.takes(k, recourse_share=recourse_share)
        )
        if not lots:
            continue
        face = sum(lot_face[k] for k in lots)
        lo = sum(lot_face[k] * BANDS.get(k, (0.0, 0.0))[0] for k in lots)
        hi = sum(lot_face[k] * BANDS.get(k, (0.0, 0.0))[1] for k in lots)
        m = Match(buyer=b, lots=lots, face=face, cheque_low=lo, cheque_high=hi)
        if m.clears_floor or include_below_floor:
            out.append(m)
    return sorted(out, key=lambda m: (m.buyer.speed_days, -m.cheque_high))
