"""Build the VAZANTE target workbook from data/derived/targets_full.pkl.

Every cell is a measured fact from a public filing, so the workbook carries values rather than formulas: the
recalculation toolchain is not available in this environment, and an unevaluated formula reads as blank in most
viewers. Regenerate the inputs with scripts/screen.py first.

Usage: .venv/bin/python scripts/build_target_workbook.py
"""
import json

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = "/home/user/VAZANTE/out/VAZANTE_targets_2026-09-11.xlsx"
sub = pd.read_pickle("/home/user/VAZANTE/data/derived/targets_full.pkl")
with open("/home/user/VAZANTE/data/derived/cedentes_resolved.json", encoding="utf-8") as _f:
    cache = json.load(_f)

def tier(r):
    if r.captive_flag:
        return "X. Excluded - captive or wrong asset"
    if r.res_verdict == "possible_target":
        return "1. Verified target"
    if r.carteira >= 60e6:
        return "2. Big enough alone"
    if r.carteira >= 25e6:
        return "3. Below the floor, substantial"
    if r.n_rj >= 1 or r.n_ced >= 4:
        return "4. Deal 1 candidate"
    return "5. Worth a look"

def why(r):
    if r.captive_flag:
        if isinstance(r.res_why, str) and r.res_why:
            return r.res_why[:600]
        return "One sponsor originates the whole book, so there is nothing to decompose and the sponsor will not sell. Identified from the fund's own name."
    b = []
    if isinstance(r.res_what, str) and r.res_what:
        b.append(r.res_what[:330])
    if r.n_ced >= 5:
        b.append(f"{int(r.n_ced)} cedentes named across unrelated industries")
    elif r.n_ced >= 2:
        b.append(f"{int(r.n_ced)} unrelated cedentes named")
    elif r.n_ced == 0:
        b.append("the administrador names no cedente, so the contents cannot be seen from outside")
    if r.n_rj:
        b.append(f"{int(r.n_rj)} cedente{'s are' if r.n_rj > 1 else ' is'} in judicial recovery, so the recourse claim is real rather than theoretical")
    if pd.notna(r.cotistas) and r.cotistas and r.cotistas <= 3:
        b.append(f"only {int(r.cotistas)} quota-holder{'s' if r.cotistas > 1 else ''}, so one institution can decide")
    if pd.notna(r.max_cap) and r.max_cap >= 50e6:
        b.append(f"the largest cedente carries R${r.max_cap/1e6:,.0f}m of capital, so recourse runs against someone solvent")
    if pd.notna(r.cart_24m) and r.cart_24m and r.carteira / r.cart_24m - 1 > 0.25:
        b.append("the carteira is still growing, so the manager has not given up and willingness will be hard")
    import re as _re
    if _re.search(r"PESSOAL|CONSIGN|CART[AÃ]O|CREDI[AÁ]RIO|VAREJO", str(r.DENOM_SOCIAL).upper()):
        b.append("CHECK THIS: the fund's own name says consumer credit while the CVM segment table says commercial. "
                 "One of the two is wrong and the name is the stronger signal, so treat it as consumer until the "
                 "regulamento says otherwise")
    return ". ".join(x[0].upper() + x[1:] for x in b) + "."

def check(r):
    if r.captive_flag:
        return "None. Excluded."
    if r.n_ced == 0:
        return "Fundos.NET: the regulamento for the disposal-authority and coobrigacao clauses, and the last two demonstracoes contabeis for the auditor's view on the lastro. The fund names no cedente, so nothing else will tell you what is inside."
    if r.n_rj:
        return "Pull the judicial recovery dockets on the cedentes in recovery, and read the termo de cessao for a personal aval from the socios. Since December 2025 the STJ holds that judicial recovery does not suspend action against guarantors, which is what makes the claim worth paying for."
    return "Fundos.NET: twelve months of atas, fatos relevantes and comunicados, looking for a class closed for redemptions. That is the art. 44 paragraph 3 trigger and the best willingness signal there is."

