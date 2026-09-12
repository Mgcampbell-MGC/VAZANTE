"""Regression anchors for the lot carve.

The carve is what a first call carries, so the arithmetic has to hold and the
flags have to fire.  These lock the bucket definitions and the two boundaries
the informe reports directly.
"""

import pandas as pd

from vazante.lots import LOTS, carve_fund, carve_universe


def _row(**kw):
    base = {
        "CNPJ_FUNDO_CLASSE": "00.000.000/0001-00",
        "DENOM_SOCIAL": "TESTE FIDC",
        "carteira": 100.0,
        "pdd": 30.0,
        "cred_a_vencer": 80.0,
        "cred_a_vencer_com_parcela_inad": 5.0,
        "cred_inadimplentes": 30.0,
        "inad_total": 40.0,
        "inad_90_mais": 25.0,
        "inad_180_mais": 15.0,
        "cred_empresa_recuperacao": 0.0,
        "dircred_com_risco": 20.0,
        "dircred_sem_risco": 60.0,
        "n_ced": 3,
        "n_rj": 0,
        "cotistas": 1.0,
    }
    base.update(kw)
    return pd.Series(base)


def test_lot_vocabulary_is_stable():
    assert [lot.key for lot in LOTS] == ["A", "B", "C", "D", "E", "F"]


def test_buckets_partition_the_ageing():
    c = carve_fund(_row())
    assert c.buckets["A"] == 80.0  # I.2.a.1/b.1 is already "a vencer e adimplentes"
    assert c.buckets["A2"] == 5.0  # the impaired block is a separate item, not a subset
    assert c.buckets["B"] == 15.0  # inad_total - inad_90_mais
    assert c.buckets["C"] == 10.0  # inad_90_mais - inad_180_mais
    assert c.buckets["D"] == 15.0
    assert c.buckets["B"] + c.buckets["C"] + c.buckets["D"] == 40.0


def test_recourse_semantics_are_not_inverted():
    """The CVM split is *aquisicao substancial dos riscos*, not recourse.

    com_risco means the FUND took the loss, so that paper is a true sale with no
    recourse.  sem_risco means the risk stayed with the cedente, which is where
    the recourse lives.  This module had it backwards on 12 September 2026 and
    the error reversed the buyer for three quarters of the book.  Do not "fix"
    this test by swapping it back.
    """
    c = carve_fund(_row(dircred_com_risco=20.0, dircred_sem_risco=60.0))
    assert c.true_sale_face == 20.0, "com_risco is the TRUE SALE block"
    assert c.recourse_face == 60.0, "sem_risco is the block that CARRIES recourse"
    assert c.recourse_share == 0.75


def test_gross_face_ties_to_tabela_i_and_does_not_double_count_recovery():
    """Bucket E is a status overlay, also counted in B/C/D. Summing buckets
    double-counts it, so gross face comes from Tabela I instead."""
    c = carve_fund(_row(cred_empresa_recuperacao=7.0))
    assert c.gross_face == 80.0 + 5.0 + 30.0  # a vencer + impaired + inadimplentes
    assert c.buckets["E"] == 7.0
    assert c.gross_face != sum(c.buckets.values())


def test_age_ladder_disagreeing_with_tabela_i_is_flagged():
    # inad_total 40 from the age ladder vs cred_inadimplentes 30 from Tabela I
    c = carve_fund(_row())
    assert any("age ladder and Tabela I disagree" in f for f in c.flags)
    tied = carve_fund(_row(inad_total=30.0, inad_90_mais=20.0, inad_180_mais=10.0))
    assert not any("disagree" in f for f in tied.flags)


def test_missing_recourse_split_is_flagged_not_guessed():
    c = carve_fund(_row(dircred_com_risco=0.0, dircred_sem_risco=0.0))
    assert c.recourse_share is None
    assert any("recourse split not reported" in f for f in c.flags)


def test_ageing_is_never_crossed_against_recourse_silently():
    c = carve_fund(_row())
    assert any("not crossed against recourse" in f for f in c.flags)


def test_single_signature_ceiling_flags_the_slow_lots():
    c = carve_fund(_row(), single_signature_ceiling=20.0)
    assert any(f.startswith("lots above one signature: A") for f in c.flags)
    small = carve_fund(_row(), single_signature_ceiling=1_000.0)
    assert not any("above one signature" in f for f in small.flags)


def test_unmarked_recovery_claim_is_flagged():
    c = carve_fund(_row(n_rj=2, cred_empresa_recuperacao=0.0))
    assert any("may sit unmarked" in f for f in c.flags)


def test_heavy_provision_against_a_performing_book_is_flagged():
    c = carve_fund(_row(pdd=60.0))
    assert any("over-provisioned or about to migrate" in f for f in c.flags)


def test_carve_universe_is_one_row_per_fund():
    df = pd.DataFrame([_row(), _row(DENOM_SOCIAL="OUTRO FIDC")])
    out = carve_universe(df)
    assert len(out) == 2
    assert out["lot_A"].tolist() == [80.0, 80.0]
    assert out["gross_face"].tolist() == [115.0, 115.0]


def test_carve_never_produces_a_price():
    c = carve_fund(_row())
    row = c.as_row()
    assert not any("price" in k or "value" in k or "bid" in k for k in row)
