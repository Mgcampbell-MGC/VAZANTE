# SOURCES — where everything lives

## The Drive folder (canonical documents)

Folder: `8-VAZANTE special servicer for structured credit` — https://drive.google.com/drive/folders/1wmkA6zO1c4DLhYXCYuOez1pVhhSqNNNT (the folder name predates the principal model; the documents inside are the current ones).

| Doc | Google Doc ID | Role |
|---|---|---|
| 01 VAZANTE — buys whole broken FIDC carteiras for one cash price and resells them in three pieces | `1GYRdZhFSEM_qCi819LexSRBje7a-4PUYilhpotvamns` | **Canonical.** The business case, final (10 Sep 2026). Snapshot: `docs/01_…` |
| 02 — The buyer outreach package | `1qKxWaNrB71rO-FQGZ1A72vMwn32Rth2NFeXXyobF8TY` | **Canonical.** Pacote de Compradores. Snapshot: `docs/02_…` |
| 03 FORENSIC ORACLE LAYER | `1xsF2pH-BiOSYr6zBlJV4BjYUSI9KvzAoupk63XtRZJ4` | **Canonical.** Oracle spec. Snapshot: `docs/03_…` |
| 97 VAZANTE | `1U47K3RZaw7YPSiQT4KPsS_8Czj0I4nad5aJjHR8gaFo` | The compiled working document ("02 VAZANTE" in the business case's words) — superseded by 01 wherever they conflict; its plain-language summary is `docs/97_…` |
| 98 VAZANTE | `1oy_2SBfeQ1ETeaPSuMGEj72BnbACxIVEZN-nP2QyHBo` | Earlier fee-model brief (SONDA, success fees) — history only |
| 99 VAZANTE | `1BzHd6cTvXuAiWcl3ePEyrEQAn_iJDxnWsV1rdi7C__A` | Earliest special-servicer version — history only |
| One two Punch | `1o3lCHvLqJBhEDAb0NItuWVm5X6wFBtT9gAz0zMDcB9U` | VAZANTE + DRAGA as one company — context |
| DRAGA — buys and collects unpaid B2B debt in Brazil | `1IiexCNroPzUaB30PsdQLjBOj9ObPIQk2HT9-_N_zSCA` | Sister project — not in scope here |

Elsewhere in Drive: `PROJETO VAZANTE (TODAS AS CAMADAS) model.xlsx` (`1Aw-G3CV0oZUIUw-oOMaFSSc_o-ScnSAR`, March 2026) — an earlier model from before the principal design; reference only.

## Lost, to be rebuilt

The business case cites working files `/v3/P1–P6` and `P5_model.py` (2,500 Monte-Carlo paths per scenario). They are not in the Drive folder, not elsewhere in Drive under those names, and not in this repository. Only their outputs survive (Part 7 tables). `vazante/economics/reference_book.py` reproduces the one-trade arithmetic exactly and is the first regression anchor for the rebuild (BACKLOG #5).

## Public data (tested from this environment on 2026-09-11)

See `config/sources.yaml` for URLs, what each gives, auth needed, and status. In one line: CVM informe mensal, its dictionary and cad_fi are live and fetched; Fundos.NET, Minha Receita and the BCB series API answer; the DJEN API resets the connection from here; the BCB regimes-especiais OData path is unconfirmed; registradoras, CENPROT bulk, bureaus and court aggregators need contracts.

## This repository

GitHub `Mgcampbell-MGC/VAZANTE`, branch `claude/trusting-hamilton-ipvjf3` (this environment setup). `README.md` before this commit was the pasted text of 01 + 03 + the 97 excerpt; it now lives in `docs/`.
