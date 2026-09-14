"""Build the deal tracker: one workbook, four tabs, for a human to read.

Styled to the same visual language as the target workbook — a navy header band,
ochre section titles, the three tracks colour-coded so the eye can follow one
down the page, and the three money rows picked out in green. Frozen panes and
real column widths on every tab, because an unformatted grid of 150-character
cells is unreadable no matter how good the content is.

    .venv/bin/python -m scripts.build_tracker
"""

from __future__ import annotations

import pandas as pd
import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from scripts.build_call_workbook import PRIORITY, _ascii

OUT = "/home/user/VAZANTE/out/VAZANTE_tracker.xlsx"

NAVY, OCHRE = "1F3864", "9C6318"
TITLE = Font(bold=True, size=18, color=NAVY)
SUB = Font(size=10.5, color="6B7885")
SECT = Font(bold=True, size=12, color=OCHRE)
HDR = Font(bold=True, color="FFFFFF", size=10.5)
BODY = Font(size=10.5)
BOLD = Font(bold=True, size=10.5)
MONEY = Font(bold=True, size=10.5, color="14532D")
KILLF = Font(bold=True, size=10.5, color="9C3A3D")

FILL_HDR = PatternFill("solid", fgColor=NAVY)
FILL_A = PatternFill("solid", fgColor="EDF1F8")
FILL_B = PatternFill("solid", fgColor="FBF2E4")
FILL_C = PatternFill("solid", fgColor="E6F2EC")
FILL_MONEY = PatternFill("solid", fgColor="C9E5D4")
FILL_FIRST = PatternFill("solid", fgColor="DCEBDF")
BAND = PatternFill("solid", fgColor="F5F7FB")
WARN = PatternFill("solid", fgColor="FBE4E4")

THIN = Side(style="thin", color="D8DEE8")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
TOPC = Alignment(vertical="top", horizontal="center")
TRACK_FILL = {"A": FILL_A, "B": FILL_B, "C": FILL_C}

