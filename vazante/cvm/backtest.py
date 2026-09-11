"""Backtest the break rule against funds we know broke.

The label is exogenous and comes from the filing record itself: a class that stops filing the informe while it
still carried material PL has gone dark, and going dark is the observable end state of the break the business
case describes. Classes still filing at the last complete month are the control.

This is not a fraud label and must never be reported as one. A fund can stop filing because it wound down
normally, was merged, or changed its CNPJ. The test is therefore comparative: does the rule fire more often, and
earlier, before a dark event than in a control window of the same length? If it does not, the detection edge is
a story rather than a measurement, and the thresholds in config/thresholds.yaml need refitting or the rule needs
rewriting.
"""
from __future__ import annotations

import pandas as pd

KEY = "CNPJ_FUNDO_CLASSE"
PRIMARIES = ["A_recompra", "B_churn", "C_coverage", "D_smooth"]


def month_index(months: list[str]) -> dict[str, int]:
    return {m: i for i, m in enumerate(sorted(months))}


def label_events(ind: pd.DataFrame, last_complete: str, min_pl: float = 1e6,
                 dark_gap_months: int = 2) -> pd.DataFrame:
    """One row per class: last filing month, whether it went dark, and its PL at that point.

    `dark_gap_months` guards against counting a merely late filer as dark: a class counts as dark only if its
    last filing is at least that many complete months before `last_complete`.
    """
    ind = ind[ind.month <= last_complete]
    idx = month_index(sorted(ind.month.unique()))
    last = (ind.sort_values("month").groupby(KEY)
            .agg(last_month=("month", "max"), first_month=("month", "min"),
                 n_months=("month", "nunique"), name=("DENOM_SOCIAL", "last"),
                 admin=("administrador_nome", "last"), pl_last=("pl", "last"),
                 carteira_last=("carteira", "last")))
    horizon = idx[last_complete]
    last["last_idx"] = last.last_month.map(idx)
    last["months_before_end"] = horizon - last.last_idx
    last["went_dark"] = (last.months_before_end >= dark_gap_months) & (last.pl_last.fillna(0) > min_pl)
    return last.reset_index()


def rule_fired(ind: pd.DataFrame, required: int = 3, consecutive: int = 2) -> pd.Series:
    """Boolean per row: at least `required` primaries hold this month and the previous `consecutive-1` months."""
    d = ind.sort_values([KEY, "month"])
    hit = (d["n_primary"] >= required)
    out = hit.copy()
    for k in range(1, consecutive):
        out &= d.groupby(KEY, sort=False)["n_primary"].shift(k).ge(required).fillna(False)
    return out


def evaluate(ind: pd.DataFrame, events: pd.DataFrame, last_complete: str,
             lookback: int = 12, required: int = 3, consecutive: int = 2) -> dict:
    """Hit rate on dark classes vs control, plus lead time in months for the classes it caught."""
    d = ind[ind.month <= last_complete].sort_values([KEY, "month"]).copy()
    d["fired"] = rule_fired(d, required=required, consecutive=consecutive).values
    idx = month_index(sorted(d.month.unique()))
    d["midx"] = d.month.map(idx)
    ev = events.set_index(KEY)
    d = d.join(ev[["went_dark", "last_idx"]], on=KEY)
    d["rel"] = d.midx - d.last_idx                      # 0 at the last filing, negative before it
    window = d[(d.rel <= 0) & (d.rel >= -lookback)]

    def stats(sub: pd.DataFrame) -> dict:
        per = sub.groupby(KEY)["fired"].max()
        lead = (sub[sub.fired].groupby(KEY)["rel"].min().abs())
        return {"classes": int(per.shape[0]), "caught": int(per.sum()),
                "hit_rate": float(per.mean()) if len(per) else float("nan"),
                "median_lead_months": float(lead.median()) if len(lead) else float("nan")}

    return {"dark": stats(window[window.went_dark]), "control": stats(window[~window.went_dark]),
            "params": {"required": required, "consecutive": consecutive, "lookback": lookback}}
