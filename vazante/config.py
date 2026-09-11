"""Paths and configuration. Thresholds live in config/thresholds.yaml, never in code."""
from __future__ import annotations

import os
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
DOCS_DIR = REPO_ROOT / "docs"
DATA_ROOT = Path(os.environ.get("VAZANTE_DATA_ROOT", REPO_ROOT / "data"))
RAW_DIR = DATA_ROOT / "raw"
DERIVED_DIR = DATA_ROOT / "derived"
EVIDENCE_DIR = DATA_ROOT / "evidence"
DEALS_DIR = DATA_ROOT / "deals"
BIDS_DIR = DATA_ROOT / "bids"


def load_yaml(name: str) -> dict:
    with open(CONFIG_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def thresholds() -> dict:
    return load_yaml("thresholds.yaml")


def sources() -> dict:
    return load_yaml("sources.yaml")


def ensure_dirs() -> None:
    for d in (RAW_DIR, DERIVED_DIR, EVIDENCE_DIR, DEALS_DIR, BIDS_DIR):
        d.mkdir(parents=True, exist_ok=True)
