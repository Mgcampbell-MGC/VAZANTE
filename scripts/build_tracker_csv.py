"""Emit the tracker as one CSV, for upload to Drive as a Google Sheet.

Three sections stacked in one tab, separated by banner rows. The .docx-style
multi-tab workbook exists too (scripts/build_tracker.py) but a Sheet built from
text uploads reliably, and one tab someone actually scrolls beats four tabs that
arrived corrupt.

    .venv/bin/python -m scripts.build_tracker_csv > out/tracker.csv
"""

from __future__ import annotations

import csv
import sys

import pandas as pd
import yaml

from scripts.build_call_workbook import PRIORITY, _ascii
from scripts.build_tracker import KILLERS, RULES, STAGES, STEPS


def main() -> None:
    w = csv.writer(sys.stdout)
    r = w.writerow

    r(["VAZANTE — DEAL TRACKER"])
    r(["14 September 2026 · forty days from a yes to settlement · nobody has been contacted"])
    r([])
    r(["THE ONE THING THAT MAKES IT FAST"])
    r([("Two tracks at once, never in sequence. Track A is the seller: paper, tape, lots. "
       "Track B is the buyers: teaser, NDA, round. Track B starts on DAY ONE from public CVM "
       "data — the distressed lot can be described without a tape. Every broker runs these "
       "end to end and takes three months.")])
    r([])
    r(["THE RULES THAT NEVER BEND"])
    for t in RULES:
        r(["", t])
    r([])

    r(["SECTION 1 — THE 40 DAYS"])
    r(["Copy this section per deal. Tick Done and put the date in."])
    r(["Deal:", "[ house name ]", "", "Day 0 date:", "[ dd/mm ]"])
    r(["Day", "Track", "Owner", "What has to happen", "Done", "Date done", "Notes"])
    for day, track, owner, what in STEPS:
        r([day, track, owner, what, "", "", ""])
    r([])
    r(["Track A = seller · Track B = buyers · Track C = the close"])
    r([])

    r(["SECTION 2 — PIPELINE"])
    r([("Where each house sits. Update after every call. "
       "Stages: ") + " / ".join(STAGES)])
    c = pd.read_csv("data/derived/call_sheet.csv")
    c["rank"] = c.house.map(lambda h: PRIORITY.get(_ascii(h), (99, ""))[0])
    c = c.sort_values(["rank", "face_Rm"], ascending=[True, False]).reset_index(drop=True)
    r(["#", "House", "Funds", "Face R$m", "Stage", "Last contact", "Next step", "Owner", "Notes"])
    for i, x in c.iterrows():
        r([i + 1, x.house.title(), int(x.funds), x.face_Rm, "", "", "", "", ""])
    r([])

    r(["SECTION 3 — BUYER ROUND"])
    r([("One row per buyer, for the live round. "
       "No price goes in this sheet until it is on the standard form, in writing, "
       "with an expiry and a signatory.")])
    r(["Deal:", "[ house name ]", "", "Round closes:", "[ dd/mm ]"])
    r(["Buyer", "Takes", "Days to a firm bid", "Teaser sent", "NDA back", "Data room",
       "Bid received", "On the standard form?", "What would move his number"])
    reg = yaml.safe_load(open("config/buyer_registry.yaml", encoding="utf-8"))  # noqa: SIM115
    lot_label = {"A": "not yet due", "A2": "impaired", "B": "1-90d", "C": "90-180d",
                 "D": "180d+", "E": "RJ claims"}
    for b in sorted(reg["buyers"], key=lambda b: b["speed_days"]):
        r([b["name"], " · ".join(lot_label.get(x, x) for x in b["lots"]),
           b["speed_days"], "", "", "", "", "", ""])
    r([])

    r(["THE FIVE THINGS THAT KILL IT"])
    for k, v in KILLERS:
        r([k, v])


if __name__ == "__main__":
    main()
