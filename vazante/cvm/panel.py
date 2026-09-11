"""Build the monthly panel from the frozen mapping (config/informe_mapping.yaml).

One row per fund-class per competency month, with every concept the break rule and the screen need resolved to
its real column. Wide tables (I, II, IV, VII, V, VI) contribute one value per row. Long tables (X_1..X_6, VIII)
are aggregated: quota series by senior/subordinada prefix, X.4 operations by TP_OPER.

Written to data/derived/panel.parquet. Rebuild is idempotent and takes minutes, not hours.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

from vazante.config import DERIVED_DIR, RAW_DIR
from vazante.cvm.schema import load_mapping, member_name, read_table

INF_DIR = RAW_DIR / "cvm" / "inf_mensal"
PANEL_PATH = DERIVED_DIR / "panel.parquet"
KEY = "CNPJ_FUNDO_CLASSE"


def available_months() -> list[str]:
    return sorted(d.name for d in INF_DIR.iterdir() if d.is_dir() and d.name.isdigit())


def snapshot(month: str) -> Path:
    snaps = sorted((INF_DIR / month).glob("fetched-*.zip"))
    if not snaps:
        raise FileNotFoundError(f"no snapshot for {month}")
    return snaps[-1]


# Res. CVM 175 moved the informe from fund level to class level during 2024. Before that the long tables (X_*)
# key on CNPJ_FUNDO; after it, on CNPJ_FUNDO_CLASSE. Tabelas I-IX carried the new name throughout.
LEGACY_KEYS = ("CNPJ_FUNDO", "CNPJ_FUNDO_CLASSE_SERIE")


def _normalize_key(df: pd.DataFrame) -> pd.DataFrame:
    if KEY in df.columns:
        return df
    for legacy in LEGACY_KEYS:
        if legacy in df.columns:
            return df.rename(columns={legacy: KEY})
    return df


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.replace("", None), errors="coerce")


def _tabs_in(zip_path: Path, month: str) -> set[str]:
    names = set(zipfile.ZipFile(zip_path).namelist())
    return {t for t in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
                        "X", "X_1", "X_2", "X_3", "X_4", "X_5", "X_6", "X_7")
            if member_name(t, month) in names}


def build_month(month: str, mapping: dict | None = None) -> pd.DataFrame:
    """One month of the panel."""
    mapping = mapping or load_mapping()
    concepts = mapping["concepts"]
    zp = snapshot(month)
    present = _tabs_in(zp, month)
    cache: dict[str, pd.DataFrame] = {}

    def table(tab: str) -> pd.DataFrame | None:
        if tab not in present:
            return None
        if tab not in cache:
            cache[tab] = _normalize_key(read_table(zp, tab, month))
        return cache[tab]

    base = table("I")
    if base is None:
        raise FileNotFoundError(f"{month} has no Tabela I")
    out = base[[KEY, "TP_FUNDO_CLASSE", "DENOM_SOCIAL", "DT_COMPTC"]].copy()
    out["month"] = month
    out = out.drop_duplicates(subset=[KEY])

    for name, spec in concepts.items():
        tabs = spec.get("tab")
        tabs = tabs if isinstance(tabs, list) else [tabs]
        cols = spec.get("column", spec.get("columns"))
        cols = cols if isinstance(cols, list) else [cols]
        agg = spec.get("aggregate")

        # long tables carry a per-row label or filter
        if spec.get("label") or spec.get("filter"):
            df = table(tabs[0])
            if df is None:
                out[name] = pd.NA
                continue
            col = cols[0]
            if col not in df.columns:
                out[name] = pd.NA
                continue
            work = df[[KEY] + ([spec["label"]] if spec.get("label") and spec["label"] in df.columns else [])
                      + ([k for k in spec.get("filter", {}) if k in df.columns])].copy()
            work["_v"] = _num(df[col])
            if spec.get("filter"):
                for k, v in spec["filter"].items():
                    if k in work.columns:
                        work = work[work[k] == v]
                out = out.merge(work.groupby(KEY)["_v"].sum().rename(name), on=KEY, how="left")
            else:
                label = spec["label"]
                if label in work.columns and label == "TAB_X_CLASSE_SERIE":
                    senior = work[work[label].str.startswith(mapping["class_series"]["senior_prefix"], na=False)]
                    sub = work[work[label].str.startswith(mapping["class_series"]["subordinada_prefix"], na=False)]
                    out = out.merge(senior.groupby(KEY)["_v"].mean().rename(f"{name}_senior"), on=KEY, how="left")
                    out = out.merge(sub.groupby(KEY)["_v"].mean().rename(f"{name}_sub"), on=KEY, how="left")
                else:
                    out = out.merge(work.groupby(KEY)["_v"].sum().rename(name), on=KEY, how="left")
            continue

        # cedente name/participation lists: count how many slots are filled
        if agg == "list":
            df = table(tabs[0])
            if df is None:
                out[f"n_{name}"] = pd.NA
                continue
            have = [c for c in cols if c in df.columns]
            if not have:
                out[f"n_{name}"] = pd.NA
                continue
            filled = df[have].apply(lambda s: s.astype(str).str.strip().ne("") & s.notna())
            out = out.merge(
                pd.DataFrame({KEY: df[KEY], f"n_{name}": filled.sum(axis=1)}).drop_duplicates(subset=[KEY]),
                on=KEY, how="left")
            continue

        # text concepts are carried through verbatim, never coerced to numbers
        if spec.get("dtype") == "text":
            df = table(tabs[0])
            src = cols[0]
            if df is None or src not in df.columns:
                out[name] = pd.NA
            else:
                out = out.merge(df[[KEY, src]].drop_duplicates(subset=[KEY]).rename(columns={src: name}),
                                on=KEY, how="left")
            continue

        # wide tables: sum the named columns across the named tabs
        total = None
        for tab in tabs:
            df = table(tab)
            if df is None:
                continue
            for c in cols:
                if c in df.columns:
                    v = pd.DataFrame({KEY: df[KEY], "_v": _num(df[c])}).groupby(KEY)["_v"].sum()
                    total = v if total is None else total.add(v, fill_value=0)
        if total is None:
            df0 = table(tabs[0])
            src = cols[0]
            if df0 is not None and src in df0.columns:  # non-numeric passthrough (admin name, flags)
                out = out.merge(df0[[KEY, src]].drop_duplicates(subset=[KEY]).rename(columns={src: name}),
                                on=KEY, how="left")
            else:
                out[name] = pd.NA
        else:
            out = out.merge(total.rename(name), on=KEY, how="left")

    # Tabela VIII: rank-and-value only, so carry the shape rather than identities
    df8 = table("VIII")
    if df8 is not None and "VALOR" in df8.columns:
        v = df8.assign(_v=_num(df8["VALOR"])).groupby(KEY)["_v"]
        out = out.merge(v.sum().rename("top_sacados_valor"), on=KEY, how="left")
        out = out.merge(v.count().rename("top_sacados_n"), on=KEY, how="left")
    return out


def build_panel(months: list[str] | None = None, save: bool = True) -> pd.DataFrame:
    mapping = load_mapping()
    months = months or available_months()
    frames = []
    for m in months:
        try:
            frames.append(build_month(m, mapping))
        except FileNotFoundError:
            continue
    panel = pd.concat(frames, ignore_index=True).sort_values([KEY, "month"])
    if save:
        DERIVED_DIR.mkdir(parents=True, exist_ok=True)
        panel.to_parquet(PANEL_PATH, index=False)
    return panel


def load_panel() -> pd.DataFrame:
    return pd.read_parquet(PANEL_PATH)


def load_cad_fi() -> pd.DataFrame:
    """LEGACY register (FI/CAD/DADOS/cad_fi.csv).

    Do not use it for FIDCs: 46,575 of its 46,806 rows are CANCELADA and only 1.6% of live informe classes
    match it. It is the pre-Res. CVM 175 file, kept for history. Use load_registro() instead.
    """
    snaps = sorted((RAW_DIR / "cvm" / "cad_fi").glob("cad_fi_*.csv"))
    if not snaps:
        raise FileNotFoundError("no cad_fi snapshot")
    return pd.read_csv(snaps[-1], sep=";", encoding="latin-1", dtype=str, low_memory=False)


def load_registro() -> pd.DataFrame:
    """The live Res. CVM 175 register (FI/CAD/DADOS/registro_fundo_classe.zip), class rows joined to their fund.

    registro_classe carries CNPJ_Classe, which is the informe's CNPJ_FUNDO_CLASSE, plus the class situação and
    the Entidade_Investimento flag the captive-FIDC tax gate turns on. registro_fundo carries administrador,
    gestor and diretor responsável. One row per class.
    """
    snaps = sorted((RAW_DIR / "cvm" / "registro").glob("registro_fundo_classe_*.zip"))
    if not snaps:
        raise FileNotFoundError("no registro snapshot; download FI/CAD/DADOS/registro_fundo_classe.zip")
    with zipfile.ZipFile(snaps[-1]) as z:
        with z.open("registro_classe.csv") as f:
            classe = pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, low_memory=False)
        with z.open("registro_fundo.csv") as f:
            fundo = pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, low_memory=False)
    fundo_cols = ["ID_Registro_Fundo", "CNPJ_Fundo", "Tipo_Fundo", "Situacao", "Diretor",
                  "CNPJ_Administrador", "Administrador", "CPF_CNPJ_Gestor", "Gestor", "Data_Cancelamento"]
    merged = classe.merge(fundo[fundo_cols], on="ID_Registro_Fundo", how="left",
                          suffixes=("_classe", "_fundo"))
    merged = merged.rename(columns={"CNPJ_Classe": KEY})
    # The register stores CNPJs as bare digits; the informe stores them punctuated. Normalise to digits and
    # carry both, so a join can use either. Observed 2026-09-11: 98.7% of live informe classes match.
    merged["cnpj_digits"] = merged[KEY].astype(str).str.replace(r"\D", "", regex=True)
    return merged
