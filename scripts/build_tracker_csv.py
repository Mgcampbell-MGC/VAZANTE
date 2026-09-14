"""Emit the tracker as three CSVs — one clean grid each.

They were one sheet with three sections stacked, and it read badly: a single
column had to hold both 150 characters of task text and a numeric face value,
three different header rows shared one grid, and a CSV upload carries no column
widths. Three focused sheets each have one header row and one set of column
semantics, which is legible without any formatting at all.

    .venv/bin/python -m scripts.build_tracker_csv out/t1.csv out/t2.csv out/t3.csv
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pandas as pd
import yaml

from scripts.build_call_workbook import PRIORITY, _ascii
from scripts.build_tracker import KILLERS, RULES, STAGES, STEPS

LOT_LABEL = {"A": "not yet due", "A2": "impaired", "B": "1-90d", "C": "90-180d",
             "D": "180d+", "E": "RJ claims"}


def sheet_days(w) -> None:
    w.writerow(["Deal:", "[ house name ]", "", "Day 0:", "[ dd/mm ]", "", "", ""])
    w.writerow(["Day", "Track", "Owner", "What has to happen", "Why / watch out",
                "Done", "Date done", "Notes"])
    for day, track, owner, what, note in STEPS:
        w.writerow([day, track, owner, what, note, "", "", ""])
    w.writerow([])
    w.writerow(["Track A = the seller", "Track B = the buyers", "Track C = the close"])
    w.writerow([])
    w.writerow(["THE RULES THAT NEVER BEND"])
    for t in RULES:
        w.writerow(["", t])
    w.writerow([])
    w.writerow(["THE FIVE THINGS THAT KILL IT", "The answer"])
    for k, v in KILLERS:
        w.writerow([k, v])


def sheet_pipeline(w) -> None:
    c = pd.read_csv("data/derived/call_sheet.csv")
    c["rank"] = c.house.map(lambda h: PRIORITY.get(_ascii(h), (99, ""))[0])
    c = c.sort_values(["rank", "face_Rm"], ascending=[True, False]).reset_index(drop=True)
    w.writerow(["#", "House", "Funds", "Face R$m", "Stage", "Last contact", "Next step",
                "Owner", "Notes"])
    for i, x in c.iterrows():
        w.writerow([i + 1, x.house.title(), int(x.funds), x.face_Rm, "", "", "", "", ""])
    w.writerow([])
    w.writerow(["Stages, in order"])
    for i, s in enumerate(STAGES, start=1):
        w.writerow([i, s])


def sheet_round(w) -> None:
    w.writerow(["Deal:", "[ house name ]", "", "Round closes:", "[ dd/mm ]", "", "", "", ""])
    w.writerow(["Buyer", "Takes", "Days to a firm bid", "Teaser sent", "NDA back",
                "Data room", "Bid received", "On the standard form?",
                "What would move his number"])
    reg = yaml.safe_load(Path("config/buyer_registry.yaml").read_text(encoding="utf-8"))
    for b in sorted(reg["buyers"], key=lambda b: b["speed_days"]):
        w.writerow([b["name"], " · ".join(LOT_LABEL.get(x, x) for x in b["lots"]),
                    b["speed_days"], "", "", "", "", "", ""])
    w.writerow([])
    w.writerow([("No price goes in this sheet until it is on the standard form, in writing, "
                "with an expiry and a signatory.")])


def main() -> None:
    out = sys.argv[1:4]
    for path, fn in zip(out, (sheet_days, sheet_pipeline, sheet_round), strict=True):
        with Path(path).open("w", newline="", encoding="utf-8") as fh:
            fn(csv.writer(fh))
        print(f"wrote {path} ({Path(path).stat().st_size} bytes)")


if __name__ == "__main__":
    main()
