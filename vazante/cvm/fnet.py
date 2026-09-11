"""Fundos.NET client — regulamento, DFs with parecer, atas, convocações, fatos relevantes, comunicados, lâmina.

Public document manager: https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM (reachable 2026-09-11).
The pre-exclusivity pack needs, per fund: the regulamento (disposal authority, coobrigação clause, eligibility, assembly
quorum), the last two DFs and pareceres, twelve months of atas and fatos relevantes, and the lâmina (top-5 devedores and
coobrigados by name). Filter (i) of the screen — class closed for redemptions — comes from here.

STATUS: not built (BACKLOG #6). Every fetch goes through vazante.oracle.evidence.pull() so the pack can cite it.
"""
from __future__ import annotations

from pathlib import Path

FNET_BASE = "https://fnet.bmfbovespa.com.br/fnet/publico"
DOCUMENT_TYPES = [
    "regulamento",
    "demonstracoes_contabeis",
    "parecer_auditor",
    "ata_assembleia",
    "convocacao",
    "fato_relevante",
    "comunicado",
    "lamina",
    "informe_mensal_filed",  # the informe as filed — BACKLOG #2 checks whether it names the 25 maiores sacados
]


def list_documents(cnpj: str, months_back: int = 12) -> list[dict]:
    raise NotImplementedError("FNET listing: BACKLOG #6")


def download_document(doc_id: str, dest_dir: Path) -> Path:
    raise NotImplementedError("FNET download through pull(): BACKLOG #6")
