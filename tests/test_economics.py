import pytest

from vazante.economics.reference_book import (
    REFERENCE_C,
    REFERENCE_L,
    REFERENCE_T1,
    bid_at_gross_contribution,
    max_bid,
    reference_trade,
)


def test_reference_book_reproduces_part_7_1():
    t = reference_trade()
    assert t.max_bid == pytest.approx(9.679, abs=0.003)
    assert t.tax == pytest.approx(1.370, abs=0.003)
    assert t.basis == pytest.approx(11.627, abs=0.003)
    assert t.gross_contribution == pytest.approx(3.695, abs=0.003)
    assert t.after_tax_contribution == pytest.approx(2.325, abs=0.002)
    assert t.after_tax_contribution == pytest.approx(REFERENCE_L / 6, abs=0.001)  # = L ÷ 6 by construction
    assert REFERENCE_L / t.basis == pytest.approx(1.20, abs=0.001)
    assert t.payout_ratio == pytest.approx(0.735, abs=0.002)  # "≈73¢ per R$1 of FIRM proceeds"


@pytest.mark.parametrize(
    "tax_rate, expected",
    [(0.371, 9.68), (0.15, 10.64), (0.40, 9.49), (0.517, 8.56)],  # T1, FIDC wrapper, T2 factoring, T3 adverse
)
def test_tax_as_a_bidding_variable(tax_rate, expected):
    assert max_bid(REFERENCE_L, REFERENCE_C, tax_rate) == pytest.approx(expected, abs=0.02)


@pytest.mark.parametrize(
    "L, expected_bid",
    [(12.25, 8.43), (13.25, 9.16), (13.54, 9.38)],  # Premium −20%; residual grid −1¢; 20% of Claims fails pre-bid
)
def test_sensitivity_table(L, expected_bid):
    assert max_bid(L, REFERENCE_C, REFERENCE_T1) == pytest.approx(expected_bid, abs=0.01)


def test_hurdle_alone_would_allow_11_87():
    assert bid_at_gross_contribution(REFERENCE_L, REFERENCE_C, 1.5) == pytest.approx(11.875, abs=0.001)
