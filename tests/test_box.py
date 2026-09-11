from vazante.buyers.box import BOXES_DIR, load_all_boxes, load_box
from vazante.oracle.states import PriceStatus


def test_example_box_loads_and_has_no_firm_lines():
    box = load_box(BOXES_DIR / "SRM_EMPIRICA.v0.example.yaml")
    assert box.buyer == "SRM_EMPIRICA" and box.role.value == "PREMIUM"
    assert box.firm_lines() == []  # a grid is a price list, not a bid
    assert all(p.status == PriceStatus.GRID for p in box.pricing)
    assert "title_conflict" in box.rejects()
    assert box.hard_filters["related_party_flag"].action == "manual_review"
    assert box.pricing[0].price_per_face == 0.75  # A01 — the S1 test


def test_all_boxes_validate():
    assert len(load_all_boxes()) >= 1
