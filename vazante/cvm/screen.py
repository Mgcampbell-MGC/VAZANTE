"""The screen that finds Deal 1 (business case Part 3.6), with the corrections the first run forced.

The business case's five filters, as written, produced 18 names of which most were captive originator books.
Three corrections were measured on the 2026-07 population and are applied here:

  1. B2B PAPER ONLY. The CVM's "comercial" bucket (II.c) includes VAREJO (II.c.2), which is retail consumer
     credit, and ARRENDAMENTO (II.c.3). 35% of the comercial face in the first result set was varejo. The desk
     buys business-to-business duplicata paper, so the share is computed from INDUSTRIAL (II.a) plus
     COMERCIAL-proper (II.c.1) only, and a fund with material varejo is excluded outright.

  2. THE PROVISION MUST BE AN EVENT, NOT A LEVEL. Several strategies carry a permanently high provision by
     design; a consumer or microcredit book at 30% for three years is a business model, not distress. The test
     is therefore a rise of at least 10 percentage points over twelve months, not a level.

  3. CAPTIVE ORIGINATOR BOOKS ARE EXCLUDED WHERE VISIBLE. A single sponsor originating the whole book has no
     heterogeneity to decompose and no third party to resell to. Where the administrador names cedentes, a
     single cedente above 50% of PL is the tell.

KNOWN REMAINING WEAKNESS, and it is the important one. Correction 3 only works where cedentes are named, and
naming is a reporting habit rather than a property of the book: it ranges from 0% of classes at Trustee, Banvox
and Merito to 95% at Catálise, with 44% of the population naming anyone at all. Where the administrador names
nobody, a captive book is invisible to this screen and only the fund's own name gives it away. Treat every
survivor whose name contains a corporate name as captive until a human says otherwise.

Filter (i) of the business case, the class closed for redemptions for more than five business days, still needs
Fundos.NET and is not implemented. It is the best willingness proxy available and its absence is why the output
is a research list, not a calling list.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from vazante.config import DERIVED_DIR, thresholds
from vazante.cvm.panel import load_registro, snapshot
from vazante.cvm.schema import read_table

KEY = "CNPJ_FUNDO_CLASSE"
CEDENTE_CNPJ_COLS = [f"TAB_I2A12_CPF_CNPJ_CEDENTE_{i}" for i in range(1, 10)] + \
                    [f"TAB_I2B12_CPF_CNPJ_CEDENTE_{i}" for i in range(1, 10)]
CEDENTE_PCT_COLS = [f"TAB_I2A12_PR_CEDENTE_{i}" for i in range(1, 10)] + \
                   [f"TAB_I2B12_PR_CEDENTE_{i}" for i in range(1, 10)]


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.replace("", None), errors="coerce")


def _digits(s: pd.Series) -> pd.Series:
    return s.astype(str).str.replace(r"\D", "", regex=True)


def enrich(month: str = "202607") -> pd.DataFrame:
    """Panel indicators for one month, joined to the register and to the B2B / cedente / trajectory measures."""
    ind = pd.read_parquet(DERIVED_DIR / "indicators.parquet")
    cur = ind[ind.month == month].copy()

    reg = load_registro()
    cur["cnpj_digits"] = _digits(cur[KEY])
    cur = cur.merge(
        reg[["cnpj_digits", "Gestor", "CPF_CNPJ_Gestor", "Administrador", "CNPJ_Administrador", "Diretor",
             "Situacao_classe", "Situacao_fundo", "Tipo_Fundo", "Entidade_Investimento", "Forma_Condominio"]]
        .drop_duplicates("cnpj_digits"), on="cnpj_digits", how="left")

    zp = snapshot(month)
    t2 = read_table(zp, "II", month)
    tot = _num(t2.TAB_II_VL_CARTEIRA).replace(0, np.nan)
    seg = pd.DataFrame({
        KEY: t2[KEY],
        "b2b_share": (_num(t2.TAB_II_A_VL_INDUST) + _num(t2.TAB_II_C1_VL_COMERC)) / tot,
        "varejo_share": _num(t2.TAB_II_C2_VL_VAREJO) / tot,
        "servicos_share": _num(t2.TAB_II_D_VL_SERV) / tot,
    }).drop_duplicates(KEY)
    cur = cur.merge(seg, on=KEY, how="left")

    t1 = read_table(zp, "I", month)
    have_c = [c for c in CEDENTE_CNPJ_COLS if c in t1.columns]
    have_p = [c for c in CEDENTE_PCT_COLS if c in t1.columns]
    ced = pd.DataFrame({
        KEY: t1[KEY],
        "n_ced_named_gt10pct": t1[have_c].apply(
            lambda r: sum(str(v).strip() not in ("", "nan") for v in r), axis=1),
        "max_cedente_pct": t1[have_p].apply(
            lambda r: max([float(v) for v in r if str(v).strip() not in ("", "nan")] or [0.0]), axis=1),
    }).drop_duplicates(KEY)
    cur = cur.merge(ced, on=KEY, how="left")

    piv = ind.pivot_table(index=KEY, columns="month", values="pdd_share_carteira", aggfunc="last")
    months = sorted(ind.month.unique())
    i = months.index(month)
    prior = months[i - 12] if i >= 12 else None
    traj = pd.DataFrame({"pdd_now": piv.get(month)}).reset_index()
    traj["pdd_12m_ago"] = piv.get(prior).values if prior else np.nan
    traj["pdd_jump_12m"] = traj.pdd_now - traj.pdd_12m_ago
    return cur.merge(traj, on=KEY, how="left")


def apply_filters(cur: pd.DataFrame) -> pd.DataFrame:
    """Add the boolean gate columns. Thresholds come from config/thresholds.yaml."""
    t = thresholds()["screen"]
    cur = cur.copy()
    cur["g_fidc"] = cur.Tipo_Fundo.eq("FIDC")
    cur["g_loss_booked"] = cur.pdd_share_carteira >= t["pdd_share_of_carteira_min"]
    cur["g_b2b"] = cur.b2b_share >= t["industrial_plus_comercial_share_min"]
    cur["g_no_retail"] = cur.varejo_share.fillna(0) < 0.10
    cur["g_provision_is_event"] = cur.pdd_jump_12m >= 0.10
    cur["g_not_captive_visible"] = cur.max_cedente_pct.fillna(0) < 50
    cur["g_size"] = cur.carteira >= 60e6
    cur["g_gestor"] = cur.Gestor.notna() & (
        _digits(cur.CPF_CNPJ_Gestor.fillna("")) != _digits(cur.CNPJ_Administrador.fillna("~")))
    return cur


GATES = [
    ("g_fidc", "FIDC (register type)"),
    ("g_loss_booked", "loss already booked: provision >= 25% of carteira"),
    ("g_b2b", "business-to-business paper: industrial + comercial(c.1) >= 60%"),
    ("g_no_retail", "no material retail consumer credit: varejo < 10%"),
    ("g_provision_is_event", "the provision is an event: +10pp over 12 months"),
    ("g_not_captive_visible", "not visibly captive: no named cedente above 50% of PL"),
    ("g_size", "carteira >= R$60m"),
    ("g_gestor", "gestor present and distinct from the administrador"),
]


def run(month: str = "202607") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (all classes with gate columns, the survivors)."""
    cur = apply_filters(enrich(month))
    mask = pd.Series(True, index=cur.index)
    for col, _ in GATES:
        mask &= cur[col].fillna(False)
    return cur, cur[mask]
