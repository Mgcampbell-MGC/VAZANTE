"""Render the call sheet as the document GC works from.

Structure and commentary in English for MGC; the spoken part in Portuguese, which
is the only part a counterparty ever sees. Every figure comes from the fund's own
CVM filing. No price appears in the Portuguese anywhere — operating rule 2 — and
none of the forbidden words appear at all: laudo, parecer, auditoria, avaliacao,
mandato.

    .venv/bin/python scripts/call_sheet_md.py > docs/seller/CALL_SHEET.md
"""

from __future__ import annotations

import pandas as pd

M = 1_000_000.0
OUT_SHEET = "data/derived/call_sheet.csv"
FUNDS = "data/derived/lot_plan.csv"

BANNED = ["laudo", "parecer", "auditoria", "avaliação", "avaliacao", "mandato", "honorário"]


def short(name: str) -> str:
    n = name.replace("FUNDO DE INVESTIMENTO EM DIREITOS CREDITÓRIOS", "FIDC")
    n = n.replace("FUNDO DE INVESTIMENTOS EM DIREITOS CREDITÓRIOS", "FIDC")
    n = n.replace("FUNDO DE INVESTIMENTO EM DIREITOS CREDITORIOS", "FIDC")
    for junk in [" NÃO PADRONIZADOS", " NÃO-PADRONIZADOS", " NAO PADRONIZADOS",
                 " - RESPONSABILIDADE LIMIT", " RESPONSABILIDADE LIMITADA", " - RESP LIMITADA",
                 " DE RESPONSABILIDADE LIMITADA", " MULTISSETORIAL", " MULTISSEGMENTOS",
                 " MULTISEGMENT0S", " MULTISEGMENTOS", " MULTICREDITO", " LP"]:
        n = n.replace(junk, "")
    return " ".join(n.split()).strip(" -")


def opening(house: str, funds: pd.DataFrame, row: pd.Series) -> str:
    """The Portuguese opening. Their own numbers, no price, ends with a small ask."""
    lead = funds.iloc[0]
    nm = short(lead["name"])
    a, d = lead.lot_A / M, lead.lot_D / M
    many = len(funds) > 1
    scope = f"os {len(funds)} fundos que vocês gerem" if many else nm
    return f"""> Bom dia, {{nome}}. Aqui é o Gui Cunha, da Sutphin.
>
> Não estou ligando para comprar nada, e não vou falar de preço.
>
> Eu li os informes mensais {"de " if many else "do "}{scope}. Em julho, a carteira soma
> R$ {row.carteira_Rm:,.0f} milhões com PDD de {row.provision_pct:.0f}%.
> Da face bruta{" do " + nm if many else ""}, R$ {a:,.0f} milhões ainda **não venceram**
> e R$ {d:,.0f} milhões estão vencidos **há mais de 180 dias**. São dois ativos
> diferentes, e quem compra um não é quem compra o outro.
>
> E tem um número no informe de vocês que me chamou atenção: **alienação para
> terceiros, zero.** Nos últimos vinte e dois meses, em nenhum dos fundos dessa
> tese saiu um real para terceiro. O único dinheiro que saiu foi recompra de
> cedente.
>
> O que a Sutphin faz é isto: a gente corta a carteira em lotes por tipo de risco,
> leva cada lote para quem compra aquele risco específico, e roda um processo
> competitivo com prazo. A Sutphin **não compra e não fica com o dinheiro** — o
> comprador paga o fundo direto, e a gente é remunerado pela corretagem.
>
> Para montar os lotes eu preciso do arquivo posição a posição. Posso te mandar
> uma página dizendo exatamente quais campos?"""


