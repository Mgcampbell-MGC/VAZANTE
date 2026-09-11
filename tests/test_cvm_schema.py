import zipfile

from vazante.cvm.download import informe_headers
from vazante.cvm.schema import MappingNotFrozen, load_mapping, member_name, month_from_path, read_table


def _fixture_zip(tmp_path):
    p = tmp_path / "202608" / "fetched-2026-09-11.zip"
    p.parent.mkdir()
    with zipfile.ZipFile(p, "w") as z:
        z.writestr(
            member_name("VIII", "202608"),
            "TP_FUNDO_CLASSE;CNPJ_FUNDO_CLASSE;DENOM_SOCIAL;DT_COMPTC;SEQUENCIAL;VALOR\r\n"
            "Classe;09.260.031/0001-56;FIDC NP SRM;2026-08-31;1;0.00\r\n".encode("latin-1"),
        )
    return p


def test_month_from_path_and_read_table(tmp_path):
    p = _fixture_zip(tmp_path)
    assert month_from_path(p) == "202608"
    df = read_table(p, "VIII")
    assert list(df.columns)[-2:] == ["SEQUENCIAL", "VALOR"]
    assert df.iloc[0]["CNPJ_FUNDO_CLASSE"] == "09.260.031/0001-56"
    assert informe_headers(p)[member_name("VIII", "202608")][-1] == "VALOR"


def test_mapping_not_frozen():
    try:
        load_mapping()
    except MappingNotFrozen:
        return
    # if a mapping exists, it must at least declare concepts
    assert "concepts" in load_mapping()
