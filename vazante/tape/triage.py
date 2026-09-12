"""Day-one triage: a tape in, a decision out, in hours and at no cost.

Three things happen here, in this order, because the cheapest test comes first.

1. RECONCILE against the fund's own CVM informe. Face against reported carteira, provision against reported
   provision, ageing bands against Tabelas V and VI. A tape that does not reconcile to the fund's own regulatory
   filing is the most important thing that can be learned on day one, and it costs nothing.
2. SWEEP, offline, 100% of positions. Check digits, NF-e keys, duplicates, impossible dates, paid-before-assigned.
   No external call, no fee.
3. CARVE. Route every position to the slice whose buyer wants that piece.

Nothing here prices anything. Pricing needs contracted buyer grids, and a grid is not a bid.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from vazante.oracle.sweep import cnpj_root, cnpj_valid, nfe_key_valid
from vazante.tape.schema import Mapping, map_columns

SLICES = ["S1_clean_not_yet_due", "S2_sell_to_debtor", "S3_sell_to_originator",
          "S4_legal_claim", "S5_residual", "S0_zero"]


def load(path: str) -> tuple[pd.DataFrame, Mapping]:
    """Read whatever the seller sent and map its columns. Everything stays text until we decide what it is."""
    if str(path).lower().endswith((".xlsx", ".xlsm")):
        raw = pd.read_excel(path, dtype=str)
    else:
        raw = None
        attempts: list[str] = []
        for enc in ("utf-8-sig", "latin-1"):
            for sep in (";", ",", "\t"):
                try:
                    cand = pd.read_csv(path, sep=sep, dtype=str, encoding=enc, keep_default_na=False)
                except Exception as exc:  # noqa: BLE001 - a failed parse is a fact, not an error
                    attempts.append(f"{enc}/{sep!r}: {exc!r}")
                    continue
                if cand.shape[1] > 1:
                    raw = cand
                    break
            if raw is not None:
                break
        if raw is None:
            raise ValueError(f"could not parse {path} as a delimited file; tried: {attempts}")
    return raw, map_columns(list(raw.columns))


def canonicalise(raw: pd.DataFrame, m: Mapping) -> pd.DataFrame:
    """Rename to canonical names and coerce types. Unmapped seller columns are kept, prefixed, never dropped."""
    df = pd.DataFrame(index=raw.index)
    for canon, col in m.resolved.items():
        df[canon] = raw[col]
    for col in m.unmapped:
        df[f"raw__{col}"] = raw[col]

    for c in ("face", "book_value", "provision", "paid_amount", "days_late"):
        if c in df:
            s = df[c].astype(str).str.strip()
            # Brazilian decimals: 1.234.567,89 -> 1234567.89; leave 1234567.89 alone
            br = s.str.contains(",", na=False)
            s = s.mask(br, s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
            df[c] = pd.to_numeric(s.str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")
    for c in ("issue_date", "due_date", "assignment_date", "payment_date"):
        if c in df:
            df[c] = pd.to_datetime(df[c], errors="coerce", dayfirst=True)
    for c in ("sacado_cnpj", "cedente_cnpj"):
        if c in df:
            df[c] = df[c].astype(str).str.replace(r"\D", "", regex=True).str.zfill(14)
            df[f"{c}_valid"] = df[c].apply(cnpj_valid)
            df[f"{c}_root"] = df[c].apply(cnpj_root)
    return df


@dataclass
class Reconciliation:
    """Tape against the fund's own CVM filing. The cheapest fraud test there is."""

    tape_face: float
    informe_carteira: float
    tape_provision: float | None
    informe_provision: float | None
    face_ratio: float
    provision_ratio: float | None
    positions: int
    verdict: str
    notes: list[str]

    def report(self) -> str:
        out = [f"tape face        R${self.tape_face/1e6:,.2f}m over {self.positions:,} positions",
               f"informe carteira R${self.informe_carteira/1e6:,.2f}m",
               f"ratio            {self.face_ratio:.3f}"]
        if self.provision_ratio is not None:
            out.append(f"provision ratio  {self.provision_ratio:.3f}")
        out.append(f"VERDICT: {self.verdict}")
        out += [f"  - {n}" for n in self.notes]
        return "\n".join(out)


def reconcile(df: pd.DataFrame, informe_carteira: float, informe_provision: float | None = None,
              tolerance: float = 0.05) -> Reconciliation:
    face = float(df["face"].sum(skipna=True)) if "face" in df else float("nan")
    prov = float(df["provision"].abs().sum(skipna=True)) if "provision" in df else None
    ratio = face / informe_carteira if informe_carteira else float("nan")
    pratio = (prov / informe_provision) if (prov is not None and informe_provision) else None
    notes: list[str] = []

    if not np.isfinite(ratio):
        verdict = "CANNOT RECONCILE - no face column or no informe figure"
    elif abs(ratio - 1) <= tolerance:
        verdict = "RECONCILES - the tape is the book the fund reported"
    elif ratio > 1 + tolerance:
        verdict = "TAPE EXCEEDS THE FILING - gross face against a net carteira, or paper the fund did not report"
        notes.append("Ask whether face is gross of provision. If it is not, this is a disclosure problem.")
    else:
        verdict = "TAPE FALLS SHORT OF THE FILING - a partial extract, or the filing is overstated"
        notes.append("Ask for the missing positions before anything else. A partial tape cannot be priced.")
    if pratio is not None and abs(pratio - 1) > 0.10:
        notes.append(f"Provision on the tape is {pratio:.2f}x the filing. One of the two is wrong.")
    return Reconciliation(face, informe_carteira, prov, informe_provision, ratio, pratio, len(df), verdict, notes)


