"""Build the call-sheet workbook: the sheet GC works from on a call.

Five tabs. Call order is not size order — the ranking encodes how fast a house can
say yes, not how big its book is. Values rather than formulas, for the same reason
as the target workbook: the recalculation toolchain is not available here and an
unevaluated formula reads as blank in most viewers.

No price appears anywhere in this workbook, and none of laudo, parecer, auditoria,
avaliacao or mandato appears in any Portuguese cell.

    .venv/bin/python scripts/build_call_workbook.py
"""

from __future__ import annotations

import pandas as pd
import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from scripts.call_sheet_md import opening, short

OUT = "/home/user/VAZANTE/out/VAZANTE_call_sheet_2026-09-13.xlsx"
M = 1_000_000.0

A = "Calibri"
TITLE = Font(name=A, size=18, bold=True, color="1F3864")
H2 = Font(name=A, size=13, bold=True, color="1F3864")
HDR = Font(name=A, size=11, bold=True, color="FFFFFF")
BODY = Font(name=A, size=11)
BOLD = Font(name=A, size=11, bold=True)
SUBF = Font(name=A, size=11, color="404040")
MONO = Font(name="Consolas", size=10.5)
SCRIPT = Font(name=A, size=12)
FILL_H = PatternFill("solid", fgColor="1F3864")
BAND = PatternFill("solid", fgColor="F2F5FB")
FIRST = PatternFill("solid", fgColor="C6E0B4")   # call these first
WARN = PatternFill("solid", fgColor="FCE4E4")    # no buyer / too small
QUOTE = PatternFill("solid", fgColor="FFF8E7")
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")
NUM = '#,##0.0;(#,##0.0);-'

#: Why each house sits where it does. Ranked by how fast it can say yes.
PRIORITY: dict[str, tuple[int, str]] = {
    "LIBERTAS / ACTUAL": (
        1, ("The only house where the same two officers sign the gestora AND the administrador "
            "- Guilherme Mourao Vaz and Marcelo Faria Rodrigues, salas 1001 and 1003 of the same "
            "building, one switchboard. Everywhere else a deal needs two parties to agree, and "
            "that is the three weeks. Two of their four books have nothing left un-matured, so "
            "there is no performing block to defend and one quota-holder each."),
    ),
    "OURO PRETO GESTAO DE RECURSOS S.A.": (
        2, ("The biggest real deal that is not Solis. Four funds, the largest pooled distressed "
            "lot on the list, Albatroz provisioned at 99% and two cedentes already in "
            "recuperacao judicial."),
    ),
    "SOLIS INVESTIMENTOS S A": (
        3, ("Biggest book in the market and the slowest room. Patria completed its purchase of "
            "51% of Solis on 2 January 2026; legacy books get cleaned in year one of a control "
            "change, and that clock started nine months ago. But procurement at a house owned by "
            "a listed manager is not a four-week process. Call early, expect late."),
    ),
    "INTRA BLACK INVESTIMENTOS GESTAO DE RECURSOS LTDA": (
        4, ("Provisioned at 189% of carteira and entirely recourse paper, so the cedente is on "
            "the hook for all of it."),
    ),
    "PETRA CAPITAL GESTAO DE INVESTIMENTOS LTDA": (
        5, "Distressed is nearly half the book and four cedentes are in recuperacao judicial.",
    ),
    "TERCON INVESTIMENTOS S.A.": (
        6, "Four funds, but the distressed block is thin and matches only the cedente.",
    ),
}


def _ascii(s: object) -> str:
    """Match a house name against PRIORITY without tripping on accents."""
    return (str(s).upper().replace("Ã", "A").replace("Á", "A").replace("Â", "A")
            .replace("É", "E").replace("Ê", "E").replace("Í", "I").replace("Ó", "O")
            .replace("Ô", "O").replace("Ú", "U").replace("Ç", "C"))


def head(ws, row: int, cols: list[tuple[str, int]]) -> None:
    for i, (label, width) in enumerate(cols, start=1):
        c = ws.cell(row=row, column=i, value=label)
        c.font, c.fill = HDR, FILL_H
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[row].height = 30


def title(ws, t: str, sub: str) -> None:
    ws["A1"] = t
    ws["A1"].font = TITLE
    ws["A2"] = sub
    ws["A2"].font = SUBF
    ws["A2"].alignment = WRAP
    ws.row_dimensions[2].height = 30


