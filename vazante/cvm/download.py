"""Bulk layer — CVM open data for FIDCs. Idempotent, snapshot-aware downloads with a SHA-256 manifest.

The CVM re-publishes each month's informe ZIP as late filers arrive (the 2026-08 file held 664 classes on
2026-09-11 while the filing window was still open), so a month is stored as dated snapshots and never
overwritten: a fund that appears late, or whose numbers move between snapshots, is itself a signal
(business case 2.4, secondary signal "late, restated or omitted informe").

Layout under data/raw/cvm/ — see data/README.md.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from vazante.config import RAW_DIR

BASE = "https://dados.cvm.gov.br/dados"
INF_MENSAL_DIR = f"{BASE}/FIDC/DOC/INF_MENSAL/DADOS/"
INF_MENSAL_HIST = f"{BASE}/FIDC/DOC/INF_MENSAL/DADOS/HIST/"
INF_MENSAL_META = f"{BASE}/FIDC/DOC/INF_MENSAL/META/meta_inf_mensal_fidc_txt.zip"
CAD_FI = f"{BASE}/FI/CAD/DADOS/cad_fi.csv"

CVM_RAW = RAW_DIR / "cvm"
MANIFEST = CVM_RAW / "manifest.jsonl"

_MONTH_RE = re.compile(r"inf_mensal_fidc_(\d{6})\.zip")
_YEAR_RE = re.compile(r"inf_mensal_fidc_(\d{4})\.zip")
_TIMEOUT = (30, 600)
_HEADERS = {"User-Agent": "vazante-desk/0.1"}
_DESK_TZ = ZoneInfo("America/Sao_Paulo")


def _today() -> str:
    """Snapshot dates are the desk's calendar day, not the container's."""
    return datetime.now(_DESK_TZ).date().isoformat()


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_rows() -> list[dict]:
    if not MANIFEST.exists():
        return []
    with open(MANIFEST, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _record(row: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def remote_last_modified(url: str) -> str | None:
    r = requests.head(url, headers=_HEADERS, timeout=_TIMEOUT, allow_redirects=True)
    r.raise_for_status()
    return r.headers.get("Last-Modified")


def download(url: str, dest: Path) -> Path:
    """Streaming download to a temp file, atomic rename, manifest line with SHA-256."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    with requests.get(url, headers=_HEADERS, timeout=_TIMEOUT, stream=True) as r:
        r.raise_for_status()
        last_mod = r.headers.get("Last-Modified")
        with open(tmp, "wb") as f:
            f.writelines(r.iter_content(1 << 20))
    tmp.replace(dest)
    _record(
        {
            "url": url,
            "path": str(dest.relative_to(RAW_DIR)),
            "sha256": sha256_of(dest),
            "bytes": dest.stat().st_size,
            "fetched_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "last_modified": last_mod,
        }
    )
    return dest


def list_available_months() -> list[str]:
    """Months the CVM has published, ascending, as 'YYYYMM'."""
    r = requests.get(INF_MENSAL_DIR, headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    return sorted(set(_MONTH_RE.findall(r.text)))


def latest_snapshot(month: str) -> Path | None:
    d = CVM_RAW / "inf_mensal" / month
    snaps = sorted(d.glob("fetched-*.zip")) if d.exists() else []
    return snaps[-1] if snaps else None


def fetch_informe(month: str, force: bool = False) -> Path:
    """One month's informe ZIP as a dated snapshot. Skipped when the remote Last-Modified is already on file."""
    url = f"{INF_MENSAL_DIR}inf_mensal_fidc_{month}.zip"
    current = latest_snapshot(month)
    if current and not force:
        known = {row.get("last_modified") for row in manifest_rows() if row.get("url") == url}
        remote = remote_last_modified(url)
        if remote and remote in known:
            return current
    dest = CVM_RAW / "inf_mensal" / month / f"fetched-{_today()}.zip"
    if dest.exists() and not force:
        return dest
    return download(url, dest)


def fetch_informe_range(months_back: int = 24, end: str | None = None, force: bool = False) -> list[Path]:
    """The last `months_back` published months (24 = the reconstruction window of business case 2.4)."""
    months = list_available_months()
    if end:
        months = [m for m in months if m <= end]
    return [fetch_informe(m, force=force) for m in months[-months_back:]]


def fetch_meta(force: bool = False) -> Path:
    dest = CVM_RAW / "meta" / "meta_inf_mensal_fidc_txt.zip"
    if dest.exists() and not force:
        return dest
    return download(INF_MENSAL_META, dest)


def fetch_cad_fi(force: bool = False) -> Path:
    dest = CVM_RAW / "cad_fi" / f"cad_fi_{_today()}.csv"
    if dest.exists() and not force:
        return dest
    return download(CAD_FI, dest)


def informe_members(zip_path: Path) -> list[str]:
    with zipfile.ZipFile(zip_path) as z:
        return sorted(z.namelist())


def informe_headers(zip_path: Path) -> dict[str, list[str]]:
    """Header row of every CSV member (latin-1, ';'). The raw side of the mapping freeze (docs/BACKLOG.md #1)."""
    out: dict[str, list[str]] = {}
    with zipfile.ZipFile(zip_path) as z:
        for name in sorted(z.namelist()):
            with z.open(name) as f:
                out[name] = f.readline().decode("latin-1").rstrip("\r\n").split(";")
    return out


def list_available_years() -> list[str]:
    """Years archived under DADOS/HIST/ (the CVM keeps only the current and prior year as monthly files)."""
    r = requests.get(INF_MENSAL_HIST, headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    return sorted(set(_YEAR_RE.findall(r.text)))


def fetch_informe_year(year: str, force: bool = False) -> Path:
    """One year's archive. Contains that year's twelve monthly ZIPs, each holding the usual CSV members."""
    dest = CVM_RAW / "inf_mensal_hist" / f"inf_mensal_fidc_{year}.zip"
    if dest.exists() and not force:
        return dest
    return download(f"{INF_MENSAL_HIST}inf_mensal_fidc_{year}.zip", dest)


def expand_year_archive(year: str) -> list[Path]:
    """Unpack a year archive into the same dated-snapshot layout the monthly downloads use.

    The year archives hold the CSV members directly (inf_mensal_fidc_tab_<T>_<YYYYMM>.csv), not nested monthly
    ZIPs, so the members are regrouped by competency month into one ZIP per month.
    """
    archive = fetch_informe_year(year)
    by_month: dict[str, list[str]] = {}
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            m = re.search(r"_(\d{6})\.csv$", name)
            if m:
                by_month.setdefault(m.group(1), []).append(name)
        out: list[Path] = []
        for month, members in sorted(by_month.items()):
            dest = CVM_RAW / "inf_mensal" / month / f"fetched-{_today()}.zip"
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as out_zip:
                    for member in sorted(members):
                        out_zip.writestr(Path(member).name, z.read(member))
            out.append(dest)
    return sorted(out)
