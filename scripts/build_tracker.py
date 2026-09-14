"""Build the deal tracker: the 40 days as something GC ticks off.

Four tabs. The 40 days is the master checklist for one live deal; Pipeline is
where each of the fifteen houses sits; Buyer round is the log for one round.
Uploaded to Drive as a Google Sheet, so it stays small and unstyled where styling
would not survive the conversion.

    .venv/bin/python -m scripts.build_tracker
"""

from __future__ import annotations

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from scripts.build_call_workbook import PRIORITY, _ascii

OUT = "/home/user/VAZANTE/out/VAZANTE_tracker.xlsx"

HDR = Font(bold=True, color="FFFFFF", size=11)
FILL_A = PatternFill("solid", fgColor="1F3864")   # seller track
FILL_B = PatternFill("solid", fgColor="9C6318")   # buyer track
FILL_C = PatternFill("solid", fgColor="2C6E4F")   # the close
BAND = PatternFill("solid", fgColor="F2F5FB")
WARN = PatternFill("solid", fgColor="FCE4E4")
BOLD = Font(bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")

#: Day, track, owner, task. The whole deal, in order.
STEPS: list[tuple[str, str, str, str]] = [
    ("0", "A", "GC", ("He agreed to send the tape. Nothing before this counts as a yes — "
                     "do not start the clock on 'manda a página'.")),
    ("0–1", "A", "GC", ("NDA signed both directions. BEFORE the tape, never after — once a tape "
                       "lands we hold personal data and LGPD applies to us.")),
    ("1", "B", "GC", ("Teaser out to the named buyers for this book's lots. No name, no CNPJ, "
                     "shape only. Do not wait for the tape.")),
    ("1–3", "A", "MGC", ("Short-form corretagem sent. With the GESTORA as a company, never the "
                        "fund. Mobilisation fee creditable — say so in the first sentence.")),
    ("1–3", "A", "GC", "Tape spec sent WITH the contract, not after. One page of fields."),
    ("1–5", "B", "GC", "NDAs back from buyers. Nobody gets exclusivity, not for a day."),
    ("3", "A", "MGC", "Contract signed. Mobilisation invoice raised."),
    ("3–5", "A", "GC", ("Tape received. Check it opens and has the Tier 1 fields before "
                       "thanking him for it.")),
    ("5", "A", "MGC", "MOBILISATION FEE PAID — first money."),
    ("3–8", "A", "MGC", ("Reconcile the tape against his own CVM informe. If it does not tie, "
                        "that is finding one and it goes back the same day.")),
    ("3–8", "A", "MGC", ("Offline sweep: CNPJ check digits, NF-e chaves, duplicates, sacado that "
                        "is its own cedente, zero-face rows.")),
    ("6–8", "A", "MGC", "Cut the lots. Recourse, age, cedente status, size."),
    ("8–12", "A", "both", "Sale book per lot. Descriptive only — no opinion of value, anywhere."),
    ("8–12", "A", "GC", ("Get the reserve IN WRITING before the round opens. The upside share "
                        "depends on it and it cannot be agreed afterwards.")),
    ("12", "B", "GC", "Data room opens to whoever signed."),
    ("12–22", "B", "GC", ("The round. One standard proposal form for everybody — lot, price, "
                         "conditions, expiry, arras, signatory.")),
    ("22", "B", "GC", "Round closes. On the day stated in writing on day one."),
    ("23", "C", "both", ("Quadro comparativo delivered. Every indication side by side, "
                        "normalised. This is what he is paying for.")),
    ("23", "C", "MGC", "ROUND FEE INVOICED — second money."),
    ("23–25", "C", "GC", "He picks."),
    ("25–40", "C", "GC", ("His counsel drafts the instrumento particular de cessão. We draft "
                         "nothing.")),
    ("25–40", "C", "MGC", "Confirm the buyer pays the FUND directly. We never touch the money."),
    ("40+", "C", "MGC", "SUCCESS FEE INVOICED on settlement — third money."),
]

KILLERS = [
    ('"Traga uma proposta primeiro."',
     ("Worse than a no — it feels like progress. Answer: a fee small enough not to be a decision, "
     "and fully creditable. Have the short-form in your pocket BEFORE the call.")),
    ("The tape arrives broken or half-empty.",
     ("Spec goes out WITH the contract. Tell him plainly: a missing sacado CNPJ is the difference "
     "between a lot that can be sold and one that cannot.")),
    ("The administrador blocks it.",
     ("Pick houses where the gestor and administrador are the same people. Libertas / Actual is the "
     "only one on the list — which is why it is call number one.")),
    ("A buyer asks for exclusivity.",
     ("No. The round is the product. A buyer who will not bid against others was never going to pay "
     "a real number.")),
    ("Title.",
     "We warrant nothing and we say so on the first call. The buyer runs his own registradora check."),
]

RULES = [
    "No price out of a call, an email or a session. A price comes out of a round.",
    "Never laudo, parecer, auditoria, avaliação, mandato, or an opinion of value.",
    "The gestora signs, never the fund.",
    "We never hold the money — the buyer pays the fund directly.",
    "We never buy.",
]

STAGES = ["Emailed", "Replied", "Call held", "Said yes (tape agreed)", "NDA signed",
          "Contract signed", "Tape received", "Lots cut", "Round open", "Round closed",
          "Settled"]


def head(ws, row: int, cols: list[tuple[str, int]], fill=FILL_A) -> None:
    for i, (label, width) in enumerate(cols, start=1):
        c = ws.cell(row=row, column=i, value=label)
        c.font, c.fill = HDR, fill
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def tab_start(wb: Workbook) -> None:
    ws = wb.create_sheet("Start here")
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 100
    rows = [
        ("VAZANTE — deal tracker", ""),
        ("", "14 September 2026. Forty days from a yes to settlement. Nobody has been contacted."),
        ("", ""),
        ("THE ONE THING THAT MAKES IT FAST", ""),
        ("Two tracks at once, never in sequence",
         ("Track A is the seller: paper, tape, lots. Track B is the buyers: teaser, NDA, round. "
         "Track B starts on DAY ONE from public CVM data — the distressed lot can be described "
         "without a tape. Every broker runs these end to end and takes three months.")),
        ("", ""),
        ("HOW TO USE IT", ""),
        ("The 40 days",
         ("The master checklist for ONE live deal. Copy the tab per deal and rename it after the "
         "house. Tick Done and put the date in.")),
        ("Pipeline", "Where each of the fifteen houses sits. Update after every call."),
        ("Buyer round", "One row per buyer per lot, for the live round."),
        ("", ""),
        ("WHEN MONEY ARRIVES", ""),
        ("Mobilisation fee", "Day 5, on signature."),
        ("Round fee", ("Day 23, on delivery of the quadro comparativo. This is the one that "
                      "decouples our cash from their closing.")),
        ("Success fee", "Day 40+, on settlement. The amounts are a partner decision."),
        ("", ""),
        ("THE RULES THAT NEVER BEND", ""),
    ]
    r = 1
    for k, v in rows:
        if k and not v:
            c = ws.cell(row=r, column=1, value=k)
            c.font = Font(bold=True, size=13, color="1F3864")
        else:
            ws.cell(row=r, column=1, value=k).font = BOLD
            ws.cell(row=r, column=1).alignment = WRAP
            ws.cell(row=r, column=2, value=v).alignment = WRAP
        ws.row_dimensions[r].height = max(16, 13 * (len(v) // 95 + 1))
        r += 1
    for t in RULES:
        ws.cell(row=r, column=2, value="•  " + t).alignment = WRAP
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="THE FIVE THINGS THAT KILL IT").font = Font(
        bold=True, size=13, color="9C3A3D")
    r += 1
    for k, v in KILLERS:
        ws.cell(row=r, column=1, value=k).font = BOLD
        ws.cell(row=r, column=1).alignment = WRAP
        c = ws.cell(row=r, column=2, value=v)
        c.alignment, c.fill = WRAP, WARN
        ws.row_dimensions[r].height = max(30, 13 * (len(v) // 95 + 1))
        r += 1


def tab_days(wb: Workbook) -> None:
    ws = wb.create_sheet("The 40 days")
    ws.cell(row=1, column=1, value="Deal:").font = BOLD
    ws.cell(row=1, column=2, value="[ house name ]")
    ws.cell(row=1, column=4, value="Day 0 date:").font = BOLD
    ws.cell(row=1, column=5, value="[ dd/mm ]")
    head(ws, 3, [("Day", 8), ("Track", 8), ("Owner", 9), ("What has to happen", 86),
                 ("Done", 8), ("Date done", 12), ("Notes", 42)])
    dv = DataValidation(type="list", formula1='"Yes,No,N/A"', allow_blank=True)
    ws.add_data_validation(dv)
    r = 4
    for day, track, owner, what in STEPS:
        fill = {"A": BAND, "B": PatternFill("solid", fgColor="FBF3E6"),
                "C": PatternFill("solid", fgColor="E9F3EE")}[track]
        for j, v in enumerate([day, track, owner, what, "", "", ""], start=1):
            c = ws.cell(row=r, column=j, value=v)
            c.alignment = WRAP if j in (4, 7) else Alignment(
                vertical="top", horizontal="center")
            c.fill = fill
            if j == 4 and ("FEE" in what or "first money" in what or "second money" in what
                           or "third money" in what):
                c.font = BOLD
        dv.add(ws.cell(row=r, column=5))
        ws.row_dimensions[r].height = max(28, 13 * (len(what) // 82 + 1))
        r += 1
    ws.auto_filter.ref = f"A3:G{r - 1}"


def tab_pipeline(wb: Workbook) -> None:
    ws = wb.create_sheet("Pipeline")
    c = pd.read_csv("data/derived/call_sheet.csv")
    c["rank"] = c.house.map(lambda h: PRIORITY.get(_ascii(h), (99, ""))[0])
    c = c.sort_values(["rank", "face_Rm"], ascending=[True, False]).reset_index(drop=True)

    cols = [("#", 5), ("House", 34), ("Funds", 7), ("Face R$m", 10), ("Stage", 22),
            ("Last contact", 13), ("Next step", 34), ("Owner", 9), ("Notes", 44)]
    head(ws, 1, cols, fill=FILL_B)
    dv = DataValidation(type="list", formula1='"' + ",".join(STAGES) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    for i, x in c.iterrows():
        r = i + 2
        vals = [i + 1, x.house.title(), int(x.funds), x.face_Rm, "", "", "", "", ""]
        for j, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.alignment = WRAP if j in (2, 7, 9) else Alignment(
                vertical="top", horizontal="center")
            if x["rank"] <= 3:
                cell.fill = PatternFill("solid", fgColor="E3EFE8")
            elif i % 2:
                cell.fill = BAND
            if j == 4:
                cell.number_format = "#,##0.0"
        dv.add(ws.cell(row=r, column=5))
    ws.auto_filter.ref = f"A1:I{len(c) + 1}"


def tab_round(wb: Workbook) -> None:
    ws = wb.create_sheet("Buyer round")
    ws.cell(row=1, column=1, value="Deal:").font = BOLD
    ws.cell(row=1, column=2, value="[ house name ]")
    ws.cell(row=1, column=4, value="Round closes:").font = BOLD
    ws.cell(row=1, column=5, value="[ dd/mm ]")
    head(ws, 3, [("Buyer", 30), ("Lot", 14), ("Teaser sent", 12), ("NDA back", 11),
                 ("Data room", 11), ("Bid received", 12), ("On the standard form?", 14),
                 ("Expiry", 11), ("What would move his number", 46)])
    dv = DataValidation(type="list", formula1='"Yes,No,Chasing"', allow_blank=True)
    ws.add_data_validation(dv)
    import yaml
    reg = yaml.safe_load(open("config/buyer_registry.yaml", encoding="utf-8"))  # noqa: SIM115
    names = [b["name"] for b in sorted(reg["buyers"], key=lambda b: b["speed_days"])]
    for i, n in enumerate(names):
        r = i + 4
        ws.cell(row=r, column=1, value=n).alignment = WRAP
        for j in range(2, 10):
            cell = ws.cell(row=r, column=j)
            cell.alignment = WRAP if j == 9 else Alignment(
                vertical="top", horizontal="center")
            if i % 2:
                cell.fill = BAND
        for j in (3, 4, 5, 6, 7):
            dv.add(ws.cell(row=r, column=j))
        if i % 2:
            ws.cell(row=r, column=1).fill = BAND
    ws.cell(row=len(names) + 5, column=1,
            value=("No price goes in this sheet until it is on the standard form, in writing, "
                  "with an expiry and a signatory.")).font = Font(bold=True, color="9C3A3D")


def main() -> None:
    wb = Workbook()
    wb.remove(wb.active)
    tab_start(wb)
    tab_days(wb)
    tab_pipeline(wb)
    tab_round(wb)
    wb.save(OUT)
    print(f"wrote {OUT}\n  tabs: {', '.join(wb.sheetnames)}")


if __name__ == "__main__":
    main()
