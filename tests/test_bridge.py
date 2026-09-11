from vazante.oracle.bridge import ForensicBridge


def test_bridge_reconciles():
    b = ForensicBridge(200, 195, 160, 150, 140, 130, 120)
    assert b.reconciled()
    assert b.zero_unresolved == 80
    assert [d for _, _, d in b.steps()] == [5, 35, 10, 10, 10, 10]
    assert b.as_rows()[-1] == {"stage": "zero_unresolved", "face": 80}


def test_bridge_flags_increase():
    b = ForensicBridge(200, 195, 196, 150, 140, 130, 120)
    assert not b.reconciled()
    assert any("existence_supported" in p for p in b.problems())