def load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    c = pd.read_csv("data/derived/call_sheet.csv")
    lp = pd.read_csv("data/derived/lot_plan.csv")
    t = pd.read_pickle("data/derived/targets_full.pkl")
    tt = t[t["captive_flag"] == False]
    lp = lp.merge(tt[["CNPJ_FUNDO_CLASSE", "Gestor", "Administrador", "Diretor", "n_ced", "n_rj"]],
                  left_on="cnpj", right_on="CNPJ_FUNDO_CLASSE", how="left")
    lp["house"] = lp["Gestor"].fillna(lp["Administrador"])
    lp.loc[lp["Administrador"].astype(str).str.contains("ACTUAL", na=False), "house"] = (
        "LIBERTAS / ACTUAL"
    )
    ct = pd.read_csv("data/derived/contacts.csv")

    c["rank"] = c.house.map(lambda h: PRIORITY.get(_ascii(h), (99, ""))[0])
    c["why"] = c.house.map(lambda h: PRIORITY.get(_ascii(h), (99, ""))[1])
    c = c.sort_values(["rank", "face_Rm"], ascending=[True, False]).reset_index(drop=True)
    return c, lp, ct


def contact(ct: pd.DataFrame, house: str) -> tuple[str, str, str]:
    m = ct[ct.name.str.contains(house.split()[0], case=False, na=False)]
    if not len(m):
        return "-", "-", "-"
    r = m.iloc[0]
    ph = str(r.phone)
    phone = f"+55 {ph[:2]} {ph[2:-4]}-{ph[-4:]}" if ph and ph != "nan" else "-"
    return phone, str(r.city), "; ".join(str(r.socios).split("; ")[:4])


