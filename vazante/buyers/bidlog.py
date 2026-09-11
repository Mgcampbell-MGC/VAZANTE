"""Every bid is stored forever (docs/02 Part 4): buyer, deal, pool, Oracle attributes at quote, initial grid, indicative,
firm, settled, retrade amount and reason, rejection reason, committee exception, days to quote, days to settle.
The log is what turns the stated box into the observed box."""
from __future__ import annotations

import uuid
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from vazante.config import BIDS_DIR


class BidRecord(BaseModel):
    bid_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    buyer: str
    deal_id: str
    pool_id: str
    stage: Literal["indicative", "firm", "settled", "rejected", "retraded"]
    oracle_attributes: dict[str, Any] = Field(default_factory=dict)
    grid_price: float | None = None
    indicative_price: float | None = None
    firm_price: float | None = None
    settled_price: float | None = None
    retrade_amount: float | None = None
    retrade_reason: str | None = None
    rejection_reason: str | None = None
    committee_exception: str | None = None
    days_to_quote: int | None = None
    days_to_settle: int | None = None
    signatory: str | None = None
    expiry: date | None = None
    arras_pct: float | None = None
    source_document: str | None = None  # the letter / email / termo the number came from — a bid without a source is not a bid
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def append_bid(record: BidRecord, store: Path | None = None) -> Path:
    store = store or BIDS_DIR
    store.mkdir(parents=True, exist_ok=True)
    path = store / "bids.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(record.model_dump_json() + "\n")
    return path


def load_bids(store: Path | None = None) -> list[BidRecord]:
    store = store or BIDS_DIR
    path = store / "bids.jsonl"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [BidRecord.model_validate_json(line) for line in f if line.strip()]
