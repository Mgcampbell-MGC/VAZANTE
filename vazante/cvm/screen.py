"""The screen that finds Deal 1 (business case Part 3.6). Five filters over two public datasets.

  (i)   class closed for redemptions more than five business days — the art. 44 §3 trigger, disclosed on
        Fundos.NET as a fato relevante or comunicado (needs the FNET client)
  (ii)  PDD >= 25% of carteira in the latest informe — the loss is already booked
  (iii) >= 60% of carteira in industrial + comercial direitos creditórios
  (iv)  PL >= R$85m (R$100m preferred)
  (v)   gestor CNPJ still active and distinct from the administrador (cad_fi)

Output: the calling list, ranked by the BREAK-FLAG conjunction rule. Packs are built only for the top three to five
GC can actually call that week. Also the fund-versus-class filing test on 200 funds (Tabela VIII Σ Valor / PL vs Σ %PL —
3× error if wrong) and the one bulk query that converts the supply count from ASSUMPTION to VERIFIED: join twelve
informes to cad_fi ADMIN, filter to the Trustee / Banvox / Reag / CBSF / Master administrators, bucket by segment
share, PL, PDD share and recompra share.
"""
from __future__ import annotations

from dataclasses import dataclass, fields

import pandas as pd

from vazante.config import thresholds
from vazante.cvm.schema import load_mapping


@dataclass(frozen=True)
class ScreenParams:
    closed_for_redemptions_business_days_min: int
    pdd_share_of_carteira_min: float
    industrial_plus_comercial_share_min: float
    pl_min_brl: float
    pl_preferred_brl: float
    gestor_must_be_active_and_distinct_from_admin: bool

    @classmethod
    def from_config(cls) -> ScreenParams:
        t = thresholds()["screen"]
        return cls(**{f.name: t[f.name] for f in fields(cls)})


def run_screen(month: str, params: ScreenParams | None = None) -> pd.DataFrame:
    """Calling list for one competência month. Columns: cnpj, denominação, administrador, gestor, PL, PDD share,
    segment share, closed-for-redemptions (bool, date), break-flag rank."""
    load_mapping()  # MappingNotFrozen until BACKLOG #1
    raise NotImplementedError("screen: build after the mapping freeze (BACKLOG #1) and the FNET client (BACKLOG #6)")


def supply_count(months: list[str], administrators: list[str]) -> pd.DataFrame:
    """The bulk query of business case 3.4 — executable situations by lineage administrator."""
    load_mapping()
    raise NotImplementedError