def sweep(df: pd.DataFrame, asof: pd.Timestamp | None = None) -> pd.DataFrame:
    """Tier 0. Every check here is offline and free. Flags are added; nothing is ever deleted."""
    asof = asof or pd.Timestamp.today().normalize()
    f = pd.DataFrame(index=df.index)
    for c in ("sacado_cnpj", "cedente_cnpj"):
        if f"{c}_valid" in df:
            f[f"bad_{c}"] = ~df[f"{c}_valid"].fillna(False)
    if "sacado_cnpj_root" in df and "cedente_cnpj_root" in df:
        f["sacado_is_cedente"] = df.sacado_cnpj_root.eq(df.cedente_cnpj_root) & df.sacado_cnpj_root.ne("")
    if "nfe_key" in df:
        k = df.nfe_key.astype(str).str.replace(r"\D", "", regex=True)
        f["nfe_present"] = k.str.len().eq(44)
        f["nfe_key_invalid"] = f.nfe_present & ~k.apply(nfe_key_valid)
    if {"issue_date", "due_date"} <= set(df):
        f["due_before_issue"] = df.due_date.lt(df.issue_date)
    if {"assignment_date", "payment_date"} <= set(df):
        f["paid_before_assigned"] = df.payment_date.lt(df.assignment_date)
    if {"issue_date", "assignment_date"} <= set(df):
        f["assigned_before_issued"] = df.assignment_date.lt(df.issue_date)
    if "due_date" in df:
        f["due_absurdly_far"] = df.due_date.gt(asof + pd.Timedelta(days=3650))
    if "face" in df:
        f["face_non_positive"] = df.face.le(0)
        cents = (df.face.fillna(0) * 100).round().astype("Int64") % 100
        f["face_round_number"] = cents.eq(0) & df.face.gt(0)
    # duplicates: the same document twice, and the same economics twice
    if "nfe_key" in df:
        k = df.nfe_key.astype(str).str.replace(r"\D", "", regex=True)
        f["dup_nfe_key"] = k.duplicated(keep=False) & k.str.len().eq(44)
    keycols = [c for c in ("sacado_cnpj", "face", "due_date") if c in df]
    if len(keycols) == 3:
        f["dup_economics"] = df.duplicated(subset=keycols, keep=False)
    if {"doc_number", "cedente_cnpj"} <= set(df):
        f["dup_doc_per_cedente"] = df.duplicated(subset=["cedente_cnpj", "doc_number"], keep=False) & \
            df.doc_number.astype(str).str.strip().ne("")
    f = f.fillna(False)
    f["n_flags"] = f.sum(axis=1)
    return f


def carve(df: pd.DataFrame, flags: pd.DataFrame, asof: pd.Timestamp | None = None) -> pd.Series:
    """Route each position to the buyer who wants that piece.

    Order matters: a hard structural defect outranks the ageing band, and evidenced recourse outranks the tail,
    because a claim against a solvent originator is worth more than the same paper sold as tonnage.
    """
    asof = asof or pd.Timestamp.today().normalize()
    n = len(df)
    out = pd.Series(["S5_residual"] * n, index=df.index)

    dpd = (asof - df.due_date).dt.days if "due_date" in df else pd.Series(np.nan, index=df.index)
    if "days_late" in df:
        dpd = dpd.fillna(df.days_late)

    recourse = pd.Series(False, index=df.index)
    if "recourse_flag" in df:
        recourse = df.recourse_flag.astype(str).str.upper().str.strip().isin(
            {"S", "SIM", "Y", "YES", "TRUE", "1", "COM COOBRIGACAO", "COOBRIGADO"})

    legal = pd.Series(False, index=df.index)
    for c in ("legal_flag", "protest_flag"):
        if c in df:
            legal |= df[c].astype(str).str.upper().str.strip().isin({"S", "SIM", "Y", "YES", "TRUE", "1"})

    hard_defect = flags.get("sacado_is_cedente", pd.Series(False, index=df.index)) | \
        flags.get("nfe_key_invalid", pd.Series(False, index=df.index)) | \
        flags.get("bad_sacado_cnpj", pd.Series(False, index=df.index)) | \
        flags.get("dup_nfe_key", pd.Series(False, index=df.index)) | \
        flags.get("face_non_positive", pd.Series(False, index=df.index))

    out[dpd.gt(360).fillna(False)] = "S5_residual"
    out[dpd.between(1, 360).fillna(False)] = "S2_sell_to_debtor"
    out[dpd.le(0).fillna(False)] = "S1_clean_not_yet_due"
    out[recourse & dpd.gt(0).fillna(False)] = "S3_sell_to_originator"
    out[legal] = "S4_legal_claim"
    out[hard_defect] = "S0_zero"
    return out


def summarise(df: pd.DataFrame, slices: pd.Series) -> pd.DataFrame:
    """Face and position count per slice, in the order a bid sheet reads."""
    g = pd.DataFrame({"slice": slices, "face": df.get("face", pd.Series(np.nan, index=df.index))})
    s = g.groupby("slice").agg(positions=("face", "size"), face=("face", "sum"))
    s = s.reindex(SLICES).fillna(0)
    s["pct_of_face"] = (s.face / s.face.sum() * 100).round(1) if s.face.sum() else 0.0
    s["face_Rm"] = (s.face / 1e6).round(2)
    return s[["positions", "face_Rm", "pct_of_face"]]
