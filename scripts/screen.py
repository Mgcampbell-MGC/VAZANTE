"""Run the Part 3.6 screen on the last complete month and print the calling list.

Filter (i), the class closed for redemptions for more than five business days, needs Fundos.NET and is not yet
built; `resgates_solicitados` outstanding is carried as a weak proxy and reported separately, never as the filter.
"""
from __future__ import annotations

import pandas as pd

from vazante.config import DERIVED_DIR, thresholds
from vazante.cvm.panel import load_registro

pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 44)
KEY = "CNPJ_FUNDO_CLASSE"


def digits(s: pd.Series) -> pd.Series:
    return s.astype(str).str.replace(r"\D", "", regex=True)


def run(month: str = "202607") -> pd.DataFrame:
    t = thresholds()["screen"]
    d = pd.read_parquet(DERIVED_DIR / "indicators.parquet")
    cur = d[d.month == month].copy()
    reg = load_registro()
    reg_cols = ["cnpj_digits", "Gestor", "CPF_CNPJ_Gestor", "Administrador", "CNPJ_Administrador",
                "Diretor", "Situacao_classe", "Situacao_fundo", "Tipo_Fundo", "Entidade_Investimento",
                "Forma_Condominio", "Publico_Alvo"]
    cur["cnpj_digits"] = digits(cur[KEY])
    cur = cur.merge(reg[reg_cols].drop_duplicates("cnpj_digits"), on="cnpj_digits", how="left")

    cur["f_pdd"] = cur.pdd_share_carteira >= t["pdd_share_of_carteira_min"]
    cur["f_seg"] = cur.ind_com_share >= t["industrial_plus_comercial_share_min"]
    cur["f_pl"] = cur.pl >= t["pl_min_brl"]
    cur["f_gestor"] = cur.Gestor.notna() & (
        digits(cur.CPF_CNPJ_Gestor.fillna("")) != digits(cur.CNPJ_Administrador.fillna("~")))
    cur["f_fidc"] = cur.Tipo_Fundo.eq("FIDC")
    return cur


if __name__ == "__main__":
    cur = run()
    print(f"population at 202607: {len(cur):,} classes | register matched {cur.Gestor.notna().mean():.1%}\n")
    print("=== funnel ===")
    mask = pd.Series(True, index=cur.index)
    for label, col in [("FIDC (register type)", "f_fidc"),
                       ("(ii)  PDD >= 25% of carteira", "f_pdd"),
                       ("(iii) industrial+comercial >= 60%", "f_seg"),
                       ("(iv)  PL >= R$85m", "f_pl"),
                       ("(v)   gestor present, distinct from admin", "f_gestor")]:
        mask &= cur[col]
        print(f"  {label:44s} alone {cur[col].sum():5d}   cumulative {mask.sum():5d}")
    core = cur[mask].copy()
    print(f"\n=== CALLING LIST: {len(core)} classes (filter (i) deferred to Fundos.NET) ===")
    core["PL_Rm"] = (core.pl / 1e6).round(0)
    core["cart_Rm"] = (core.carteira / 1e6).round(0)
    core["PDD%"] = (core.pdd_share_carteira * 100).round(1)
    core["ind+com%"] = (core.ind_com_share * 100).round(1)
    core["180+%"] = (core.inad_180_share * 100).round(1)
    out = core[["DENOM_SOCIAL", "Administrador", "Gestor", "Situacao_classe", "PL_Rm", "cart_Rm",
                "PDD%", "ind+com%", "180+%", "resg_solicitado_outstanding"]].sort_values("PL_Rm", ascending=False)
    print(out.to_string(index=False))
    out.to_csv(DERIVED_DIR / "calling_list_202607.csv", index=False)
    print(f"\nsaved -> {DERIVED_DIR / 'calling_list_202607.csv'}")
    print("\n=== classes already in liquidação (archetype B), any size ===")
    liq = cur[cur.Situacao_classe.eq("Em Liquidação") & cur.f_fidc]
    print(f"  {len(liq)} FIDC classes in liquidação, R${liq.pl.sum()/1e9:.2f}bn PL; "
          f"{(liq.pdd_share_carteira >= 0.25).sum()} of them with PDD >= 25%")