sub["Tier"] = sub.apply(tier, axis=1)
sub["Why"] = sub.apply(why, axis=1)
sub["Check"] = sub.apply(check, axis=1)
sub["Researched"] = np.where(sub.res_verdict.notna(), "Yes - desk research done", "Not yet researched")
o = {"1. Verified target": 0, "2. Big enough alone": 1, "3. Below the floor, substantial": 2,
     "4. Deal 1 candidate": 3, "5. Worth a look": 4, "X. Excluded - captive or wrong asset": 5}
sub["_o"] = sub.Tier.map(o)
sub = sub.sort_values(["_o", "carteira"], ascending=[True, False]).reset_index(drop=True)
sub.insert(0, "Rank", range(1, len(sub) + 1))

A = "Arial"
TITLE = Font(name=A, size=18, bold=True, color="1F3864")
SUBF = Font(name=A, size=11, color="404040")
HDR = Font(name=A, size=12, bold=True, color="FFFFFF")
BODY = Font(name=A, size=11)
BOLD = Font(name=A, size=11, bold=True)
H2 = Font(name=A, size=14, bold=True, color="1F3864")
FILL_H = PatternFill("solid", fgColor="1F3864")
BAND = PatternFill("solid", fgColor="F2F5FB")
FT = {"1. Verified target": PatternFill("solid", fgColor="C6E0B4"),
      "2. Big enough alone": PatternFill("solid", fgColor="D9E2F3"),
      "3. Below the floor, substantial": PatternFill("solid", fgColor="E7EEF8"),
      "4. Deal 1 candidate": PatternFill("solid", fgColor="FFF2CC"),
      "5. Worth a look": None,
      "X. Excluded - captive or wrong asset": PatternFill("solid", fgColor="EDEDED")}
thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()

def head(ws, row, cols):
    for i, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = HDR; c.fill = FILL_H; c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[row].height = 48

# ---------------------------------------------------------------- Targets
ws = wb.active; ws.title = "Targets"
ws["A1"] = "VAZANTE - funds to go after"; ws["A1"].font = TITLE
ws.row_dimensions[1].height = 28
ws["A2"] = ("Every FIDC class filing with the CVM at competencia July 2026 that carries business-to-business paper, a provision that "
            "jumped rather than sat still, and no visible captive sponsor. Built 11 September 2026 from CVM open data; cedente names "
            "resolved through the Receita. Sorted best first. Nothing here has been contacted and no price appears anywhere.")
ws["A2"].font = SUBF; ws["A2"].alignment = WRAP
ws.merge_cells("A2:U2"); ws.row_dimensions[2].height = 42

COLS = [("Rank", 6), ("Tier", 22), ("Researched", 17), ("Fund", 44), ("CNPJ", 20), ("Orphan lineage", 13),
        ("Carteira R$m", 12), ("PL R$m", 10), ("Provision % of carteira", 12),
        ("Rise above 24m low (pp)", 12), ("Over 180 days %", 11), ("B2B paper %", 11),
        ("Cedentes named", 11), ("In judicial recovery", 12), ("Largest cedente capital R$m", 14),
        ("Quota-holders", 11), ("Administrador", 32), ("Gestor", 28), ("Diretor responsavel", 24),
        ("What it is and why it is here", 76), ("Cheapest next check", 62), ("Cedentes named", 66)]
head(ws, 4, [c[0] for c in COLS])
for i, (_, w) in enumerate(COLS, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

r = 5
for _, x in sub.iterrows():
    f = FT.get(x.Tier)
    vals = [x.Rank, x.Tier, x.Researched, x.DENOM_SOCIAL, x.CNPJ_FUNDO_CLASSE,
            (x.lineage if isinstance(x.lineage, str) and x.lineage else "-"),
            round(x.carteira / 1e6, 1), round(x.pl / 1e6, 1),
            round(float(x.pdd_share_carteira) * 100, 1) if pd.notna(x.pdd_share_carteira) else None,
            round(float(x.pdd_rise_from_trough) * 100, 1) if pd.notna(x.pdd_rise_from_trough) else None,
            round(float(x.inad_180_share) * 100, 1) if pd.notna(x.inad_180_share) else None,
            round(float(x.b2b_share) * 100, 0) if pd.notna(x.b2b_share) else None,
            int(x.n_ced), int(x.n_rj),
            round(x.max_cap / 1e6, 1) if pd.notna(x.max_cap) else None,
            int(x.cotistas) if pd.notna(x.cotistas) else None,
            x.Administrador, x.Gestor, x.Diretor, x.Why, x.Check, x.ced_names or "(none named)"]
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=i, value=v)
        c.font = BOLD if i == 4 else BODY
        c.border = BOX
        if i in (2, 3, 4, 17, 18, 19, 20, 21, 22):
            c.alignment = WRAP
        elif i in (7, 8, 9, 10, 11, 12, 15):
            c.alignment = Alignment(vertical="top", horizontal="right"); c.number_format = '#,##0.0;(#,##0.0);-'
        else:
            c.alignment = Alignment(vertical="top", horizontal="center")
        if f:
            c.fill = f
    ws.row_dimensions[r].height = 92
    r += 1
