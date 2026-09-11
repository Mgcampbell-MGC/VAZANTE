"""Did the orphaned estates survive, and if so which filter kills them?

The question this answers: a fund whose administrador is liquidated keeps its own CNPJ and moves to a new
administrador. Grouping the current month by administrador NAME therefore counts only the funds that have not
moved yet, and undercounts the estate badly. This builds the cohort from every administrador a class has ever
had across the 44-month panel, plus Reag, which never appears as an administrador at all and shows up only as a
gestor in the live register.

Output: cohort size, how many filed the last complete month, how many already moved, which gate kills each
survivor, and what the cohort's carteira is actually invested in.

Usage: .venv/bin/python scripts/orphan_cohort.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from vazante.config import DERIVED_DIR
from vazante.cvm.panel import load_registro, snapshot
from vazante.cvm.schema import read_table
from vazante.cvm.screen import GATES, apply_filters, enrich

pd.set_option("display.width", 250)
KEY = "CNPJ_FUNDO_CLASSE"
MONTH = "202607"
# Houses whose administrador was put into liquidation, plus Reag, which was a gestora.
ADMIN_LINEAGES = {"TRUSTEE": "TRUSTEE", "BANVOX": "BANVOX", "MASTER": "MASTER S/A", "CBSF": "CBSF", "SEFER": "SEFER"}
GESTOR_LINEAGES = {"REAG": "REAG"}


def _digits(s: pd.Series) -> pd.Series:
    return s.astype(str).str.replace(r"\D", "", regex=True)


def build_cohort(ind: pd.DataFrame) -> pd.DataFrame:
    """Every class ever administered or managed by a liquidated-lineage house."""
    ind = ind.copy()
    ind["adm_u"] = ind.administrador_nome.astype(str).str.upper()
    coh: dict[str, set[str]] = {}
    for label, pat in ADMIN_LINEAGES.items():
        for c in ind[ind.adm_u.str.contains(pat, na=False, regex=True)][KEY].unique():
            coh.setdefault(c, set()).add(label)
    reg = load_registro()
    reg["g_u"] = reg.Gestor.astype(str).str.upper()
    by_digits = dict(zip(_digits(ind[KEY]), ind[KEY]))
    for label, pat in GESTOR_LINEAGES.items():
        for cd in _digits(reg[reg.g_u.str.contains(pat, na=False, regex=True)][KEY]):
            c = by_digits.get(cd)
            if c:
                coh.setdefault(c, set()).add(label)
    return pd.DataFrame({KEY: list(coh), "lineage": [",".join(sorted(v)) for v in coh.values()]})


def first_failing_gate(row: pd.Series) -> str:
    for col, _ in GATES:
        v = row.get(col)
        if pd.isna(v) or not bool(v):
            return col
    return "PASSES ALL"


def main() -> None:
    ind = pd.read_parquet(DERIVED_DIR / "indicators.parquet")
    cohort = build_cohort(ind)
    cur = apply_filters(enrich(MONTH))
    cohort["filed"] = cohort[KEY].isin(set(cur[KEY]))
    print(f"cohort: {len(cohort):,} classes ever under a liquidated-lineage house")
    print(cohort.lineage.value_counts().head(8).to_string())
    print(f"\nfiled a {MONTH} informe: {cohort.filed.sum():,} ({cohort.filed.mean():.0%})  |  gone dark: {(~cohort.filed).sum():,}")

    live = cur[cur[KEY].isin(cohort[cohort.filed][KEY])].merge(cohort, on=KEY, how="left")
    live["still_old"] = live.administrador_nome.astype(str).str.upper().str.contains(
        "|".join(ADMIN_LINEAGES.values()), na=False, regex=True)
    print(f"\nof the {len(live)} survivors: {int(live.still_old.sum())} still under the old name, "
          f"{int((~live.still_old).sum())} already moved")
    print("\nwho administers the movers now:")
    print(live[~live.still_old].administrador_nome.value_counts().head(8).to_string())

    live["killed_by"] = live.apply(first_failing_gate, axis=1)
    labels = dict(GATES)
    print("\nwhich gate kills them (walked in screen order):")
    for col, _ in GATES + [("PASSES ALL", "")]:
        n = int((live.killed_by == col).sum())
        if n:
            pl = live.loc[live.killed_by == col, "pl"].sum() / 1e9
            print(f"  {labels.get(col, 'survives every gate'):58s} {n:4d}  (R${pl:6.2f}bn PL)")

    t2 = read_table(snapshot(MONTH), "II", MONTH)
    num = lambda s: pd.to_numeric(s.replace("", None), errors="coerce")
    seg = pd.DataFrame({KEY: t2[KEY]})
    for name, col in [("industrial", "TAB_II_A_VL_INDUST"), ("comercial", "TAB_II_C1_VL_COMERC"),
                      ("servicos", "TAB_II_D_VL_SERV"), ("financeiro", "TAB_II_F_VL_FINANC"),
                      ("financeiro_outros", "TAB_II_F8_VL_OUTRO"), ("consignado", "TAB_II_F2_VL_CRED_PESSOA_CONSIG")]:
        seg[name] = num(t2[col]) if col in t2.columns else np.nan
    L = live[[KEY, "carteira", "b2b_share"]].merge(seg, on=KEY, how="left")
    print(f"\nwhat the cohort's R${L.carteira.sum()/1e9:.1f}bn of carteira is actually invested in:")
    for name in ("industrial", "comercial", "servicos", "financeiro", "financeiro_outros", "consignado"):
        print(f"  {name:20s} R${L[name].sum()/1e9:7.2f}bn")
    print(f"\n  median business-to-business share: {L.b2b_share.median():.1%}")
    print(f"  classes with the right paper (b2b >= 60%): {int((L.b2b_share >= 0.60).sum())} of {len(L)}")
    live.to_pickle(DERIVED_DIR / "orphan_cohort.pkl")


if __name__ == "__main__":
    main()