#: Day, track, owner, the action, and the note. The action is short so the column
#: stays narrow; the note carries the reason, which is what stops it being done wrong.
STEPS: list[tuple[str, str, str, str, str]] = [
    ("0", "A", "GC", "He agrees to send the tape",
     ("This is the only thing that counts as a yes. 'Manda a página' is not one. "
     "Do not start the clock before it.")),
    ("0–1", "A", "GC", "NDA signed, both directions",
     ("BEFORE the tape, never after. Once a tape lands we hold personal data and LGPD "
     "applies to us.")),
    ("1", "B", "GC", "Teaser out to the buyers for these lots",
     "No name, no CNPJ, shape only. Do NOT wait for the tape — this is where the weeks are."),
    ("1–3", "A", "MGC", "Short-form corretagem sent",
     ("With the GESTORA as a company, never the fund. Mobilisation fee creditable — say so in "
     "the first sentence, not the last.")),
    ("1–3", "A", "GC", "Tape spec sent WITH the contract",
     "One page of fields. Sending it afterwards costs a week for nothing."),
    ("1–5", "B", "GC", "NDAs back from buyers",
     "Nobody gets exclusivity. Not for a day."),
    ("3", "A", "MGC", "Contract signed · mobilisation invoice raised", ""),
    ("3–5", "A", "GC", "Tape received",
     "Check it opens and has the Tier 1 fields before thanking him for it."),
    ("5", "A", "MGC", "MOBILISATION FEE PAID", "First money."),
    ("3–8", "A", "MGC", "Reconcile the tape against his own CVM informe",
     "If it does not tie, that is finding number one and it goes back to him the same day."),
    ("3–8", "A", "MGC", "Offline sweep",
     ("CNPJ check digits, NF-e chaves, duplicates, a sacado that is its own cedente, "
     "zero-face rows.")),
    ("6–8", "A", "MGC", "Cut the lots", "Recourse, age, cedente status, size."),
    ("8–12", "A", "both", "Build the sale book, per lot",
     "Descriptive only. No opinion of value, anywhere, ever."),
    ("8–12", "A", "GC", "Get the reserve IN WRITING",
     ("Before the round opens. The upside share depends on it and it cannot be agreed "
     "after the bids are in.")),
    ("12", "B", "GC", "Data room opens", "To whoever signed the NDA."),
    ("12–22", "B", "GC", "Run the round",
     ("One standard proposal form for everybody — lot, price, conditions, expiry, arras, "
     "signatory. Otherwise you cannot compare them.")),
    ("22", "B", "GC", "Round closes", "On the day stated in writing on day one."),
    ("23", "C", "both", "Quadro comparativo delivered",
     ("Every indication side by side, normalised, with what each buyer said would move his "
     "number. This is what he is paying for.")),
    ("23", "C", "MGC", "ROUND FEE INVOICED", "Second money. Decouples our cash from his closing."),
    ("23–25", "C", "GC", "He picks", ""),
    ("25–40", "C", "GC", "His counsel drafts the cessão", "We draft nothing."),
    ("25–40", "C", "MGC", "Confirm the buyer pays the FUND directly",
     "We never touch the money. We invoice separately."),
    ("40+", "C", "MGC", "SUCCESS FEE INVOICED on settlement", "Third money."),
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


def head(ws, row: int, cols: list[tuple[str, int]]) -> None:
    for i, (label, width) in enumerate(cols, start=1):
        c = ws.cell(row=row, column=i, value=label)
        c.font, c.fill, c.border = HDR, FILL_HDR, BOX
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[row].height = 30
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def title(ws, t: str, sub: str) -> None:
    ws.cell(row=1, column=1, value=t).font = TITLE
    ws.row_dimensions[1].height = 26
    c = ws.cell(row=2, column=1, value=sub)
    c.font, c.alignment = SUB, Alignment(vertical="center")
    ws.row_dimensions[2].height = 18


def tab_start(wb: Workbook) -> None:
    ws = wb.create_sheet("Start here")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["B"].width = 96
    title(ws, "VAZANTE — deal tracker",
          "14 September 2026 · forty days from a yes to settlement · nobody has been contacted")

    r = 4

    def section(name: str) -> None:
        nonlocal r
        c = ws.cell(row=r, column=1, value=name)
        c.font = SECT
        ws.row_dimensions[r].height = 24
        r += 1

    def line(k: str, v: str, fill=None, font=None) -> None:
        nonlocal r
        a = ws.cell(row=r, column=1, value=k)
        a.font, a.alignment = font or BOLD, WRAP
        b = ws.cell(row=r, column=2, value=v)
        b.font, b.alignment = BODY, WRAP
        if fill:
            a.fill = b.fill = fill
        a.border = b.border = BOX
        ws.row_dimensions[r].height = max(30, 12.5 * (len(v) // 92 + 1))
        r += 1

    section("THE ONE THING THAT MAKES IT FAST")
    line("Two tracks at once, never in sequence",
         ("Track A is the seller — paper, tape, lots. Track B is the buyers — teaser, NDA, "
         "round. Track B starts on DAY ONE from public CVM data, because the distressed lot "
         "can be described without a tape. Every broker runs these end to end and takes "
         "three months."), FILL_B)
    r += 1

    section("HOW TO USE IT")
    line("The 40 days", ("The checklist for ONE live deal. Duplicate the tab per deal and "
                        "rename it after the house. Tick Done and put the date in."))
    line("Pipeline", "Where each of the fifteen houses sits. Update after every call.")
    line("Buyer round", "One row per buyer for the live round.")
    r += 1

    section("WHEN MONEY ARRIVES")
    line("Mobilisation fee", "Day 5, on signature.", FILL_MONEY, MONEY)
    line("Round fee", ("Day 23, on delivery of the quadro comparativo. This is the one that "
                      "decouples our cash from his closing."), FILL_MONEY, MONEY)
    line("Success fee", "Day 40+, on settlement. The amounts are a partner decision.",
         FILL_MONEY, MONEY)
    r += 1

    section("THE RULES THAT NEVER BEND")
    for t in RULES:
        line("", t)
    r += 1

    section("THE FIVE THINGS THAT KILL IT")
    for k, v in KILLERS:
        line(k, v, WARN, KILLF)


def tab_days(wb: Workbook) -> None:
    ws = wb.create_sheet("The 40 days")
    ws.sheet_view.showGridLines = False
    title(ws, "The 40 days",
          "Track A = the seller · Track B = the buyers · Track C = the close")
    ws.cell(row=3, column=1, value="Deal:").font = BOLD
    ws.cell(row=3, column=2, value="[ house name ]").font = BODY
    ws.cell(row=3, column=4, value="Day 0:").font = BOLD
    ws.cell(row=3, column=5, value="[ dd/mm ]").font = BODY
    head(ws, 4, [("Day", 9), ("Track", 7), ("Owner", 8), ("What has to happen", 40),
                 ("Why / watch out", 62), ("Done", 8), ("Date", 11), ("Notes", 30)])

    dv = DataValidation(type="list", formula1='"Yes,No,N/A"', allow_blank=True)
    ws.add_data_validation(dv)
    r = 5
    for day, track, owner, what, note in STEPS:
        money = "FEE" in what
        fill = FILL_MONEY if money else TRACK_FILL[track]
        for j, v in enumerate([day, track, owner, what, note, "", "", ""], start=1):
            c = ws.cell(row=r, column=j, value=v)
            c.font = MONEY if money and j == 4 else BODY
            c.alignment = WRAP if j in (4, 5, 8) else TOPC
            c.fill, c.border = fill, BOX
        dv.add(ws.cell(row=r, column=6))
        ws.row_dimensions[r].height = max(30, 12.5 * (len(note) // 60 + 1))
        r += 1
    ws.auto_filter.ref = f"A4:H{r - 1}"


def tab_pipeline(wb: Workbook) -> None:
    ws = wb.create_sheet("Pipeline")
    ws.sheet_view.showGridLines = False
    title(ws, "Pipeline",
          "Ordered by how fast a house can say yes, not by size. Green = the first three calls.")
    head(ws, 4, [("#", 5), ("House", 36), ("Funds", 7), ("Face R$m", 11), ("Stage", 22),
                 ("Last contact", 13), ("Next step", 34), ("Owner", 8), ("Notes", 38)])

    c = pd.read_csv("data/derived/call_sheet.csv")
    c["rank"] = c.house.map(lambda h: PRIORITY.get(_ascii(h), (99, ""))[0])
    c = c.sort_values(["rank", "face_Rm"], ascending=[True, False]).reset_index(drop=True)
    dv = DataValidation(type="list", formula1='"' + ",".join(STAGES) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    for i, x in c.iterrows():
        r = i + 5
        first = x["rank"] <= 3
        fill = FILL_FIRST if first else (BAND if i % 2 else None)
        for j, v in enumerate([i + 1, x.house.title(), int(x.funds), x.face_Rm,
                               "", "", "", "", ""], start=1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.font = BOLD if first and j == 2 else BODY
            cell.alignment = WRAP if j in (2, 7, 9) else TOPC
            cell.border = BOX
            if fill:
                cell.fill = fill
            if j == 4:
                cell.number_format = "#,##0.0"
        dv.add(ws.cell(row=r, column=5))
        ws.row_dimensions[r].height = 26
    ws.auto_filter.ref = f"A4:I{len(c) + 4}"


def tab_round(wb: Workbook) -> None:
    ws = wb.create_sheet("Buyer round")
    ws.sheet_view.showGridLines = False
    title(ws, "Buyer round",
          ("Fastest to a firm bid first. No price goes in here until it is on the standard "
          "form, in writing, with an expiry and a signatory."))
    ws.cell(row=3, column=1, value="Deal:").font = BOLD
    ws.cell(row=3, column=2, value="[ house name ]").font = BODY
    ws.cell(row=3, column=4, value="Round closes:").font = BOLD
    ws.cell(row=3, column=5, value="[ dd/mm ]").font = BODY
    head(ws, 4, [("Buyer", 34), ("Takes", 30), ("Days to a firm bid", 11),
                 ("Teaser sent", 11), ("NDA back", 10), ("Data room", 10),
                 ("Bid received", 11), ("On the standard form?", 13),
                 ("What would move his number", 44)])

    lot_label = {"A": "not yet due", "A2": "impaired", "B": "1-90d", "C": "90-180d",
                 "D": "180d+", "E": "RJ claims"}
    with open("config/buyer_registry.yaml", encoding="utf-8") as fh:
        reg = yaml.safe_load(fh)
    dv = DataValidation(type="list", formula1='"Yes,No,Chasing"', allow_blank=True)
    ws.add_data_validation(dv)
    for i, b in enumerate(sorted(reg["buyers"], key=lambda b: b["speed_days"])):
        r = i + 5
        fast = b["speed_days"] <= 21
        fill = FILL_FIRST if fast else (BAND if i % 2 else None)
        vals = [b["name"], " · ".join(lot_label.get(x, x) for x in b["lots"]),
                b["speed_days"], "", "", "", "", "", ""]
        for j, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.font = BOLD if fast and j == 1 else BODY
            cell.alignment = WRAP if j in (1, 2, 9) else TOPC
            cell.border = BOX
            if fill:
                cell.fill = fill
        for j in (4, 5, 6, 7, 8):
            dv.add(ws.cell(row=r, column=j))
        ws.row_dimensions[r].height = 26
    ws.auto_filter.ref = f"A4:I{len(reg['buyers']) + 4}"


def main() -> None:
    wb = Workbook()
    wb.remove(wb.active)
    tab_start(wb)
    tab_days(wb)
    tab_pipeline(wb)
    tab_round(wb)
    wb.save(OUT)
    size = slim(OUT)
    print(f"wrote {OUT} ({size:,} bytes)\n  tabs: {', '.join(wb.sheetnames)}")



def slim(path: str = OUT) -> int:
    """Repack with a stub theme and maximum compression.

    openpyxl writes a 10KB Office theme that nothing here uses; replacing it with
    a minimal valid one takes the workbook from 14.2KB to 13.1KB, which matters
    only because the file has to travel. The stub keeps the schema satisfied, so
    Excel, LibreOffice and Google all still open it.
    """
    import zipfile
    from pathlib import Path

    stub = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="t">'
        "<a:themeElements><a:clrScheme name=\"t\">"
        '<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>'
        '<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>'
        '<a:dk2><a:srgbClr val="44546A"/></a:dk2><a:lt2><a:srgbClr val="E7E6E6"/></a:lt2>'
        '<a:accent1><a:srgbClr val="4472C4"/></a:accent1>'
        '<a:accent2><a:srgbClr val="ED7D31"/></a:accent2>'
        '<a:accent3><a:srgbClr val="A5A5A5"/></a:accent3>'
        '<a:accent4><a:srgbClr val="FFC000"/></a:accent4>'
        '<a:accent5><a:srgbClr val="5B9BD5"/></a:accent5>'
        '<a:accent6><a:srgbClr val="70AD47"/></a:accent6>'
        '<a:hlink><a:srgbClr val="0563C1"/></a:hlink>'
        '<a:folHlink><a:srgbClr val="954F72"/></a:folHlink>'
        '</a:clrScheme><a:fontScheme name="t"><a:majorFont>'
        '<a:latin typeface="Calibri Light"/><a:ea typeface=""/><a:cs typeface=""/>'
        '</a:majorFont><a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/>'
        '<a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="t">'
        '<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
        '<a:lnStyleLst><a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '<a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '<a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
        "<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>"
        "<a:effectStyle><a:effectLst/></a:effectStyle>"
        "<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>"
        '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
        "</a:fmtScheme></a:themeElements></a:theme>"
    )
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(
        tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zout:
        for it in zin.infolist():
            body = stub.encode() if it.filename == "xl/theme/theme1.xml" else zin.read(it.filename)
            zout.writestr(it.filename, body)
    Path(tmp).replace(path)
    return Path(path).stat().st_size

if __name__ == "__main__":
    main()
