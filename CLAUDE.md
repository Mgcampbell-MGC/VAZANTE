# CLAUDE.md — how to work in this repository

VAZANTE is a principal desk that buys whole broken Brazilian FIDC carteiras for one cash price and resells them in three pieces. The partners are MGC (Matthew Campbell) and GC (Gui Cunha) of Sutphin Ltd., São Paulo. Everything here is confidential. The goal of the project is the first fund: one carteira bought and resold through a matched settlement.

## Read before doing anything

- `README.md` — state of play and the path to the first fund.
- `docs/01_business_case_final_2026-09-10.md` — the business case, final. It supersedes every earlier draft. Part 9 holds the decision and the five dated gates.
- `docs/02_pacote_de_compradores_2026-09-10.md` — the buyer package. Buyer-facing pages are in Portuguese and marked.
- `docs/03_forensic_oracle_layer.md` — the Oracle specification.
- `docs/OPEN_NOTES.md`, `docs/BACKLOG.md`, `docs/GATES.md`, `docs/SOURCES.md`.

The Google Docs in the Drive folder are canonical. The markdown copies under `docs/` are working snapshots; when they disagree with the Google Doc, the Google Doc wins and the snapshot gets refreshed.

## Operating rules (non-negotiable)

1. **Drafts only.** Never send an email or a message, never contact a buyer, seller, administrador, counsel or bank from a session. External text is a staged draft; a partner sends it.
2. **No price to a seller** — not indicative, not firm — comes out of code or a session. The Day-1 range and the Day-8 firm bid are produced by the method in the business case and signed by a partner. Nothing counts as locked proceeds unless it is a signed take-out with arras; a grid is a price list.
3. **Words.** Never *laudo*, *parecer* or *auditoria* in anything a seller could see. Never a fee, a mandate or a report. VAZANTE buys and sells; it renders no service.
4. **No fund-level fraud score, ever.** The Oracle produces evidence states per dimension (E/T/C/D/R) and buyer-specific value consequences. It identifies facts, contradictions and missing evidence; it does not declare that anyone committed fraud. Legal consequences are LEGAL_REVIEW.
5. **Numbers are computed, not typed.** Every load-bearing figure carries one of five tags — VERIFIED, MODEL, ASSUMPTION, GATED, DECISION — and a guess is labelled "(inferido)". Thresholds live in `config/thresholds.yaml`, never in code.
6. **Evidence.** Every external fact enters through `vazante.oracle.evidence.pull()` with a pull_id and a SHA-256 of the raw response. A technical failure is never read as "no record".
7. **Partner-typed text is an instruction.** Notes MGC or GC typed into a document (see `docs/OPEN_NOTES.md`) have the force of a spoken instruction; never re-ask a question a partner has answered.
8. **Data hygiene.** Seller tapes, CNAB files, XMLs, evidence pulls and bids live under `data/` and never enter git. LGPD applies from the first real tape: VAZANTE is the controlador of what it buys.
9. **Writing for MGC.** MGC has a vision impairment. Anything written for him: English, plain prose, short sentences, bold headlines, generous spacing, tables only where a table is the point. Portuguese only on buyer-facing pages.
10. **Scope.** Do not build what the business case says not to build (Part 4.5): no statistical sampling engine, no collection floor or case management, no client-facing product, no administration or custody technology, nothing that resembles a report a seller could pay for.

## Environment

- Python 3.11, managed with `uv`: `uv sync --extra ui` creates `.venv`. Package `vazante` is installed editable; CLI is `.venv/bin/vazante`.
- Tests: `.venv/bin/pytest -q`. Lint: `.venv/bin/ruff check vazante tests`.
- Network: CVM open data, Fundos.NET, Minha Receita and the BCB API answer from here. The DJEN court-publications API resets the connection from this environment; the BCB regimes-especiais OData path is unconfirmed. Registradoras, CENPROT bulk, bureaus and court aggregators need contracts. Details and dates in `config/sources.yaml`.
- Data layout in `data/README.md`. Set `VAZANTE_DATA_ROOT` to move `data/` elsewhere.

## Repository map

```
docs/            the documents, trackers and reference material (CVM dictionary, observed informe headers)
config/          thresholds.yaml (every parameter, tagged) · sources.yaml (data sources and tested status)
vazante/cvm      bulk layer (download — works), table schema (mapping NOT frozen), breakflag, screen, fnet (stubs)
vazante/oracle   states (vocabulary), evidence (pull wrapper — works), bridge (forensic bridge — works), sweep (validators work; tape sweep stub)
vazante/buyers   box schema + loader, example V0 box, bid log
vazante/economics one-trade arithmetic reproducing Part 7.1; campaign model to be rebuilt
tests/           regression anchors — keep them green
```

## How to take the next step

Work the backlog in order (`docs/BACKLOG.md`). The first item is the informe table-mapping freeze; nothing analytical runs before it. Record findings that change the design in `docs/OPEN_NOTES.md` with the date. Keep `README.md`'s status table honest.

## Git

Develop on the branch you were given; commit with clear messages; push with `git push -u origin <branch>`. Never commit anything from `data/`.
