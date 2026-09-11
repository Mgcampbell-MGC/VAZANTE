# VAZANTE

**What this is.** VAZANTE is a finite-life principal desk. It finds broken Brazilian FIDCs from public CVM data, establishes what is really inside the carteira on five separate dimensions (existence, title, cash, debtor, recourse), buys the whole carteira for one cash price, and resells it in three pieces (Premium, Claims, Residual) under buyer commitments locked before the seller ever hears a number. It never quotes a firm price to a seller until firm onward exits cover the all-in basis, tax included, by 1.20×. Sutphin Ltd. — MGC and GC — São Paulo. Confidential.

**The goal.** Get the first fund: one real carteira bought and resold through a matched settlement. Everything in this repository exists to shorten the path from "flagged in the CVM data" to "settled".

**State of play, 11 September 2026.** The business case is final and the decision is GO WITH CONDITIONS (five dated gates, see `docs/GATES.md`). No fund has been approached, no buyer has been called, nothing has been sent to anyone. This repository holds the documents, a working Python environment, the CVM data feed (verified live), and the scaffolding of the machine. The P1–P6 work-stream files and the P5 Monte-Carlo model referenced by the business case are not in Drive or here; they have to be rebuilt, and their published outputs are the regression targets.

## Read first

1. `docs/01_business_case_final_2026-09-10.md` — the business case, final. Part 1 is the business in one page; Part 9 is the decision.
2. `docs/02_pacote_de_compradores_2026-09-10.md` — the buyer package (buyer-facing pages in Portuguese).
3. `docs/03_forensic_oracle_layer.md` — the specification of the Oracle.
4. `docs/OPEN_NOTES.md` — MGC's typed notes and the open questions the environment setup surfaced.
5. `docs/BACKLOG.md` — the engineering work, in order. `docs/GATES.md` — the non-engineering conditions.

The Google Docs in the Drive folder are canonical; the markdown copies are working snapshots (`docs/SOURCES.md` has the IDs).

## The path to the first fund, and what exists for each step

| Step | Tool | Status |
|---|---|---|
| Detect: read every FIDC informe monthly, rank the broken ones | `vazante cvm fetch` (bulk layer), `vazante.cvm.breakflag` | Feed verified; mapping not frozen; rule not built |
| Screen: the five filters that produce the calling list | `vazante.cvm.screen` | Stub — needs the mapping and the Fundos.NET client |
| Pack: the two-page Day-1 sheet in 3.5–5 hours | `vazante.cvm.fnet` + counterparty run | Not built |
| Call → exclusivity → tape | GC, with the pack | Not started |
| Oracle: E/T/C/D/R on the tape, the forensic bridge, the lift list | `vazante.oracle` | Vocabulary, evidence wrapper, bridge and validators built; sweep and dimension engines not |
| Three FIRM take-outs under standing boxes | `vazante.buyers` | Box schema and bid log built; no real box exists yet |
| Max bid → firm whole-book bid | `vazante.economics` | One-trade arithmetic reproduces the business case; campaign model to rebuild |
| Matched settlement | counsel + bank | Not started (condition 5) |

## Set up

Needs Python 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --extra ui          # creates .venv with everything, including Streamlit for the partners' UI
.venv/bin/pytest -q         # the test suite
.venv/bin/vazante status    # environment report
.venv/bin/vazante cvm months            # what the CVM has published
.venv/bin/vazante cvm fetch --months 1  # one informe month into data/raw (smoke test)
.venv/bin/vazante max-bid --L 13.953    # the reference-book arithmetic
```

`data/` is git-ignored; see `data/README.md` for the layout. Thresholds live in `config/thresholds.yaml`, data sources and their tested status in `config/sources.yaml`.

## Rules that apply to every session in this repository

See `CLAUDE.md`. The short version: drafts only, nothing is sent to anyone from here; no price to a seller before three FIRM exits exist; never the words laudo, parecer or auditoria in seller-facing text; every figure carries its tag (VERIFIED, MODEL, ASSUMPTION, GATED, DECISION); numbers are computed by code, not typed.
