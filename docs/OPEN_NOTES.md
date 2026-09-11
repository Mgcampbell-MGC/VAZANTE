# OPEN NOTES — partner-typed notes and questions the setup surfaced

Partner-typed text is an instruction. Entries are verbatim, then a plain reading, then what it changes. Add new entries at the top with the date.

## MGC's typed notes found in the documents (as pasted 2026-09-11)

**1. In the business case, Part 1, Capital row (verbatim):**
> "Third-party capital where needed; Sutphin takes the residual….GC MIGHT NOT BE NEED MIGHT E BETTER WAY TO DO THIS instead of a bridge"

Plain reading (inferido): MGC questions whether the R$5m committed settlement line ("bridge") is needed at all, and whether a better structure exists for the settlement float. Possibly also whether GC's involvement in that piece is needed. **Open decision for MGC.** It touches Part 7.4 (settlement float R$6.2m P50 / R$11.9m P90), red-team attacks 3 and 14 (committed capital sized at the largest exit parcel), and condition 5 (all legs through one escrow agent). Nothing in the repo assumes the line exists.

**2. In the business case, Part 1, the one sentence for GC (verbatim):**
> "— GC the seller  never see how we cut it up and break down the brick."

Plain reading: the seller never sees the carve. This is already an absolute rule (carve private; the existence of a resale-in-parcels strategy is acknowledged in the SPA, never the prices or the routing). Recorded so the sentence is not lost when the doc is edited.

**3. At the head of the "97 VAZANTE" summary (verbatim):**
> "THESE CAN CHNAGE NOTTHING HERE IS PERMINT THIS THE WORKING IDEA OF THE BUSSINESS KISS"

Plain reading: nothing in that summary is fixed; it is the working idea; keep it simple. Treat 97 as direction, not specification; 01 governs.

## Questions the environment setup raised (2026-09-11)

**A. Tabela VIII in the open data does not name the sacados.** The business case (Part 2.1, tagged VERIFIED) relies on Tabela VIII giving "CPF/CNPJ, R$, % PL" for the 25 largest sacados every month, and builds the D-dimension pre-exclusivity engine and the Day-1 sheet's field 12 on it. The CSV published by the CVM (`inf_mensal_fidc_tab_VIII_202608.csv`) carries only `SEQUENCIAL` and `VALOR` per fund; the dictionary describes no identity field. Either the identities exist in the informe as filed on Fundos.NET, or in another CVM extract, or they are not public. **BACKLOG #2 settles it.** If not public, the counterparty run has to be rebuilt from the lâmina (top-5 devedores and coobrigados by name), rating reports and the fund's litigation, and the Day-1 band is wider than Part 2.3 assumes.

**B. Cedentes are partly named in Tabela I.** `TAB_I2A12_CPF_CNPJ_CEDENTE_1…9` with `TAB_I2A12_PR_CEDENTE_n` (participation). The business case says cedentes are "usually empty in a genuine multicedente book" — to be measured on the population (BACKLOG #3).

**C. The current month's file is partial while the filing window is open.** 2026-08 had 664 classes on 2026-09-11. The downloader stores dated snapshots so late and restated filings become visible; population counts should use the last closed month.

**D. The P1–P6 working files and P5_model.py are lost.** See `docs/SOURCES.md`. The one-trade arithmetic is reproduced and tested; the campaign model is not.

**E. Sources blocked or unconfirmed from this environment.** DJEN (`comunica.pje.jus.br`) resets the connection; the BCB regimes-especiais OData path guessed from the doc returns 404. Both may work from a Brazilian desk; both are needed for the pack (litigation by party name; liquidation regimes weekly).
