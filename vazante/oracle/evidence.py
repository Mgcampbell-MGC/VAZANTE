"""The pull() evidence wrapper (docs/03 — EVIDENCE WRAPPER).

Every external call goes through pull(). Each call stores: pull_id, deal, entity, provider, product, parameters,
credential identity, request and response timestamps, result state, the raw response (by SHA-256), the parser
version, parsed facts and the retry history. No material derived fact enters underwriting without a pull_id or an
explicit ASSUMPTION status. A technical failure is recorded as such and is never converted to NO_RECORD.
"""
from __future__ import annotations

import hashlib
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from vazante.config import EVIDENCE_DIR
from vazante.oracle.states import FAILURE_STATES, OracleResultState

Fetch = Callable[[], tuple[bytes, OracleResultState]]
Parser = Callable[[bytes], dict[str, Any]]


class Pull(BaseModel):
    pull_id: str
    deal_id: str | None = None
    entity_id: str | None = None
    provider: str
    product: str
    params: dict[str, Any] = Field(default_factory=dict)
    credential_identity: str | None = None
    requested_at: datetime
    responded_at: datetime | None = None
    status: OracleResultState
    raw_sha256: str | None = None
    raw_path: str | None = None
    raw_bytes: int = 0
    parser_version: str = "0"
    parsed: dict[str, Any] = Field(default_factory=dict)
    retries: list[dict[str, Any]] = Field(default_factory=list)
    error: str | None = None

    @property
    def failed(self) -> bool:
        return self.status in FAILURE_STATES


def _now() -> datetime:
    return datetime.now(UTC)


def _append(store: Path, record: Pull) -> None:
    store.mkdir(parents=True, exist_ok=True)
    with open(store / "pulls.jsonl", "a", encoding="utf-8") as f:
        f.write(record.model_dump_json() + "\n")


def pull(
    provider: str,
    product: str,
    params: dict[str, Any],
    fetch: Fetch,
    *,
    deal_id: str | None = None,
    entity_id: str | None = None,
    credential_identity: str | None = None,
    parser: Parser | None = None,
    parser_version: str = "0",
    store: Path | None = None,
    max_retries: int = 0,
) -> Pull:
    """Run `fetch` (returns raw bytes and the oracle result state), persist everything, return the record."""
    store = store or EVIDENCE_DIR
    record = Pull(
        pull_id=uuid.uuid4().hex,
        deal_id=deal_id,
        entity_id=entity_id,
        provider=provider,
        product=product,
        params=params,
        credential_identity=credential_identity,
        requested_at=_now(),
        status=OracleResultState.SOURCE_UNAVAILABLE,
        parser_version=parser_version,
    )
    attempt = 0
    while True:
        try:
            raw, status = fetch()
            break
        except Exception as exc:  # noqa: BLE001 — every failure is evidence
            record.retries.append({"attempt": attempt, "at": _now().isoformat(), "error": repr(exc)})
            if attempt >= max_retries:
                record.responded_at = _now()
                record.status = OracleResultState.SOURCE_UNAVAILABLE
                record.error = repr(exc)
                _append(store, record)
                return record
            attempt += 1
    record.responded_at = _now()
    record.status = status
    if raw:
        sha = hashlib.sha256(raw).hexdigest()
        raw_dir = store / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        path = raw_dir / f"{sha}.bin"
        if not path.exists():
            path.write_bytes(raw)
        record.raw_sha256 = sha
        record.raw_path = str(path.relative_to(store))
        record.raw_bytes = len(raw)
        if parser is not None and status not in FAILURE_STATES:
            try:
                record.parsed = parser(raw)
            except Exception as exc:  # noqa: BLE001
                record.status = OracleResultState.PENDING_HUMAN_REVIEW
                record.error = f"parser failed: {exc!r}"
    _append(store, record)
    return record


def load_pulls(store: Path | None = None) -> list[Pull]:
    store = store or EVIDENCE_DIR
    path = store / "pulls.jsonl"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [Pull.model_validate_json(line) for line in f if line.strip()]
