"""Render the email pack as HTML for upload to Drive as a Google Doc.

Same content as the .docx. Google converts HTML to a Doc on upload, which keeps
headings, bold and rules, and gives GC something he can open in a browser and
copy straight out of.

    .venv/bin/python -m scripts.build_email_pack_html > out/emails.html
"""

from __future__ import annotations

import html

import pandas as pd

from scripts.build_call_workbook import PRIORITY, _ascii, contact
from scripts.build_email_pack import body, cased
from scripts.call_sheet_md import short

M = 1_000_000.0


def e(s: object) -> str:
    return html.escape(str(s))


HOWTO = [
    ("One email per section.", ("Select from <b>COPY FROM HERE</b> down to the signature, "
     "copy, paste into your mail client. Nothing inside a copyable block is a table, so it "
     "pastes cleanly.")),
    ("Fifteen emails, not twenty-five.", ("Where a house manages four funds, one man signs for "
     "all four. Four separate emails to the same person read as a mail-merge and lose the "
     "house. Each email names every fund and leads on the largest.")),
    ("They are in call order, not size order.", ("Libertas / Actual is first because the same "
     "two officers sign the gestora and the administrador, so there is no second party to "
     "convince.")),
    ("Send them one at a time, by hand, over several days.", ("Fifteen emails is not a campaign. "
     "A sequencing tool leaves fingerprints this audience notices, and it would put all fifteen "
     "at risk at once.")),
]

RULES = [
    ("No price.", ("Not a range, not an example, not in a reply. If asked, the answer is that a "
     "price comes out of a competitive round.")),
    (("Never write <i>laudo</i>, <i>parecer</i>, <i>auditoria</i>, <i>avaliação</i> or "
     "<i>mandato</i>."), ("The contract is a <b>corretagem</b> under arts. 722–729 do Código "
     "Civil. A <i>mandato</i> binds, and we must not have one.")),
    ("Check one number before the first email goes.", ("Every figure here is from the fund's own "
     "CVM informe for July 2026 and is public. If a manager corrects you on his own filing, the "
     "conversation is over.")),
    ("The recipient address is blank on every email.", ("Find the person. Do not guess an "
     "address and do not send to a generic <i>contato@</i> inbox.")),
    ("The first serious reply will ask what we charge.", ("The corretagem contract is not drafted "
     "yet. Decide with MGC what you say before the first email goes out.")),
]

WARN = [
    ("Positiva Investimentos", ("the phone number in our file is 11 9999-9999, which is "
     "placeholder data rather than a number. Find the real one before calling. The email itself "
     "is unaffected.")),
    ("Signing directors", ("these come from the CVM register and may have changed. Confirm the "
     "name before you send — an email addressed to somebody who left is worse than no email.")),
]


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

    o: list[str] = ['<meta charset="utf-8">']
    o.append("<h1>VAZANTE — fifteen emails, ready to send</h1>")
    o.append(f"<p><i>14 September 2026 · {len(c)} houses · 25 funds · "
             "nobody has been contacted · drafts only, a partner sends them</i></p>")

    o.append("<h2>How to use this</h2><ul>")
    for k, v in HOWTO:
        o.append(f"<li><b>{k}</b> {v}</li>")
    o.append("</ul>")

    o.append("<h2>Before you send anything</h2><ul>")
    for k, v in RULES:
        o.append(f"<li><b>{k}</b> {v}</li>")
    o.append("</ul>")

    o.append("<h2>Two data problems</h2><ul>")
    for k, v in WARN:
        o.append(f"<li><b>{k}</b> — {v}</li>")
    o.append("</ul>")

    for i, row in c.iterrows():
        funds = lp[lp.house == row.house].sort_values("carteira", ascending=False)
        phone, city, _ = contact(ct, row.house)
        why = PRIORITY.get(_ascii(row.house), (99, ""))[1]
        lead = funds.iloc[0]
        director = cased(lead.get("Diretor", "")) or "{nome}"
        subject, paras = body(row.house, funds, row)

        o.append(f"<h2>{i + 1}. {e(row.house.title())}</h2>")
        o.append(f"<p><i>{e(city)} · {e(phone)} · {len(funds)} fundo"
                 f"{'s' if len(funds) > 1 else ''} · R$ {row.face_Rm:,.0f}m de face · "
                 f"PDD {row.provision_pct:.0f}%</i></p>")
        if why:
            o.append(f"<p><i>{e(why)}</i></p>")
        o.append("<p><i>Funds: "
                 + " · ".join(e(short(x['name'])) for _, x in funds.iterrows()) + "</i></p>")

        o.append("<p><b>— — — COPY FROM HERE — — —</b></p>")
        o.append(f"<p>Para: {e(director)} &lt;___________________________&gt;</p>")
        o.append(f"<p><b>Assunto: {e(subject)}</b></p>")
        o.append(f"<p>{e(director.split()[0])},</p>")
        for p in paras:
            o.append(f"<p>{e(p)}</p>")
        o.append("<p>Gui Cunha<br>Sutphin Ltd. · São Paulo</p>")
        o.append("<p><b>— — — COPY TO HERE — — —</b></p>")

    print("\n".join(o))


if __name__ == "__main__":
    main()
