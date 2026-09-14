"""Build the email pack: one Portuguese email per house, as a Word document.

Fifteen emails, not twenty-five. A house with four funds has one man who signs
for all four; sending him four emails would read as a mail-merge and lose the
house. Each email names every fund he manages and leads on the largest.

The body is written to be selected and pasted straight into an email client, so
each one is plain paragraphs — no tables, no boxes, nothing that survives a copy
badly.

No price appears anywhere. None of laudo, parecer, auditoria, avaliacao or
mandato appears anywhere. Operating rules 1 and 2: these are drafts, and a
partner sends them.

    .venv/bin/python -m scripts.build_email_pack
"""

from __future__ import annotations

import pandas as pd
from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Pt, RGBColor

from scripts.build_call_workbook import PRIORITY, _ascii, contact
from scripts.call_sheet_md import short

OUT = "/home/user/VAZANTE/out/VAZANTE_emails_2026-09-14.docx"
M = 1_000_000.0
INK = RGBColor(0x14, 0x1E, 0x28)
OCHRE = RGBColor(0x9C, 0x63, 0x18)
GREY = RGBColor(0x6B, 0x78, 0x85)
RED = RGBColor(0x9C, 0x3A, 0x3D)


def brl(v: float) -> str:
    """R$ 17 milhoes / R$ 1 milhao — Portuguese needs the singular."""
    n = round(v / M)
    if n >= 2:
        return f"R$ {n} milhões".replace(",", ".")
    if n == 1:
        return "R$ 1 milhão"
    return f"R$ {v / 1000:,.0f} mil".replace(",", ".")


def cased(name: str) -> str:
    """ALEXANDRE LODI DE OLIVEIRA -> Alexandre Lodi de Oliveira."""
    small = {"de", "da", "do", "dos", "das", "e"}

    def cap(w: str) -> str:
        # Sant'ana -> Sant'Ana, d'oro -> D'Oro
        return "'".join(part.capitalize() for part in w.split("'"))

    parts = str(name).strip().lower().split()
    return " ".join(p if p in small and i else cap(p) for i, p in enumerate(parts))


def body(house: str, funds: pd.DataFrame, row: pd.Series) -> tuple[str, list[str]]:
    """Return (subject, paragraphs). The second paragraph is the proof of work."""
    lead = funds.iloc[0]
    nm = short(lead["name"])
    a, d, b90 = lead.lot_A, lead.lot_D, lead.lot_B
    many = len(funds) > 1
    names = ", ".join(short(x["name"]) for x in [r for _, r in funds.iterrows()])

    scope = (f"dos {len(funds)} fundos que vocês gerem — {names}" if many
             else f"do {nm}")

    # The contrast only works when both sides exist. Where the book has nothing
    # left un-matured, or nothing deeply overdue, say the true thing instead.
    if a <= 0 and d > 0:
        proof = (f"No {nm} não há mais nada a vencer: a carteira inteira já venceu, e "
                 f"{brl(d)} passaram de 180 dias. Mesmo dentro disso há pedaços muito "
                 f"diferentes entre si, e cada um tem um comprador diferente.")
    elif d <= 0 and a > 0:
        venc = "vencido" if round(b90 / M) == 1 else "vencidos"
        proof = (f"O {nm} reporta {brl(a)} a vencer e {brl(b90)} {venc} há menos de "
                 f"90 dias. São dois ativos diferentes: a casa que compra um não é a "
                 f"casa que compra o outro.")
    else:
        venc = "vencido" if round(d / M) == 1 else "vencidos"
        proof = (f"O {nm} reporta {brl(a)} a vencer e {brl(d)} {venc} há mais de 180 "
                 f"dias. São dois ativos diferentes: a casa que compra um não é a casa "
                 f"que compra o outro.")
        if many:
            proof += " Os outros fundos se dividem da mesma forma."

    # The subject has to match what the body actually says.
    if a <= 0 and d > 0:
        subject = f"{nm} — a carteira vencida, em partes"
    elif many:
        others = len(funds) - 1
        subject = (f"{nm} e os outros {others} FIDCs — os dois lados da carteira"
                   if others > 1 else f"{nm} e o {short(funds.iloc[1]['name'])} — "
                                      "os dois lados da carteira")
    else:
        subject = f"{nm} — os dois lados da carteira"
    paras = [
        f"Li os informes mensais de julho {scope}.",
        proof,
        ("É isso que a Sutphin faz. Cortamos a carteira em lotes por tipo de risco, "
         "levamos cada lote a quem compra aquele risco específico e conduzimos uma "
         "rodada competitiva com prazo. Não compramos nada e não ficamos com o "
         "dinheiro — o comprador paga o fundo diretamente."),
        ("Se algo tiver de liquidar ainda dentro deste exercício, a rodada precisa "
         "começar nas próximas semanas. É aritmética, não pressão."),
        ("Quinze minutos esta semana? Se preferir, mando uma página com o que "
         "precisaríamos olhar."),
    ]
    return subject, paras


def para(doc, text, *, size=11, bold=False, color=INK, space=6, italic=False, align=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size, r.font.bold, r.font.italic = Pt(size), bold, italic
    r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space)
    if align:
        p.alignment = align
    return p


