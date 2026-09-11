# data/

Everything under here except this file is git-ignored. Layout (created on demand by `vazante.config.ensure_dirs()`):

- `raw/cvm/inf_mensal/<YYYYMM>/fetched-<date>.zip` — monthly informe ZIPs as dated snapshots (the CVM re-publishes a month as late filers arrive; a late or restated filing is itself a signal).
- `raw/cvm/cad_fi/cad_fi_<date>.csv` — daily cadastro snapshot (administrador, gestor, custodiante, auditor, situação).
- `raw/cvm/meta/` — the CVM data dictionary ZIP.
- `raw/cvm/manifest.jsonl` — one line per stored file: url, path, sha256, bytes, fetched_at, last_modified.
- `raw/fnet/<cnpj>/` — regulamento, DFs, atas, fatos relevantes, lâmina pulled from Fundos.NET.
- `derived/` — parquet panels built from raw (indicator panel, screen output, calling list).
- `evidence/` — `pull()` records (`pulls.jsonl`) and raw responses by SHA-256. Every external fact the Oracle uses has a line here.
- `deals/<deal_id>/` — seller tapes, CNAB files, XMLs, termos. **Never leaves the machine, never enters git.**
- `bids/bids.jsonl` — every buyer bid ever received, stored forever (stated box → observed box).
