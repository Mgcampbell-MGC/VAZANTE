"""Informe Mensal table map — Res. CVM 175, Suplemento G.

STATUS: NOT FROZEN. Business case Part 2.1 records that an earlier tab mapping was wrong and would have broken
the most important query. BACKLOG #1 freezes it: diff the observed CSV headers
(docs/reference/informe_mensal_202608_headers.txt) and the CVM dictionary (docs/reference/cvm_meta_inf_mensal_fidc/)
against Suplemento G, then write config/informe_mapping.yaml. Until that file exists every semantic accessor raises
MappingNotFrozen. Raw table reads are allowed.

Observed 2026-09-11 (competência 2026-08, 18 ZIP members, all keyed on TP_FUNDO_CLASSE;CNPJ_FUNDO_CLASSE;DENOM_SOCIAL;DT_COMPTC):
  I      ativo, PDD, carteira; cedentes 1–9 as TAB_I2A12_CPF_CNPJ_CEDENTE_n / TAB_I2A12_PR_CEDENTE_n     109 cols
  II     carteira por segmento (industrial, imobiliário, comercial, serviços, agro, financeiro, ...)       37
  III    passivo                                                                                          13
  IV     PL, PL médio                                                                                      6
  V      comportamento da carteira — com aquisição substancial (a vencer, inadimplentes, pagos antecip.)  37
  VI     comportamento da carteira — sem aquisição substancial                                            37
  VII    negócios no mês: aquisições, alienações, substituições, recompras — quantidade e valor           29
  VIII   25 maiores sacados — SEQUENCIAL + VALOR ONLY in the open-data CSV; no CPF/CNPJ                    6  ← FLAG
  IX     taxas praticadas (compra/venda min, média, max)                                                  76
  X      SCR risk buckets · X_1 cotistas por classe · X_1_1 cotistas por tipo · X_2 cotas · X_3 rentabilidade
         X_4 captações/resgates por tipo de operação · X_5 liquidez · X_6 desempenho esperado/real · X_7 garantias

FLAG (2026-09-11): the business case treats Tabela VIII as naming the 25 largest sacados with CPF/CNPJ every
month. The open-data CSV carries rank and value only. Whether the identities exist anywhere public (the informe
as filed on Fundos.NET, a different CVM extract) is BACKLOG #2. If the answer is no, the D-dimension
pre-exclusivity engine (business case 2.1–2.3) has to be redesigned around the lâmina, the rating reports and
the fund's own litigation instead of the informe.
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pandas as pd
import yaml

from vazante.config import CONFIG_DIR

MAPPING_FILE = CONFIG_DIR / "informe_mapping.yaml"

TABS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "X_1", "X_1_1", "X_2", "X_3", "X_4", "X_5", "X_6", "X_7"]
KEY_COLS = ["TP_FUNDO_CLASSE", "CNPJ_FUNDO_CLASSE", "DENOM_SOCIAL", "DT_COMPTC"]


class MappingNotFrozen(RuntimeError):
    """Raised by semantic accessors until config/informe_mapping.yaml exists (docs/BACKLOG.md #1)."""


def member_name(tab: str, month: str) -> str:
    return f"inf_mensal_fidc_tab_{tab}_{month}.csv"


def month_from_path(zip_path: Path) -> str:
    for part in reversed(zip_path.parts):
        if len(part) == 6 and part.isdigit():
            return part
    m = re.search(r"(\d{6})", zip_path.name)
    if m:
        return m.group(1)
    raise ValueError(f"cannot infer YYYYMM from {zip_path}")


def read_table(zip_path: Path, tab: str, month: str | None = None) -> pd.DataFrame:
    """Raw read of one table. Everything stays a string until the frozen mapping fixes each column's meaning."""
    month = month or month_from_path(zip_path)
    with zipfile.ZipFile(zip_path) as z, z.open(member_name(tab, month)) as f:
        return pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, keep_default_na=False)


def load_mapping() -> dict:
    if not MAPPING_FILE.exists():
        raise MappingNotFrozen("config/informe_mapping.yaml does not exist — run the header diff (docs/BACKLOG.md #1) and freeze it")
    with open(MAPPING_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def column(concept: str) -> tuple[str, str]:
    """Resolve a concept such as 'recompras_valor' to (tab, column) from the frozen mapping."""
    mapping = load_mapping()
    try:
        entry = mapping["concepts"][concept]
    except KeyError as e:
        raise MappingNotFrozen(f"concept {concept!r} is not in the frozen mapping") from e
    return entry["tab"], entry["column"]
