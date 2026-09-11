# docs/reference

- `cvm_meta_inf_mensal_fidc/` — the CVM's own field dictionary for the FIDC Informe Mensal (18 tables), fetched 2026-09-11 from `dados.cvm.gov.br/dados/FIDC/DOC/INF_MENSAL/META/`, converted to UTF-8. Public metadata.
- `informe_mensal_202608_headers.txt` — the header row and row count of every CSV member of `inf_mensal_fidc_202608.zip` as observed on 2026-09-11 (filing window still open: 664 classes). This is the raw side of the mapping freeze (BACKLOG #1).

Two observations that matter for the design, both recorded in `docs/OPEN_NOTES.md`: Tabela VIII in the open-data CSV carries rank and value only (no sacado CPF/CNPJ); Tabela I carries up to nine cedente CPF/CNPJs with their participation.