def cover(doc, c: pd.DataFrame) -> None:
    para(doc, "VAZANTE", size=26, bold=True, space=2)
    para(doc, "Fifteen emails, ready to send", size=15, color=OCHRE, space=14)
    para(doc, f"14 September 2026 · {len(c)} houses · 25 funds · nobody has been contacted",
         size=10, color=GREY, space=18)

    para(doc, "How to use this", size=14, bold=True, space=8)
    for t in [
        ("One email per page. Scroll to the one you want, select from the subject line "
         "down to the signature, copy, paste into your mail client. Nothing in the "
         "copyable block is a table, so it will paste cleanly."),
        ("Fifteen emails, not twenty-five. Where a house manages four funds, one man "
         "signs for all four — four separate emails to the same person would read as a "
         "mail-merge and lose the house. Each email names every fund and leads on the "
         "largest."),
        ("They are in call order, not size order. Libertas/Actual is first because the "
         "same two officers sign the gestora and the administrador, so there is no "
         "second party to convince."),
        ("Send them one at a time, by hand, over several days. Fifteen emails is not a "
         "campaign, and a sequencing tool leaves fingerprints this audience notices."),
    ]:
        para(doc, "•  " + t, size=10.5, space=6)

    para(doc, "Before you send anything", size=14, bold=True, space=8)
    for t in [
        ("No price. Not a range, not an example, not in a reply. If asked, the answer "
         "is that a price comes out of a competitive round."),
        ("Never write laudo, parecer, auditoria, avaliação or mandato. The contract is "
         "a corretagem under arts. 722–729 do Código Civil. A mandato binds, and we "
         "must not have one."),
        ("Every number in these emails is from the fund's own CVM informe for July "
         "2026 and is public. Check one before you send the first email — if a manager "
         "corrects you on his own filing, the conversation is over."),
        ("The recipient address is blank on every email. Find the person, do not guess "
         "the address, and do not send to a generic contato@ inbox."),
        ("The first serious reply will ask what we charge. The corretagem contract is "
         "not drafted yet. Decide with MGC what you say before the first email goes."),
    ]:
        para(doc, "•  " + t, size=10.5, space=6)

    para(doc, "Two data problems you should know about", size=14, bold=True, space=8)
    para(doc, "Positiva Investimentos — the phone number in our file is 11 9999-9999, "
              "which is placeholder data, not a number. Find the real one before "
              "calling. The email is unaffected.", size=10.5, color=RED, space=6)
    para(doc, "Signing directors come from the CVM register and may have changed. "
              "Confirm the name before you send; an email addressed to somebody who "
              "left is worse than no email.", size=10.5, color=RED, space=6)

    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def email_page(doc, i: int, house: str, funds: pd.DataFrame, row: pd.Series,
               phone: str, city: str) -> None:
    rank = PRIORITY.get(_ascii(house), (99, ""))
    lead = funds.iloc[0]
    director = cased(lead.get("Diretor", "")) or "{nome}"

    para(doc, f"{i}. {house.title()}", size=17, bold=True, space=2)
    meta = (f"{city} · {phone} · {len(funds)} fundo{'s' if len(funds) > 1 else ''} · "
            f"R$ {row.face_Rm:,.0f}m de face · PDD {row.provision_pct:.0f}%")
    para(doc, meta, size=9.5, color=GREY, space=8)
    if rank[1]:
        para(doc, rank[1], size=9.5, italic=True, color=OCHRE, space=10)

    para(doc, "Funds: " + " · ".join(short(x["name"]) for _, x in funds.iterrows()),
         size=9.5, color=GREY, space=14)

    para(doc, "COPY FROM HERE", size=8, bold=True, color=OCHRE, space=8)

    subject, paras = body(house, funds, row)
    para(doc, f"Para:  {director}  <___________________________>", size=10.5,
         color=GREY, space=4)
    para(doc, f"Assunto:  {subject}", size=11, bold=True, space=12)
    para(doc, f"{director.split()[0]},", size=11, space=10)
    for p in paras:
        para(doc, p, size=11, space=10)
    para(doc, "Gui Cunha", size=11, space=0)
    para(doc, "Sutphin Ltd. · São Paulo", size=10.5, color=GREY, space=8)

    para(doc, "COPY TO HERE", size=8, bold=True, color=OCHRE, space=0)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def main() -> None:
    c = pd.read_csv("data/derived/call_sheet.csv")
    lp = pd.read_csv("data/derived/lot_plan.csv")
    t = pd.read_pickle("data/derived/targets_full.pkl")
    tt = t[t["captive_flag"] == False]
    lp = lp.merge(tt[["CNPJ_FUNDO_CLASSE", "Gestor", "Administrador", "Diretor"]],
                  left_on="cnpj", right_on="CNPJ_FUNDO_CLASSE", how="left")
    lp["house"] = lp["Gestor"].fillna(lp["Administrador"])
    lp.loc[lp["Administrador"].astype(str).str.contains("ACTUAL", na=False), "house"] = (
        "LIBERTAS / ACTUAL"
    )
    ct = pd.read_csv("data/derived/contacts.csv")

    c["rank"] = c.house.map(lambda h: PRIORITY.get(_ascii(h), (99, ""))[0])
    c = c.sort_values(["rank", "face_Rm"], ascending=[True, False]).reset_index(drop=True)

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name, st.font.size = "Calibri", Pt(11)
    for s in doc.sections:
        s.left_margin = s.right_margin = Pt(54)

    cover(doc, c)
    for i, row in c.iterrows():
        funds = lp[lp.house == row.house].sort_values("carteira", ascending=False)
        phone, city, _ = contact(ct, row.house)
        email_page(doc, i + 1, row.house, funds, row, phone, city)

    doc.save(OUT)
    print(f"wrote {OUT}\n  {len(c)} emails, {len(lp)} funds named")


if __name__ == "__main__":
    main()