def sheet_start(wb: Workbook, c: pd.DataFrame) -> None:
    ws = wb.create_sheet("Start here")
    title(ws, "VAZANTE — the call sheet",
          f"13 September 2026.  {len(c)} conversations reach 25 funds, "
          f"R${c.face_Rm.sum():,.0f}m of gross face.  Nobody has been contacted.")
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 104

    blocks = [
        ("WHAT CHANGED", ""),
        ("The model", ("VAZANTE no longer buys. It is paid by the seller to cut a broken carteira "
          "into lots and sell each lot to the buyer who wants that risk. The sheet "
          "built on 12 September pitched 'compra carteiras inteiras, a vista, como "
          "principal' on every row. That was the old model and it cannot close fast.")),
        ("The opening", ("Each row now opens with that house's own lot plan, taken from its own "
          "filings, and ends with one small ask: a page listing the fields we need "
          "in the tape. The old sheet opened with a question about art. 44 par. 3, "
          "which produces a conversation rather than a transaction.")),
        ("The fact that carries every call",
         ("It is theirs, not ours. Across all 25 funds, third-party sales total R$5.0m EVER - one "
          "fund, twice, last in October 2024. Nothing has been sold to anybody in twenty-two "
          "months. Meanwhile the cedentes repurchased R$1,033m in the twelve months to July. "
          "These books have exactly one buyer and it is the man who sold them the paper.")),
        ("", ""),
        ("RULES FOR EVERY CALL", ""),
        ("No price",
         ("Not indicative, not a range, not 'somewhere around'. If asked, the answer is that a "
          "price comes out of a competitive round, not out of a phone call.")),
        ("Never say",
         ("laudo, parecer, auditoria, avaliacao or mandato. The contract is a CORRETAGEM under "
          "arts. 722-729 do Codigo Civil - it introduces without binding. A mandato binds, and we "
          "must not have one.")),
        ("The gestora signs, never the fund",
         ("That keeps the whole thing outside Anexo II da Res. CVM 175: no change to the "
          "regulamento, no assembleia, no fee at fund level, no CVM filing. One director signs.")),
        ("The ask is the tape",
         "Not a meeting, not a mandate, not a price. One file, position by position."),
        ("", ""),
        ("HOW THE TABS WORK", ""),
        ("Call order", ("The 15 houses ranked by how fast each can say yes, not by size. Green "
          "rows are the first three calls.")),
        ("Funds", ("All 25 funds with the book cut four ways, so you can answer any question "
          "about a specific fund without leaving the sheet.")),
        ("Scripts", "The Portuguese opening for each house, ready to read aloud."),
        ("Buyers", ("The 17 named firms, what each buys, the smallest cheque it will write and "
          "who signs. Sourced from desk research; nobody has been approached.")),
        ("", ""),
        ("TWO THINGS TO KNOW BEFORE YOU DIAL", ""),
        ("Three houses have no buyer yet",
         ("Augme, Fram and Utility report no recourse to the cedente at all, so a buyer has to "
          "underwrite the DEBTOR. Almost every firm we found underwrites ORIGINATORS. Paramis is "
          "the only crossover. That is a gap in our research, not proof the market is empty - but "
          "do not walk into those three implying we have a bid.")),
        ("The single-cotista claim is weak",
         ("The senior quota-holder field is empty for all 25 funds. Where a row says one holder "
          "that is the subordinada count, and it is empty for ten more. Do not build a "
          "one-person-assembleia argument on it without reading the regulamento.")),
    ]
    r = 4
    for k, v in blocks:
        if k and not v:
            ws.cell(row=r, column=1, value=k).font = H2
            r += 1
            continue
        if not k:
            r += 1
            continue
        a = ws.cell(row=r, column=1, value=k)
        a.font, a.alignment = BOLD, WRAP
        b = ws.cell(row=r, column=2, value=v)
        b.font, b.alignment = BODY, WRAP
        ws.row_dimensions[r].height = max(30, 14 * (len(v) // 95 + 1))
        r += 1


def sheet_order(wb: Workbook, c: pd.DataFrame, ct: pd.DataFrame) -> None:
    ws = wb.create_sheet("Call order")
    title(
        ws,
        "Call order",
        ("Ranked by how fast a house can say yes, not by size. "
               "Green = the first three calls. Red = no named buyer for that block."),
    )
    cols = [("#", 5), ("House", 34), ("City", 17), ("Phone", 18), ("Funds", 7),
            ("Face R$m", 10), ("PDD %", 8), ("Recourse %", 11), ("Cedentes", 9), ("In RJ", 7),
            ("Performing R$m", 13), ("Who buys the performing block", 44),
            ("Distressed R$m", 13), ("Who buys the distressed block", 40),
            ("Why here", 74), ("Registered officers", 54)]
    head(ws, 4, cols)
    r = 5
    for i, x in c.iterrows():
        phone, city, socios = contact(ct, x.house)
        vals = [i + 1, x.house.title(), city, phone, int(x.funds), x.face_Rm,
                x.provision_pct, None if pd.isna(x.recourse_pct) else x.recourse_pct,
                int(x.cedentes), int(x.in_rj), x.performing_Rm,
                x.performing_buyers if isinstance(x.performing_buyers, str) and x.performing_buyers
                else "NO NAMED BUYER",
                x.distressed_Rm,
                x.distressed_buyers if isinstance(x.distressed_buyers, str) and x.distressed_buyers
                else ("NO NAMED BUYER - cheque below every floor" if x.distressed_Rm > 0 else "-"),
                x.why or "", socios]
        for j, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.font = BODY
            if j in (6, 7, 8, 11, 13):
                cell.alignment = Alignment(vertical="top", horizontal="right")
                cell.number_format = NUM if j in (6, 11, 13) else '#,##0"%"'
            elif j in (1, 5, 9, 10):
                cell.alignment = Alignment(vertical="top", horizontal="center")
            else:
                cell.alignment = WRAP
            if x["rank"] <= 3:
                cell.fill = FIRST
            elif i % 2:
                cell.fill = BAND
            if j in (12, 14) and isinstance(v, str) and v.startswith("NO NAMED"):
                cell.fill, cell.font = WARN, BOLD
        ws.row_dimensions[r].height = 74
        r += 1
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = f"A4:P{r - 1}"


def sheet_funds(wb: Workbook, c: pd.DataFrame, lp: pd.DataFrame) -> None:
    ws = wb.create_sheet("Funds")
    title(
        ws,
        "The 25 funds",
        ("The book cut four ways, per fund. All VERIFIED from the fund's own "
               "CVM Informe Mensal at competencia 2026-07. Nothing here is a price."),
    )
    cols = [("House", 30), ("Fund", 40), ("CNPJ", 20), ("Carteira R$m", 12), ("PDD R$m", 11),
            ("PDD %", 8), ("Not yet due", 12), ("Due, 1 instalment missed", 13),
            ("Overdue 1-90d", 12), ("Overdue 90-180d", 13), ("Overdue 180d+", 12),
            ("Carries recourse R$m", 14), ("True sale R$m", 12), ("Cedentes", 9), ("In RJ", 7),
            ("Signing director", 34)]
    head(ws, 4, cols)
    order = {h: i for i, h in enumerate(c.house)}
    lp = lp.assign(_o=lp.house.map(order)).sort_values(["_o", "carteira"],
                                                       ascending=[True, False])
    r, band = 5, 0
    prev = None
    for _, x in lp.iterrows():
        if x.house != prev:
            band, prev = band + 1, x.house
        pdd = 100 * x.provision / x.carteira if x.carteira else 0
        vals = [x.house.title(), short(x["name"]), x.cnpj, x.carteira / M, x.provision / M, pdd,
                x.lot_A / M, x.lot_A2 / M, x.lot_B / M, x.lot_C / M, x.lot_D / M,
                x.recourse_face / M, x.true_sale_face / M,
                int(x.cedentes_named), int(x.cedentes_in_rj), str(x.Diretor)[:60]]
        for j, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.font = MONO if j == 3 else BODY
            if 4 <= j <= 13:
                cell.alignment = Alignment(vertical="top", horizontal="right")
                cell.number_format = '#,##0"%"' if j == 6 else NUM
            elif j in (14, 15):
                cell.alignment = Alignment(vertical="top", horizontal="center")
            else:
                cell.alignment = WRAP
            if band % 2:
                cell.fill = BAND
            if j == 15 and x.cedentes_in_rj:
                cell.fill, cell.font = WARN, BOLD
        r += 1
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = f"A4:P{r - 1}"


def sheet_scripts(wb: Workbook, c: pd.DataFrame, lp: pd.DataFrame, ct: pd.DataFrame) -> None:
    ws = wb.create_sheet("Scripts")
    title(
        ws,
        "Ao telefone",
        ("The Portuguese opening for each house, in call order. Read it aloud. "
               "No price appears in any of these, and none of the forbidden words."),
    )
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 32
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 104
    head(ws, 4, [("#", 5), ("House", 32), ("Phone", 20), ("Script", 104)])
    r = 5
    for i, x in c.iterrows():
        funds = lp[lp.house == x.house].sort_values("carteira", ascending=False)
        phone, _, _ = contact(ct, x.house)
        raw = opening(x.house, funds, x)
        lines = [ln[2:].strip() for ln in raw.split("\n") if ln.startswith(">")]
        paras, buf = [], []
        for ln in lines:
            if ln:
                buf.append(ln)
            elif buf:
                paras.append(" ".join(buf))
                buf = []
        if buf:
            paras.append(" ".join(buf))
        text = "\n\n".join(p.replace("**", "") for p in paras)

        ws.cell(row=r, column=1, value=i + 1).alignment = Alignment(
            vertical="top", horizontal="center")
        ws.cell(row=r, column=2, value=x.house.title()).font = BOLD
        ws.cell(row=r, column=2).alignment = WRAP
        ws.cell(row=r, column=3, value=phone).font = MONO
        ws.cell(row=r, column=3).alignment = TOP
        cell = ws.cell(row=r, column=4, value=text)
        cell.font, cell.alignment, cell.fill = SCRIPT, WRAP, QUOTE
        ws.row_dimensions[r].height = 235
        r += 1
    ws.freeze_panes = "B5"


def sheet_buyers(wb: Workbook) -> None:
    ws = wb.create_sheet("Buyers")
    title(ws, "Who buys what",
          ("17 named firms from desk research. NOBODY HAS BEEN APPROACHED. The floor is a CHEQUE, "
           "not a face value: R$10m of deep paper at five centavos is a R$500k cheque and clears "
           "nobody. No price lives in this table - a price belongs to a calibrated buy box."))
    cols = [("Firm", 34), ("Takes lots", 12), ("Underwrites", 13),
            ("Smallest cheque R$", 15), ("Biggest cheque R$", 15),
            ("Days to a firm bid", 11), ("Who signs", 40), ("Evidence", 11), ("What we know", 86)]
    head(ws, 4, cols)
    reg = yaml.safe_load(open("config/buyer_registry.yaml", encoding="utf-8"))  # noqa: SIM115
    lot_label = {"A": "not yet due", "A2": "impaired", "B": "1-90d", "C": "90-180d",
                 "D": "180d+", "E": "RJ claims"}
    rows = sorted(reg["buyers"], key=lambda b: b["speed_days"])
    r = 5
    for i, b in enumerate(rows):
        vals = [b["name"], " · ".join(lot_label.get(x, x) for x in b["lots"]),
                b["risk"], b.get("ticket_floor_brl") or 0, b.get("ticket_ceiling_brl"),
                b["speed_days"], b["signs"], b["tag"], (b.get("note") or "").strip()]
        for j, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.font = BOLD if j == 1 else BODY
            if j in (4, 5):
                cell.alignment = Alignment(vertical="top", horizontal="right")
                cell.number_format = '#,##0;;"—"'
            elif j in (3, 6, 8):
                cell.alignment = Alignment(vertical="top", horizontal="center")
            else:
                cell.alignment = WRAP
            if i % 2:
                cell.fill = BAND
            if j == 8 and v == "ASSUMPTION":
                cell.fill = WARN
        ws.row_dimensions[r].height = max(30, 13 * (len(vals[8]) // 82 + 1))
        r += 1
    ws.freeze_panes = "B5"


def main() -> None:
    c, lp, ct = load()
    wb = Workbook()
    wb.remove(wb.active)
    sheet_start(wb, c)
    sheet_order(wb, c, ct)
    sheet_funds(wb, c, lp)
    sheet_scripts(wb, c, lp, ct)
    sheet_buyers(wb)
    wb.save(OUT)
    print(f"wrote {OUT}")
    print(f"  {len(c)} houses · {len(lp)} funds · tabs: {', '.join(wb.sheetnames)}")


if __name__ == "__main__":
    main()