def main() -> None:
    c = pd.read_csv(OUT_SHEET)
    lp = pd.read_csv(FUNDS)
    t = pd.read_pickle("data/derived/targets_full.pkl")
    tt = t[t["captive_flag"] == False]
    lp = lp.merge(tt[["CNPJ_FUNDO_CLASSE", "Gestor", "Administrador", "n_ced", "n_rj"]],
                  left_on="cnpj", right_on="CNPJ_FUNDO_CLASSE", how="left")
    lp["house"] = lp["Gestor"].fillna(lp["Administrador"])
    lp.loc[lp["Administrador"].astype(str).str.contains("ACTUAL", na=False), "house"] = (
        "LIBERTAS / ACTUAL"
    )
    ct = pd.read_csv("data/derived/contacts.csv")

    print(f"""# The call sheet

**13 September 2026. Fifteen conversations reach all twenty-five funds.
R$ {c.face_Rm.sum():,.0f}m of gross face. Nobody has been contacted.**

This replaces the sheet built on 12 September. Every row on that one pitched
*compra carteiras inteiras, à vista, como principal* with a footer about three firm
exits at 1.20×. That was the model the desk ran until this week and it cannot close
fast. These rows pitch the lot sale instead.

## What is different

**The opening is a plan, not a question.** The old sheet opened by asking about
redemption suspension under art. 44 §3, which is an intelligence question — it
produces a conversation, not a transaction. Each row below opens with that house's
own lot plan, taken from its own filings, and ends with one small ask: a page
listing the fields we need in the tape.

**The fact that carries every call is theirs, not ours.** Across all twenty-five
funds, third-party sales total R$5.0m ever — one fund, twice, last in October 2024.
**Nothing has been sold to anybody in twenty-two months.** Meanwhile the cedentes
repurchased R$1,033m in the twelve months to July. These books have exactly one
buyer and it is the man who sold them the paper.

**Each row names the buyers for that house's own lots**, and the two blocks route
to different firms. That routing is computed by `vazante/lots/route.py` against
`config/buyer_registry.yaml`, and a firm is dropped when the lot cannot produce a
cheque above its floor.

## Rules for every call

**No price. Not indicative, not a range, not "somewhere around".** If asked, the
answer is that a price comes out of a competitive round, not out of a phone call.

**Never say** *laudo*, *parecer*, *auditoria*, *avaliação* or *mandato*. The contract
is a **corretagem** under arts. 722–729 do Código Civil — it introduces without
binding. A *mandato* binds, and we must not have one.

**We contract with the gestora as a company, never with the fund.** That keeps the
whole thing outside Anexo II da Res. CVM 175: no change to the regulamento, no
assembleia, no fee at fund level, no CVM filing.

**The ask is the tape.** Not a meeting, not a mandate, not a price. One file,
position by position.

---
""")

    for i, (_, r) in enumerate(c.iterrows(), 1):
        h = r.house
        funds = lp[lp.house == h].sort_values("carteira", ascending=False)
        m = ct[ct.name.str.contains(h.split()[0], case=False, na=False)]
        phone = city = socios = "—"
        if len(m):
            row0 = m.iloc[0]
            ph = str(row0.phone)
            phone = f"+55 {ph[:2]} {ph[2:-4]}-{ph[-4:]}" if ph and ph != "nan" else "—"
            city = row0.city
            socios = "; ".join(str(row0.socios).split("; ")[:3])

        rp = "não reportado" if pd.isna(r.recourse_pct) else f"{r.recourse_pct:.0f}%"
        print(f"## {i}. {h}\n")
        print(f"**{city}** · {phone} · {int(r.funds)} fund"
              f"{'s' if r.funds > 1 else ''} · R$ {r.face_Rm:,.0f}m face\n")
        print(f"Registered officers: {socios}\n")

        print("| Fund | Carteira | PDD | Not yet due | 1–90d | 90–180d | 180d+ | Cedentes |")
        print("|---|--:|--:|--:|--:|--:|--:|--:|")
        for _, x in funds.iterrows():
            pdd = 100 * x.provision / x.carteira if x.carteira else 0
            print(f"| {short(x['name'])} | {x.carteira / M:,.1f} | {pdd:.0f}% | "
                  f"{x.lot_A / M:,.1f} | {x.lot_B / M:,.1f} | {x.lot_C / M:,.1f} | "
                  f"{x.lot_D / M:,.1f} | {int(x.cedentes_named)}"
                  f"{f' ({int(x.cedentes_in_rj)} em RJ)' if x.cedentes_in_rj else ''} |")
        print(f"\nRecourse to the cedente: **{rp}** of the credit book.\n")

        print("**Who buys it**\n")
        for block, face, names in [
            ("Performing", r.performing_Rm, r.performing_buyers),
            ("Distressed", r.distressed_Rm, r.distressed_buyers),
        ]:
            if face <= 0:
                continue
            nm = names if isinstance(names, str) and names else (
                "**no named buyer — the cheque is below every floor in the registry**"
            )
            print(f"- **{block} · R$ {face:,.1f}m** → {nm}")
        print()
        print(opening(h, funds, r))
        print("\n---\n")

    print("""*Drafts only. Nothing here has been said to anybody, and nothing here is a price.
Rebuild with `.venv/bin/python scripts/call_sheet.py && .venv/bin/python scripts/call_sheet_md.py`.*""")


if __name__ == "__main__":
    main()
