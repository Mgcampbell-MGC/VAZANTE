"""Machine-readable buy box (docs/02 Part 4). Two boxes per buyer at all times, stated and observed; the observed box
dominates from deal 3 and the buyer never sees it. Only pricing lines with status FIRM enter locked proceeds — that
single rule is what stops a grid from being mistaken for a contract.
"""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, model_validator

from vazante.oracle.states import Confidence, PriceStatus

BOXES_DIR = Path(__file__).resolve().parent / "boxes"


class Role(str, Enum):
    PREMIUM = "PREMIUM"
    CLAIMS = "CLAIMS"
    RESIDUAL = "RESIDUAL"


class BoxType(str, Enum):
    stated = "stated"
    observed = "observed"


class HardFilter(BaseModel):
    action: Literal["reject", "manual_review", "accept"]
    confidence: Confidence


class AssetType(BaseModel):
    accept: bool | Literal["manual_review"]
    confidence: Confidence


class PricingRule(BaseModel):
    cond: dict[str, Any]
    price_per_face: float | None = None
    uplift: float | None = None
    status: PriceStatus
    confidence: Confidence

    @model_validator(mode="after")
    def _one_of(self) -> PricingRule:
        if (self.price_per_face is None) == (self.uplift is None):
            raise ValueError("a pricing rule carries exactly one of price_per_face or uplift")
        return self


class Capacity(BaseModel):
    face_per_month: float
    price_per_month: float
    carry_forward_months: int = 0


class Execution(BaseModel):
    days_to_indicative: int | None = None
    days_to_firm: int | None = None
    quote_validity_bd: int | None = None
    settlement: str | None = None


class Retrade(BaseModel):
    permitted: list[str] = Field(default_factory=list)
    cap_pct_of_lot_price: float
    confidence: Confidence


class BuyBox(BaseModel):
    buyer: str
    role: Role
    box_version: str
    box_type: BoxType
    source_events: list[dict[str, Any]] = Field(default_factory=list)
    human_checked_by: str | None = None
    hard_filters: dict[str, HardFilter] = Field(default_factory=dict)
    asset_types: dict[str, AssetType] = Field(default_factory=dict)
    dpd: dict[str, Any] = Field(default_factory=dict)
    pool: dict[str, Any] = Field(default_factory=dict)
    pricing: list[PricingRule] = Field(default_factory=list)
    capacity: Capacity
    execution: Execution = Field(default_factory=Execution)
    retrade: Retrade
    locked_proceeds_rule: str = "only status: FIRM enters the 1.20x numerator"

    def firm_lines(self) -> list[PricingRule]:
        return [p for p in self.pricing if p.status == PriceStatus.FIRM]

    def rejects(self) -> list[str]:
        return [k for k, v in self.hard_filters.items() if v.action == "reject"]


def load_box(path: Path) -> BuyBox:
    with open(path, encoding="utf-8") as f:
        return BuyBox.model_validate(yaml.safe_load(f))


def load_all_boxes(directory: Path = BOXES_DIR) -> list[BuyBox]:
    return [load_box(p) for p in sorted(directory.glob("*.yaml"))]