LAST = r - 1
ws.freeze_panes = "G5"
ws.auto_filter.ref = f"A4:V{LAST}"

s = LAST + 2
ws.cell(row=s, column=1, value="Summary").font = H2
nc = sub[~sub.captive_flag]
summary = [("Funds listed", len(sub)),
           ("Verified targets (desk research done)", int((sub.Tier.str.startswith("1.")).sum())),
           ("Big enough to carry a trade alone", int((sub.Tier.str.startswith("2.")).sum())),
           ("Right shape, below the R$60m floor", int((sub.Tier.str.startswith(("3.","4."))).sum())),
           ("Deal 1 candidates", int((sub.Tier.str.startswith("4.")).sum())),
           ("Excluded as captive or wrong asset", int(sub.captive_flag.sum())),
           ("Funds with a cedente in judicial recovery", int((nc.n_rj > 0).sum())),
           ("Combined carteira of everything not excluded (R$m)", round(nc.carteira.sum() / 1e6, 1)),
           ("Combined carteira of tiers 1 and 2 (R$m)", round(sub[sub.Tier.str.startswith(("1.", "2."))].carteira.sum() / 1e6, 1))]
for j, (k, v) in enumerate(summary):
    a = ws.cell(row=s + 1 + j, column=1, value=k); a.font = BODY
    ws.merge_cells(start_row=s + 1 + j, start_column=1, end_row=s + 1 + j, end_column=6)
    b = ws.cell(row=s + 1 + j, column=7, value=v); b.font = BOLD; b.fill = BAND; b.border = BOX
    b.number_format = '#,##0.0' if isinstance(v, float) else '#,##0'

n = s + len(summary) + 2
ws.cell(row=n, column=1, value=("No price appears in this workbook by design. Under the desk's own rules a bid exists only once a seller tape "
                                "has been verified and three firm onward exits cover the all-in basis, tax included, by 1.20 times.")).font = SUBF
ws.merge_cells(start_row=n, start_column=1, end_row=n, end_column=22)
ws.cell(row=n, column=1).alignment = WRAP; ws.row_dimensions[n].height = 30

# ---------------------------------------------------------------- Cedentes
w2 = wb.create_sheet("Cedentes")
w2["A1"] = "Who owes the money"; w2["A1"].font = TITLE; w2.row_dimensions[1].height = 28
w2["A2"] = ("Every cedente named in the informe, resolved through the Receita. A cedente in judicial recovery is what makes a recourse "
            "claim worth paying for. Capital matters: the same claim against a company with R$200,000 of capital and one with R$70m are "
            "not the same asset. Rows shaded pink are in judicial recovery.")
w2["A2"].font = SUBF; w2["A2"].alignment = WRAP; w2.merge_cells("A2:H2"); w2.row_dimensions[2].height = 42
C2 = [("Fund", 42), ("Tier", 22), ("Cedente CNPJ", 18), ("Razao social", 46), ("Activity", 40),
      ("Capital R$m", 12), ("Location", 24), ("Status", 26)]
head(w2, 4, [c[0] for c in C2])
for i, (_, w) in enumerate(C2, 1):
    w2.column_dimensions[get_column_letter(i)].width = w
