"""Build the lot plan for every target fund, from public CVM data only.

This is what a first call carries.  No tape, no price, no opinion of value —
just the shape of the book cut along the four boundaries the fund itself already
reports, so the conversation starts with a plan instead of a question.

    .venv/bin/python scripts/lot_plan.py
"""

from __future__ import annotations

import pandas as pd

from vazante.lots import carve_universe

TARGETS = "data/derived/targets_full.pkl"
OUT = "data/derived/lot_plan.csv"
M = 1_000_000.0


def main() -> None:
    t = pd.read_pickle(TARGETS)
    q = t[t["captive_flag"] == False].copy()
    plan = carve_universe(q).sort_values("carteira", ascending=False)
    plan.to_csv(OUT, index=False)

    lots = ["lot_A", "lot_B", "lot_C", "lot_D", "lot_E"]
    print(f"{len(plan)} funds · carteira R${plan.carteira.sum() / M:,.0f}m · "
          f"gross face R${plan.gross_face.sum() / M:,.0f}m\n")
    print("Universe by lot (gross face, R$m):")
    for c in lots:
        v = plan[c].sum() / M
        print(f"  {c[-1]}  {v:>8,.0f}   {100 * v / (plan.gross_face.sum() / M):>5.1f}%")
    print(f"\n  with recourse     {plan.recourse_face.sum() / M:>8,.0f}")
    print(f"  without recourse  {plan.non_recourse_face.sum() / M:>8,.0f}")

    print("\nLots that are one person's decision (under R$10m) — the fast ones:")
    small = []
    for _, r in plan.iterrows():
        for c in lots:
            if 0 < r[c] <= 10 * M:
                small.append((r["name"][:34], c[-1], r[c] / M))
    print(f"  {len(small)} lots across {len({s[0] for s in small})} funds, "
          f"R${sum(s[2] for s in small):,.0f}m of face in total")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
