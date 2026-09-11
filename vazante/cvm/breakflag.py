"""BREAK-FLAG — the conjunction rule (business case Part 2.4).

Fires when at least three of four primary conditions hold in the same month for two consecutive months:
  A  recompra intensity > 3% of carteira per month, or > 2× the fund's own trailing-12 median
  B  churn-to-default migration < 0.35
  C  PDD ÷ 90+ vencidos < 0.60
  D  senior-quota 12-month return stdev < 0.15 pp while the 180+ bucket grew > 50%
Nine secondary signals confirm and never trigger alone: alienações ao cedente > alienações a terceiros; recompra
Valor ≈ Valor Contábil ten months in twelve; pré-pagamento > 15% of liquidations; RESG_SOLIC outstanding two months;
late, restated or omitted informe; counterparty changes; top-25 churn outside 20–70%; auditor ressalva.
Two dates fall out of the series — t_peak (max recompra) and t_stop (intensity < 25% of trailing peak, and stays) —
and partition the book into V1 pre-break residue, V2 churn zone, V3 post-break cohort.

Every threshold is ASSUMPTION (config/thresholds.yaml) until fitted on the labelled set — Master, Reag, Trustee and
Banvox lineage funds whose break dates are known from the BCB decrees (BACKLOG #4). All of it waits on the frozen
mapping (BACKLOG #1).
"""
from __future__ import annotations

from dataclasses import dataclass, fields

import pandas as pd

from vazante.config import thresholds
from vazante.cvm.schema import load_mapping


@dataclass(frozen=True)
class BreakFlagParams:
    recompra_intensity_max: float
    recompra_vs_trailing_median: float
    churn_to_default_min: float
    pdd_coverage_min: float
    senior_return_stdev_max: float
    bucket_180_growth_min: float
    primary_conditions_required: int
    consecutive_months: int
    t_stop_fraction_of_peak: float

    @classmethod
    def from_config(cls) -> BreakFlagParams:
        t = thresholds()["breakflag"]
        return cls(**{f.name: t[f.name] for f in fields(cls)})


def monthly_indicators(history: pd.DataFrame) -> pd.DataFrame:
    """24-month fund history → indicator panel (primaries A–D, secondaries), one row per month."""
    load_mapping()  # MappingNotFrozen until BACKLOG #1
    raise NotImplementedError("indicator panel: build after the mapping freeze (docs/BACKLOG.md #1)")


def break_flag(indicators: pd.DataFrame, params: BreakFlagParams | None = None) -> pd.Series:
    """Boolean per month: >= N of 4 primaries hold this month and the previous one."""
    raise NotImplementedError("conjunction rule: build after the mapping freeze; fit thresholds on the labelled set (BACKLOG #4)")


def break_dates(indicators: pd.DataFrame, params: BreakFlagParams | None = None) -> tuple[str | None, str | None]:
    """(t_peak, t_stop) as 'YYYYMM', or None where the series does not show them."""
    raise NotImplementedError