rr = 5
for _, x in sub.iterrows():
    if not isinstance(x.ceds, list) or not x.ceds:
        continue
    for cn in x.ceds:
        j = cache.get(cn, {})
        rz = j.get("razao_social") or "(unresolved)"
        rj = "RECUPERA" in rz.upper()
        sit = j.get("descricao_situacao_cadastral", "?")
        status = "In judicial recovery" if rj else ("Active" if sit == "ATIVA" else str(sit).title())
        if rj and sit != "ATIVA":
            status = f"In judicial recovery, {str(sit).lower()}"
        vals = [x.DENOM_SOCIAL, x.Tier, cn,
                rz.replace("EM RECUPERACAO JUDICIAL", "").replace("- EM RECUPERACAO JUDICIAL", "").strip(),
                j.get("cnae_fiscal_descricao") or "?", round(float(j.get("capital_social") or 0) / 1e6, 3),
                f"{j.get('municipio','?')}/{j.get('uf','?')}", status]
        for i, v in enumerate(vals, 1):
            c = w2.cell(row=rr, column=i, value=v)
            c.font = BODY; c.border = BOX
            c.alignment = WRAP if i in (1, 2, 4, 5) else Alignment(vertical="top")
            if i == 6:
                c.number_format = '#,##0.000;(#,##0.000);-'; c.alignment = Alignment(vertical="top", horizontal="right")
            if rj:
                c.fill = PatternFill("solid", fgColor="FCE4E4")
        w2.row_dimensions[rr].height = 34
        rr += 1
w2.freeze_panes = "C5"; w2.auto_filter.ref = f"A4:H{rr-1}"
w2.cell(row=rr + 1, column=1, value="Cedentes named in total").font = BOLD
w2.cell(row=rr + 1, column=3, value=rr - 5).font = BOLD
w2.cell(row=rr + 2, column=1, value="Of which in judicial recovery").font = BOLD
w2.cell(row=rr + 2, column=3, value=int(sub.n_rj.sum())).font = BOLD

# ---------------------------------------------------------------- Clusters
w3 = wb.create_sheet("Clusters")
w3["A1"] = "The clusters - one conversation, several funds"; w3["A1"].font = TITLE; w3.row_dimensions[1].height = 28
w3["A2"] = ("Broken books concentrate under a few managers. This matters because almost no single small vehicle clears the R$60m floor "
            "on its own, but a bundle does, and a manager holding several books of one kind has one decision to make rather than four. "
            "Excluded captive funds are left out of these totals.")
w3["A2"].font = SUBF; w3["A2"].alignment = WRAP; w3.merge_cells("A2:F2"); w3.row_dimensions[2].height = 42
start = 5
for label, key in [("By gestora", "Gestor"), ("By administrador", "Administrador")]:
    w3.cell(row=start - 1, column=1, value=label).font = H2
    head(w3, start, [key, "Funds", "Combined carteira R$m", "Largest single fund R$m",
                     "Funds with a cedente in recovery", "The vehicles"])
    g = (nc.groupby(key).agg(funds=("Rank", "size"), tot=("carteira", "sum"), mx=("carteira", "max"),
                             rj=("n_rj", lambda s: int((s > 0).sum())),
                             names=("DENOM_SOCIAL", lambda s: " | ".join(n[:38] for n in s)))
         .sort_values("tot", ascending=False))
    g = g[g.funds >= 2]
    rw = start + 1
    for name, x in g.iterrows():
        for i, v in enumerate([name, int(x.funds), round(x.tot / 1e6, 1), round(x.mx / 1e6, 1), x.rj, x.names], 1):
            c = w3.cell(row=rw, column=i, value=v)
            c.font = BOLD if i == 1 else BODY; c.border = BOX
            if i in (3, 4):
                c.alignment = Alignment(vertical="top", horizontal="right"); c.number_format = '#,##0.0'
            else:
                c.alignment = WRAP if i in (1, 6) else Alignment(vertical="top", horizontal="center")
        w3.row_dimensions[rw].height = 42
        rw += 1
    for i, w in enumerate([34, 9, 16, 16, 14, 76], 1):
        w3.column_dimensions[get_column_letter(i)].width = w
    start = rw + 3
w3.freeze_panes = "B5"

