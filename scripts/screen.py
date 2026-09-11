"""Print the screen funnel and the research list. Usage: .venv/bin/python scripts/screen.py [YYYYMM]"""
from __future__ import annotations

import sys

import pandas as pd

from vazante.config import DERIVED_DIR
from vazante.cvm.screen import GATES, apply_filters, enrich

pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 52)


def main(month: str = "202607") -> None:
    cur = apply_filters(enrich(month))
    print(f"population at {month}: {len(cur):,} classes | register matched {cur.Gestor.notna().mean():.1%}\n")
    print("=== funnel ===")
    mask = pd.Series(True, index=cur.index)
    for col, label in GATES:
        mask &= cur[col].fillna(False)
        print(f"  {label:60s} alone {int(cur[col].fillna(False).sum()):5d}   cumulative {int(mask.sum()):4d}")
    res = cur[mask].copy()
    print(f"\n=== RESEARCH LIST: {len(res)} classes ===")
    print("NOT a calling list. Filter (i), redemption suspension, needs Fundos.NET. Captive books are invisible")
    print("where the administrador names no cedente, so a corporate name in the fund name means captive until")
    print("a human says otherwise.\n")
    if len(res):
        res["PL_Rm"] = (res.pl / 1e6).round(0)
        res["cart_Rm"] = (res.carteira / 1e6).round(0)
        res["PDD%"] = (res.pdd_share_carteira * 100).round(1)
        res["jump_pp"] = (res.pdd_jump_12m * 100).round(1)
        res["b2b%"] = (res.b2b_share * 100).round(1)
        out = res[["DENOM_SOCIAL", "Administrador", "Gestor", "PL_Rm", "cart_Rm", "PDD%", "jump_pp",
                   "b2b%", "n_ced_named_gt10pct", "Situacao_classe"]].sort_values("PL_Rm", ascending=False)
        print(out.to_string(index=False))
        out.to_csv(DERIVED_DIR / f"research_list_{month}.csv", index=False)
        print(f"\nsaved -> {DERIVED_DIR / f'research_list_{month}.csv'}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "202607")
