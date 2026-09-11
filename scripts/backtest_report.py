"""Score the break rule against the provision blow-up event and print the per-indicator discrimination table.

The event is a class whose provision crosses 25% of the carteira and stays there three months. Indicators are
measured in the twelve months before it, against a control window of the same length on classes that never
reach it. Everything printed here is reproducible from data/raw.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from vazante.config import DERIVED_DIR
from vazante.cvm.backtest import evaluate, label_events

KEY = "CNPJ_FUNDO_CLASSE"
LAST = "202607"
TESTS = [
    ("pdd_share_carteira", ">", 0.10, "-"),
    ("inad_180_share", ">", 0.05, "-"),
    ("churn_intensity", ">", 0.05, "-"),
    ("bucket_180_growth_12m", ">", 0.50, "D"),
    ("recompra_intensity", ">", 0.03, "A"),
    ("pdd_coverage_90", "<", 0.60, "C"),
    ("churn_to_default", "<", 0.35, "B"),
    ("senior_return_stdev_12m", "<", 0.0015, "D"),
    ("prepay_share", ">", 0.15, "-"),
    ("alienacao_cedente_over_terceiros", ">", 1.0, "-"),
]


def windows(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    d = d[d.month <= LAST].sort_values([KEY, "month"]).copy()
    idx = {m: i for i, m in enumerate(sorted(d.month.unique()))}
    d["midx"] = d.month.map(idx)
    d["pdd_hi"] = d.pdd_share_carteira > 0.25
    d["pdd_hi_3m"] = d.groupby(KEY)["pdd_hi"].transform(
        lambda s: s.rolling(3, min_periods=3).min().astype(float)) == 1
    first = d[d.pdd_hi_3m].groupby(KEY)["midx"].min().rename("event_idx")
    d = d.join(first, on=KEY)
    d["k"] = d.event_idx - d.midx
    horizon = idx[LAST]
    pre = d[(d.k >= 1) & (d.k <= 12)]
    ctrl = d[d.event_idx.isna() & (d.midx >= 12) & (d.midx <= horizon - 12)]
    return d, pre, ctrl


def main() -> None:
    d = pd.read_parquet(DERIVED_DIR / "indicators.parquet")
    full, pre, ctrl = windows(d)
    n_event = full.loc[full.event_idx.notna(), KEY].nunique()
    print(f"classes {full[KEY].nunique():,} | reach provision > 25% for 3 months: {n_event:,}")
    print(f"pre-event rows {len(pre):,} | control rows {len(ctrl):,}\n")
    print(f"{'indicator':34s} {'prim':>5s} {'computable':>11s} {'pre':>8s} {'control':>8s} {'lift':>6s}  verdict")
    for col, op, thr, prim in TESTS:
        fp = (pre[col] > thr).mean() if op == ">" else (pre[col] < thr).mean()
        fc = (ctrl[col] > thr).mean() if op == ">" else (ctrl[col] < thr).mean()
        lift = fp / fc if fc else np.nan
        cov = pre[col].notna().mean()
        if cov < 0.05 or not np.isfinite(lift):
            verdict = "not reported — unusable on this population"
        elif lift < 0.95:
            verdict = "INVERTED"
        elif lift < 1.5:
            verdict = "near-useless"
        elif lift < 3:
            verdict = "works"
        else:
            verdict = "strong"
        print(f"{col:34s} {prim:>5s} {cov:10.1%} {fp:8.1%} {fc:8.1%} {lift:6.2f}  {verdict}")

    print("\n=== conjunction rule as written in the business case, against the dark-filing label ===")
    ev = label_events(d, LAST)
    for req, cons in ((3, 2), (2, 1)):
        r = evaluate(d, ev, LAST, required=req, consecutive=cons)
        print(f"  {req} of 4 x {cons}m: dark {r['dark']['caught']}/{r['dark']['classes']} "
              f"({r['dark']['hit_rate']:.1%})  control {r['control']['caught']}/{r['control']['classes']} "
              f"({r['control']['hit_rate']:.1%})")


if __name__ == "__main__":
    main()
