"""Environment report: what is installed, where data lives, which sources answer."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data"

PACKAGES = ["pandas", "numpy", "scipy", "pyarrow", "duckdb", "requests", "httpx", "lxml", "pydantic", "yaml", "networkx"]


def report() -> None:
    print(f"python  {sys.version.split()[0]}")
    print(f"repo    {REPO_ROOT}")
    print(f"data    {DATA_ROOT}  ({'exists' if DATA_ROOT.exists() else 'missing'})")
    for name in PACKAGES:
        try:
            mod = importlib.import_module(name)
            print(f"  {name:12s} {getattr(mod, '__version__', 'ok')}")
        except Exception:  # noqa: BLE001
            print(f"  {name:12s} MISSING")
