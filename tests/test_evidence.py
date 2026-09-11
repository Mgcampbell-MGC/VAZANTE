import json

from vazante.oracle.evidence import load_pulls, pull
from vazante.oracle.states import OracleResultState


def test_pull_stores_raw_and_record(tmp_path):
    rec = pull(
        "minha_receita",
        "cnpj",
        {"cnpj": "33000167000101"},
        lambda: (b'{"razao_social": "PETROBRAS"}', OracleResultState.FOUND_POSITIVE),
        parser=lambda raw: json.loads(raw),
        store=tmp_path,
        deal_id="DEAL0",
    )
    assert rec.status == OracleResultState.FOUND_POSITIVE
    assert rec.parsed["razao_social"] == "PETROBRAS"
    assert (tmp_path / rec.raw_path).exists()
    assert len(rec.raw_sha256) == 64
    assert load_pulls(tmp_path)[0].pull_id == rec.pull_id


def test_pull_failure_is_never_no_record(tmp_path):
    def boom():
        raise ConnectionError("reset by peer")

    rec = pull("djen", "party", {"name": "x"}, boom, store=tmp_path, max_retries=1)
    assert rec.status == OracleResultState.SOURCE_UNAVAILABLE
    assert rec.failed
    assert len(rec.retries) == 2
