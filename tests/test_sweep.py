from vazante.oracle.sweep import (
    cnpj_check_digits,
    cnpj_root,
    cnpj_valid,
    cpf_valid,
    nfe_key_check_digit,
    nfe_key_parse,
    nfe_key_valid,
)


def test_cpf():
    assert cpf_valid("111.444.777-35")
    assert not cpf_valid("111.444.777-36")
    assert not cpf_valid("111.111.111-11")
    assert not cpf_valid("123")


def test_cnpj_numeric():
    assert cnpj_valid("33.000.167/0001-01")  # Petrobras
    assert cnpj_valid("00.000.000/0001-91")  # Banco do Brasil
    assert not cnpj_valid("33.000.167/0001-02")
    assert not cnpj_valid("11.111.111/1111-11")


def test_cnpj_alphanumeric_official_example():
    # Receita Federal's published example for the alphanumeric CNPJ: 12.ABC.345/01DE-35
    assert cnpj_check_digits("12ABC34501DE") == "35"
    assert cnpj_valid("12.ABC.345/01DE-35")
    assert not cnpj_valid("12.ABC.345/01DE-36")


def test_cnpj_root():
    assert cnpj_root("33.000.167/0001-01") == "33000167"


def _reference_dv(first43: str) -> int:
    # independent implementation: explicit weight list built left-to-right
    weights = []
    w = 2
    for _ in range(43):
        weights.append(w)
        w = 2 if w == 9 else w + 1
    weights.reverse()
    total = sum(int(c) * w for c, w in zip(first43, weights))
    r = total % 11
    return 0 if r < 2 else 11 - r


def test_nfe_key_roundtrip():
    first43 = "35" + "2601" + "33000167000101" + "55" + "001" + "000000001" + "1" + "12345678"
    assert len(first43) == 43
    dv = nfe_key_check_digit(first43)
    assert dv == _reference_dv(first43)
    key = first43 + str(dv)
    assert nfe_key_valid(key)
    assert not nfe_key_valid(first43 + str((dv + 1) % 10))
    parsed = nfe_key_parse(key)
    assert parsed["uf"] == "SP"
    assert parsed["issue_year"] == 2026 and parsed["issue_month"] == 1
    assert parsed["cnpj_emitente"] == "33000167000101" and parsed["cnpj_emitente_valid"]
    assert parsed["modelo_nome"] == "NF-e" and parsed["serie"] == 1 and parsed["nNF"] == 1
    assert parsed["dv_ok"] and parsed["uf_ok"] and parsed["month_ok"]
