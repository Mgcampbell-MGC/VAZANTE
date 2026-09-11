"""Derived indicators on top of the panel: the four primary break conditions, the secondaries, and the
shape measures the screen filters on. One row per class per month, same key as the panel.

Every ratio here is defined once, in code, so the break rule and the screen cannot drift apart.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

KEY = "CNPJ_FUNDO_CLASSE"


def _safe_div(a: pd.Series, b: pd.Series) -> pd.Series:
    b = b.replace(0, np.nan)
    return a / b


def add_indicators(panel: pd.DataFrame) -> pd.DataFrame:
    """Add the ratios. Sorted by key and month; trailing windows are per key."""
    df = panel.sort_values([KEY, "month"]).copy()
    for c in ("pdd", "recompras", "substituicoes", "carteira", "pl", "inad_180_mais", "inad_90_mais",
              "inad_total", "a_vencer_total", "pagos_antecipadamente", "alienacoes_ao_cedente",
              "alienacoes_a_terceiros", "recompras_contabil", "resgates_solicitados",
              "carteira_segmento", "seg_industrial", "seg_comercial", "rentabilidade_mes_senior"):
        if c not in df.columns:
            df[c] = np.nan
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["pdd"] = df["pdd"].abs()

    g = df.groupby(KEY, sort=False)

    # A — recompra intensity: repurchases as a share of the carteira, and against the fund's own trailing median
    df["recompra_intensity"] = _safe_div(df["recompras"], df["carteira"])
    df["recompra_trailing_median"] = g["recompra_intensity"].transform(
        lambda s: s.shift(1).rolling(12, min_periods=6).median())
    df["recompra_vs_own_median"] = _safe_div(df["recompra_intensity"], df["recompra_trailing_median"])
    df["substituicao_intensity"] = _safe_div(df["substituicoes"], df["carteira"])
    df["churn_intensity"] = _safe_div(df["recompras"] + df["substituicoes"], df["carteira"])

    # B — churn-to-default: how much of the churn shows up as default. Low means defaults are being absorbed.
    df["churn_to_default"] = _safe_div(df["inad_total"], (df["recompras"] + df["substituicoes"]))

    # C — provision coverage of the aged book
    df["pdd_coverage_90"] = _safe_div(df["pdd"], df["inad_90_mais"])
    df["pdd_share_carteira"] = _safe_div(df["pdd"], df["carteira"])

    # D — a senior return too smooth to be real, while the far bucket grows
    df["senior_return_stdev_12m"] = g["rentabilidade_mes_senior"].transform(
        lambda s: s.rolling(12, min_periods=8).std())
    df["bucket_180_growth_12m"] = g["inad_180_mais"].transform(lambda s: _safe_div(s, s.shift(12)) - 1.0)
    df["inad_180_share"] = _safe_div(df["inad_180_mais"], df["carteira"])

    # secondaries
    df["alienacao_cedente_over_terceiros"] = _safe_div(df["alienacoes_ao_cedente"], df["alienacoes_a_terceiros"])
    df["recompra_at_book_value"] = (_safe_div(df["recompras"], df["recompras_contabil"]).sub(1).abs() < 0.01)
    df["prepay_share"] = _safe_div(df["pagos_antecipadamente"], df["carteira"])
    df["resg_solicitado_outstanding"] = df["resgates_solicitados"].fillna(0) > 0

    # shape, for the screen
    df["ind_com_share"] = _safe_div(df["seg_industrial"] + df["seg_comercial"], df["carteira_segmento"])
    df["n_cedentes_named"] = df.get("n_cedentes_com_risco", pd.Series(0, index=df.index)).fillna(0) + \
                             df.get("n_cedentes_sem_risco", pd.Series(0, index=df.index)).fillna(0)
    return df


def primary_conditions(df: pd.DataFrame, t: dict) -> pd.DataFrame:
    """The four primaries A-D of business case 2.4, as booleans."""
    out = pd.DataFrame(index=df.index)
    out["A_recompra"] = ((df["recompra_intensity"] > t["recompra_intensity_max"]) |
                         (df["recompra_vs_own_median"] > t["recompra_vs_trailing_median"])).fillna(False)
    out["B_churn"] = (df["churn_to_default"] < t["churn_to_default_min"]).fillna(False)
    out["C_coverage"] = (df["pdd_coverage_90"] < t["pdd_coverage_min"]).fillna(False)
    out["D_smooth"] = ((df["senior_return_stdev_12m"] < t["senior_return_stdev_max"]) &
                       (df["bucket_180_growth_12m"] > t["bucket_180_growth_min"])).fillna(False)
    out["n_primary"] = out[["A_recompra", "B_churn", "C_coverage", "D_smooth"]].sum(axis=1)
    return out