# ---------------------------------------------------------------- Method
w4 = wb.create_sheet("How to read this")
w4["A1"] = "How to read this"; w4["A1"].font = TITLE; w4.row_dimensions[1].height = 28
w4.column_dimensions["A"].width = 42; w4.column_dimensions["B"].width = 108
blocks = [
 ("What the tiers mean",
  ("Tier 1 is a fund a researcher has checked against the public record and not been able to disqualify. Tier 2 is big enough to "
  "carry a trade on its own but has not been researched yet. Tier 3 is the right shape and too small alone, which makes it the "
  "natural first trade: the business case wants a first deal small enough that losing all of it costs less than the tax opinion. "
  "Tier 4 is worth a look. Tier X is excluded, and the reason is in the same row.")),
 ("Where the numbers come from",
  ("Every FIDC Informe Mensal filed with the CVM, 44 months from January 2023 to August 2026, 5,376 fund classes. The last complete "
  "month is July 2026, because the August window was still open when this was built. Cedente identities come from the Receita. "
  "All of it is public and free. Every figure in this workbook is a measurement, not a projection.")),
 ("The filters, in order",
  ("From 4,321 FIDC classes filing in July 2026: provision at least 25 percent of the carteira, leaving 420; business-to-business "
  "paper at least 60 percent, leaving 94; no material retail consumer credit, 91; the provision rose at least 10 points above its "
  "own 24-month low, 85; no named cedente above half of PL, 47; carteira of at least R$5m, 36.")),
 ("Why retail had to come out",
  ("The CVM's commercial category includes varejo, which is retail consumer credit. It was 35 percent of the commercial face in the "
  "first version of this list and put a R$3.7bn retailer's own store-credit book at the top. A 35 percent provision on a consumer "
  "book is the normal expected loss of that business, not distress.")),
 ("Why the provision has to have jumped, and measured against its own low",
  ("Some strategies carry a high provision permanently by design, so testing the level catches business models rather than events. "
  "But a twelve-month difference misses a book that broke eighteen months ago and has been flat since. Daniele Multiplo rose 21.7 "
  "points over 24 months and fell 1.3 over the last 12; a twelve-month test dropped it, and it is now the largest genuine target "
  "on the list. The test is therefore the rise above the lowest point in the previous 24 months.")),
 ("The captive problem, which is not solved",
  ("A captive fund is one where a single sponsor originates the whole book. There is nothing to decompose and the sponsor will not "
  "sell. Where the administrador names cedentes, one above half of PL gives it away. But naming is a reporting habit rather than a "
  "property of the book: it runs from zero percent of classes at some administrators to 95 percent at others, and only 44 percent "
  "of the population names anyone at all. Where nobody is named a captive book is invisible, and only the fund's name or desk "
  "research finds it. Two of the largest names on the first version of this list were captive and were caught by research, not by "
  "the screen. Sponsors also rename funds off their own name: Agro Capital Finance was FIDC Albaugh I until December 2025.")),
 ("What is still missing, and it is the biggest thing",
  ("Willingness. Everything here passes on paper, size and provision. Nothing in the CVM data says whether the person holding the "
  "pen will crystallise a loss. The best proxy is a class closed for redemptions for more than five business days, which needs "
  "Fundos.NET and is not built. Expect it to remove most of this list.")),
 ("A correction to the method the business case uses",
  ("The business case leans on a suspiciously smooth senior quota return as one of the three sentences that buy exclusivity. "
  "Measured across the whole population, a smooth return fires on 19 percent of funds heading for trouble and 29 percent of healthy "
  "ones. The opposite reading, a return that has stopped, is no better at 42 against 55. The field carries no signal in either "
  "direction and should come out of the script.")),
 ("Why there are no formulas in this workbook",
  ("Every number here is a measured fact from a public filing rather than a modelled one, so there is nothing to recalculate. The "
  "recalculation toolchain in the environment that built this file could not run, so live formulas were deliberately not used: a "
  "formula that has never been evaluated shows as blank in many viewers, and a blank is worse than a number.")),
 ("How to reproduce it",
  ("In the VAZANTE repository, scripts/screen.py rebuilds this list from the raw CVM files and scripts/backtest_report.py scores the "
  "detection rule. The written version is docs/TARGETS.md and the method corrections are in docs/FINDINGS_2026-09-11.md.")),
]
rw = 4
for h, b in blocks:
    a = w4.cell(row=rw, column=1, value=h); a.font = Font(name=A, size=12, bold=True, color="1F3864")
    a.alignment = WRAP; a.fill = BAND; a.border = BOX
    c = w4.cell(row=rw, column=2, value=b); c.font = BODY; c.alignment = WRAP; c.border = BOX
    w4.row_dimensions[rw].height = max(50, 14 * (len(b) // 98 + 1))
    rw += 1


# ---------------------------------------------------------------- Start here
w0 = wb.create_sheet("Start here", 0)
w0.column_dimensions["A"].width = 4
w0.column_dimensions["B"].width = 52
w0.column_dimensions["C"].width = 16
w0.column_dimensions["D"].width = 16
w0.column_dimensions["E"].width = 62
w0.sheet_view.showGridLines = False

BIG = Font(name=A, size=40, bold=True, color="1F3864")
LBL = Font(name=A, size=13, color="404040")

w0["B2"] = "VAZANTE - how many funds can we attack"
w0["B2"].font = TITLE
w0.row_dimensions[2].height = 30
w0["B3"] = "Every FIDC filing with the CVM at competencia July 2026, screened and researched. Built 11 September 2026."
w0["B3"].font = SUBF
w0.merge_cells("B3:E3")

live = sub[~sub.captive_flag]
w0["B5"] = str(len(live)); w0["B5"].font = BIG
w0.row_dimensions[5].height = 52
w0["C5"] = "funds you can attack"; w0["C5"].font = LBL
w0["C5"].alignment = Alignment(vertical="center")
w0.merge_cells("C5:E5")

ngest = live.Gestor.nunique()
w0["B6"] = str(ngest); w0["B6"].font = BIG
w0.row_dimensions[6].height = 52
w0["C6"] = "conversations, because several funds share one gestora"; w0["C6"].font = LBL
w0["C6"].alignment = Alignment(vertical="center")
w0.merge_cells("C6:E6")

r0 = 8
w0.cell(row=r0, column=2, value="How the 4,321 FIDCs narrow down").font = H2
funnel = [
    ("FIDC classes filing with the CVM in July 2026", 4321),
    ("Provision at or above 25% of the carteira, so the loss is already booked", 420),
    ("Business-to-business paper, industrial plus commercial, at least 60%", 94),
    ("No material retail consumer credit", 91),
    ("The provision jumped at least 10 points above its own 24-month low", 85),
    ("No named cedente above half of the fund's equity", 47),
    ("Carteira of at least R$5m", len(sub)),
    ("Minus the captive sponsor books, found by research and by fund name", len(live)),
]
for j, (lbl, n) in enumerate(funnel):
    a = w0.cell(row=r0 + 1 + j, column=2, value=lbl); a.font = BODY; a.alignment = WRAP
    w0.merge_cells(start_row=r0 + 1 + j, start_column=2, end_row=r0 + 1 + j, end_column=4)
    b = w0.cell(row=r0 + 1 + j, column=5, value=n)
    b.font = BOLD if j == len(funnel) - 1 else BODY
    b.number_format = '#,##0'; b.border = BOX
    b.alignment = Alignment(horizontal="left", vertical="center")
    if j == len(funnel) - 1:
        b.fill = PatternFill("solid", fgColor="C6E0B4")
    w0.row_dimensions[r0 + 1 + j].height = 22

r1 = r0 + len(funnel) + 3
w0.cell(row=r1, column=2, value="By size, and why the clusters matter").font = H2
bands = [("R$60m and above - can carry a trade alone", live[live.carteira >= 60e6]),
         ("R$25m to R$60m - needs bundling", live[(live.carteira >= 25e6) & (live.carteira < 60e6)]),
         ("Under R$25m - the natural first trade", live[live.carteira < 25e6])]
head(w0, r1 + 1, ["", "Size band", "Funds", "Carteira R$m", "Why it matters"])
for j, (lbl, dfb) in enumerate(bands):
    rw = r1 + 2 + j
    c = w0.cell(row=rw, column=2, value=lbl); c.font = BODY; c.alignment = WRAP; c.border = BOX
    n = w0.cell(row=rw, column=3, value=len(dfb)); n.font = BOLD; n.border = BOX
    n.alignment = Alignment(horizontal="center")
    v = w0.cell(row=rw, column=4, value=round(dfb.carteira.sum() / 1e6, 0)); v.font = BODY; v.border = BOX
    v.number_format = '#,##0'; v.alignment = Alignment(horizontal="right")
    note = ["Only these four are a trade on their own.",
            "Below the R$60m floor alone, but a bundle from one gestora clears it.",
            "Small enough to be the first trade, which is what the business case asks for."][j]
    t_ = w0.cell(row=rw, column=5, value=note); t_.font = BODY; t_.alignment = WRAP; t_.border = BOX
    w0.row_dimensions[rw].height = 32

r2 = r1 + len(bands) + 4
w0.cell(row=r2, column=2, value="Start with these").font = H2
head(w0, r2 + 1, ["", "Fund", "Carteira R$m", "Gestora", "Why it leads"])
lead_notes = {
    0: "Largest, and the only one checked against the public record without being disqualified. Sourced by a factoring house barred from selling its own credits.",
    1: "Two quota-holders, so one institution decides. One cedente already in judicial recovery, so the recourse claim is real.",
    2: "One cedente in judicial recovery. Same gestora as three others, so one call reaches four funds.",
    3: "Clears the floor on its own. Not yet researched.",
    4: "Five cedentes named, which is what a genuine multicedente book looks like.",
}
for j, (_, x) in enumerate(live.sort_values("carteira", ascending=False).head(5).iterrows()):
    rw = r2 + 2 + j
    c = w0.cell(row=rw, column=2, value=x.DENOM_SOCIAL[:58]); c.font = BOLD; c.alignment = WRAP; c.border = BOX
    v = w0.cell(row=rw, column=3, value=round(x.carteira / 1e6, 0)); v.font = BODY; v.border = BOX
    v.number_format = '#,##0'; v.alignment = Alignment(horizontal="right")
    g_ = w0.cell(row=rw, column=4, value=str(x.Gestor)[:30]); g_.font = BODY; g_.alignment = WRAP; g_.border = BOX
    n_ = w0.cell(row=rw, column=5, value=lead_notes.get(j, "")); n_.font = BODY; n_.alignment = WRAP; n_.border = BOX
    w0.row_dimensions[rw].height = 44

r3 = r2 + 8
notes = [
    ("The one caveat that matters",
     ("Willingness is untested. Every fund here passes on paper, size and provision, but nothing in the CVM data says whether "
     "the person holding the pen will crystallise a loss. Expect roughly seven in ten to die there. Twenty-five funds gets you "
     "to about seven or eight trades against a plan that needs six to ten, so it works with no margin.")),
    ("What the other tabs hold",
     ("Targets is all 36 funds including the 11 excluded, with the reason on each row. Who to call has the telephone, "
     "city and registered officers of every gestora and administrador. Cedentes names who owes the money and flags those "
     "in judicial recovery. Clusters shows which gestoras hold more than one fund. How to read this covers the method.")),
    ("The orphaned estates are not a separate opportunity",
     ("780 FIDC classes were orphaned when Trustee, Banvox, Master, CBSF, Sefer and Reag failed. 531 still file. Seventy percent "
     "of their R$118bn is financial-sector paper the desk cannot resell, and the nine worth having are already in this list, "
     "marked in the Orphan lineage column. There is no bulk trade with a receiver.")),
]
for h, b in notes:
    a = w0.cell(row=r3, column=2, value=h); a.font = Font(name=A, size=12, bold=True, color="1F3864")
    a.alignment = WRAP; a.fill = BAND; a.border = BOX
    c = w0.cell(row=r3, column=3, value=b); c.font = BODY; c.alignment = WRAP; c.border = BOX
    w0.merge_cells(start_row=r3, start_column=3, end_row=r3, end_column=5)
    w0.row_dimensions[r3] = w0.row_dimensions[r3]
    w0.row_dimensions[r3].height = max(46, 13 * (len(b) // 105 + 1))
    r3 += 1


# ---------------------------------------------------------------- Who to call
import pandas as _pd

_ct = _pd.read_pickle("/home/user/VAZANTE/data/derived/contacts.pkl")
w5 = wb.create_sheet("Who to call")
w5["A1"] = "Who to call"; w5["A1"].font = TITLE; w5.row_dimensions[1].height = 28
w5["A2"] = ("Every gestora and administrador behind the funds you can attack, sorted by how much carteira each one reaches. "
            "Telephone, city, CNPJ and the registered officers all come from the Receita, which is public. Where two "
            "entities share a switchboard or two or more officers they are marked as one house: calling either reaches "
            "both roles. No one here has been contacted.")
w5["A2"].font = SUBF; w5["A2"].alignment = WRAP; w5.merge_cells("A2:J2"); w5.row_dimensions[2].height = 46
C5 = [("Role", 14), ("House", 10), ("Name", 42), ("Funds", 8), ("Carteira reached R$m", 13), ("Telephone", 15),
      ("City", 22), ("CNPJ", 19), ("Registered officers", 62), ("The funds they hold", 60)]
head(w5, 4, [c[0] for c in C5])
for i, (_, w) in enumerate(C5, 1):
    w5.column_dimensions[get_column_letter(i)].width = w
_ct = _ct.sort_values("carteira_Rm", ascending=False)
rw5 = 5
for _, x in _ct.iterrows():
    tel = str(x.phone)
    tel = f"+55 {tel[:2]} {tel[2:6]}-{tel[6:]}" if len(tel) == 10 else (f"+55 {tel[:2]} {tel[2:7]}-{tel[7:]}" if len(tel) == 11 else tel)
    cn = str(x.cnpj)
    cn = f"{cn[:2]}.{cn[2:5]}.{cn[5:8]}/{cn[8:12]}-{cn[12:]}" if len(cn) == 14 else cn
    vals = [x.role, x.house or "-", x["name"], int(x.funds), round(x.carteira_Rm, 1), tel,
            x.city, cn, x.socios, x.fund_list]
    for i, v in enumerate(vals, 1):
        c = w5.cell(row=rw5, column=i, value=v)
        c.font = BOLD if i == 3 else BODY
        c.border = BOX
        if i == 5:
            c.number_format = '#,##0.0'; c.alignment = Alignment(vertical="top", horizontal="right")
        elif i in (3, 9, 10):
            c.alignment = WRAP
        else:
            c.alignment = Alignment(vertical="top", horizontal="center" if i in (2, 4) else "left")
        if x.role == "Gestora":
            c.fill = PatternFill("solid", fgColor="EAF1DD")
    w5.row_dimensions[rw5].height = 46
    rw5 += 1
w5.freeze_panes = "D5"
w5.auto_filter.ref = f"A4:J{rw5-1}"

_n = rw5 + 1
for _h, _b in [
    ("Read the gestora rows first",
     ("The gestora decides what the fund does with its carteira and the administrador signs. Both matter, but the "
     "gestora is the conversation. Gestora rows are shaded green.")),
    ("Three names you already know",
     ("Fram Capital manages one of these funds and is on your own buyer list as a Premium buyer, already emailed. BRZ "
     "Gestao manages another and is a named deal in your book. Solis manages the largest fund on the list, and the "
     "business case says to skip committee-heavy houses for the first few deals.")),
    ("Four pairs are really one house each",
     ("Finaxis and Petra share three officers. Actual and Libertas share a switchboard and two officers, and between "
     "them touch seven fund slots. Intra DTVM and Intra Black share a switchboard. Oliveira Trust DTVM and Oliveira "
     "Trust Servicer share five officers.")),
    ("What is missing",
     ("The Receita publishes a switchboard, not a direct line, and no email for any of these. The named officers are "
     "the registered partners, which is who to ask for. The diretor responsavel for each specific fund is in the "
     "Targets tab, and that is the person who signs.")),
]:
    a = w5.cell(row=_n, column=1, value=_h); a.font = Font(name=A, size=12, bold=True, color="1F3864")
    a.alignment = WRAP; a.fill = BAND; a.border = BOX
    w5.merge_cells(start_row=_n, start_column=1, end_row=_n, end_column=3)
    c = w5.cell(row=_n, column=4, value=_b); c.font = BODY; c.alignment = WRAP; c.border = BOX
    w5.merge_cells(start_row=_n, start_column=4, end_row=_n, end_column=10)
    w5.row_dimensions[_n].height = max(40, 13 * (len(_b) // 110 + 1))
    _n += 1

for s_ in wb.worksheets:
    s_.sheet_view.showGridLines = False
wb.save(OUT)
print("wrote", OUT)
print(f"{len(sub)} funds | {rr-5} cedente rows | {int(sub.captive_flag.sum())} excluded")
