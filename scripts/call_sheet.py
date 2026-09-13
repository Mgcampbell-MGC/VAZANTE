"""Build the call sheet: one row per house, with its own lot plan and its own buyers.

Fifteen conversations reach all twenty-five funds. Each row carries what that house
actually holds, the buyers whose appetite covers those lots, and a Portuguese
opening that states facts from the house's own filings and asks for the tape.

No price appears anywhere in the Portuguese. Operating rule 2.

    .venv/bin/python scripts/call_sheet.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from vazante.lots import route

M = 1_000_000.0
LOTS = ["A", "A2", "B", "C", "D"]
OUT = "data/derived/call_sheet.csv"


def build() -> pd.DataFrame:
    lp = pd.read_csv("data/derived/lot_plan.csv")
    t = pd.read_pickle("data/derived/targets_full.pkl")
    cols = ["CNPJ_FUNDO_CLASSE", "Gestor", "Administrador", "Diretor", "n_ced", "n_rj"]
    d = lp.merge(t[t["captive_flag"] == False][cols], left_on="cnpj",
                 right_on="CNPJ_FUNDO_CLASSE", how="left")

    d["house"] = d["Gestor"].fillna(d["Administrador"])
    # Libertas and Actual share two officers and a switchboard — one conversation.
    d.loc[d["Administrador"].astype(str).str.contains("ACTUAL", na=False), "house"] = (
        "LIBERTAS / ACTUAL"
    )

    agg = {f"lot_{k}": (f"lot_{k}", "sum") for k in LOTS}
    g = d.groupby("house").agg(
        funds=("cnpj", "count"), face=("gross_face", "sum"), carteira=("carteira", "sum"),
        provision=("provision", "sum"), recourse=("recourse_face", "sum"),
        true_sale=("true_sale_face", "sum"), cedentes=("n_ced", "sum"), in_rj=("n_rj", "sum"),
        **agg,
    )
    g["recourse_share"] = g.recourse / (g.recourse + g.true_sale).replace(0, np.nan)
    g["provision_pct"] = g.provision / g.carteira
    return g.sort_values("face", ascending=False)


#: The two blocks a buyer actually shops for.  Routing the whole book at once
#: returns the same generic names for every house, which is useless on a call;
#: routing each block separately is the question a gestor is really asking.
BLOCKS = {"performing": ["A", "A2", "B"], "distressed": ["C", "D"]}


def buyers_for(row: pd.Series, block: str, *, limit: int = 4) -> list:
    lot_face = {k: float(row[f"lot_{k}"]) for k in BLOCKS[block]}
    share = None if pd.isna(row.recourse_share) else float(row.recourse_share)
    return route(lot_face, recourse_share=share)[:limit]


def main() -> None:
    g = build()
    rows = []
    for house, r in g.iterrows():
        rec = {
            "house": house, "funds": int(r.funds),
            "face_Rm": round(r.face / M, 1), "carteira_Rm": round(r.carteira / M, 1),
            "provision_pct": round(100 * r.provision_pct),
            **{f"lot_{k}_Rm": round(r[f"lot_{k}"] / M, 1) for k in LOTS},
            "recourse_pct": None if pd.isna(r.recourse_share) else round(100 * r.recourse_share),
            "cedentes": int(r.cedentes), "in_rj": int(r.in_rj),
        }
        for block, keys in BLOCKS.items():
            ms = buyers_for(r, block)
            rec[f"{block}_Rm"] = round(sum(r[f"lot_{k}"] for k in keys) / M, 1)
            rec[f"{block}_buyers"] = " · ".join(m.buyer.name for m in ms)
            rec[f"{block}_days"] = ms[0].buyer.speed_days if ms else None
            rec[f"{block}_n"] = len(ms)
        rows.append(rec)
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)

    print(f"{len(out)} conversations reach {int(out.funds.sum())} funds, "
          f"R${out.face_Rm.sum():,.0f}m of gross face\n")
    for _, r in out.iterrows():
        rp = "not reported" if pd.isna(r.recourse_pct) else f"{r.recourse_pct:.0f}%"
        print(f"{r.house[:46]}  ·  {r.funds} fund(s)  ·  R${r.face_Rm:,.0f}m face  ·  "
              f"PDD {r.provision_pct}%  ·  recourse {rp}")
        for block in BLOCKS:
            names = r[f"{block}_buyers"] or "NO NAMED BUYER"
            print(f"    {block:11} R${r[f'{block}_Rm']:7,.1f}m  ->  {names}")
        print()

    thin = out[(out.recourse_pct == 0) & (out.performing_Rm > 0)]
    if len(thin):
        print("TRUE-SALE BOOKS — the buyer must underwrite the debtor, and we have "
              f"almost no named firm for that ({len(thin)} houses, "
              f"R${thin.performing_Rm.sum():,.0f}m of performing face):")
        for _, r in thin.iterrows():
            print(f"    {r.house[:44]:46} R${r.performing_Rm:7,.1f}m")
        print("    -> the registry is almost entirely cedente-underwriters. This is a "
              "gap in the research, not in the market.\n")

    small = out[(out.distressed_n == 0) & (out.distressed_Rm > 0)]
    if len(small):
        print("DISTRESSED BLOCKS TOO SMALL FOR ANY CHEQUE FLOOR:")
        for _, r in small.iterrows():
            print(f"    {r.house[:44]:46} R${r.distressed_Rm:7,.1f}m face "
                  f"-> roughly R${r.distressed_Rm * 0.03:.1f}-{r.distressed_Rm * 0.08:.1f}m of price")
        print("    -> bundle across houses, or leave them.\n")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
