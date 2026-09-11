from vazante.cvm.schema import column, load_mapping

REQUIRED = [
    "carteira", "pdd", "pl", "recompras", "recompras_contabil", "substituicoes",
    "alienacoes_ao_cedente", "alienacoes_a_terceiros", "aquisicoes_com_risco",
    "inad_total", "inad_90_mais", "inad_180_mais", "a_vencer_total", "pagos_antecipadamente",
    "seg_industrial", "seg_comercial", "carteira_segmento", "administrador_nome",
    "rentabilidade_mes", "resgates_solicitados", "maiores_sacados_valor",
]


def test_mapping_is_frozen_and_complete():
    m = load_mapping()
    assert m["version"] == 1 and m["frozen_on"] == "2026-09-11"
    for concept in REQUIRED:
        assert concept in m["concepts"], f"{concept} missing from the frozen mapping"


def test_pdd_is_the_provision_not_a_cedente():
    """Business case 2.1 called a.11/b.11 a cedente name. It is the provision; the cedentes are a.12/b.12."""
    spec = load_mapping()["concepts"]["pdd"]
    assert spec["columns"] == ["TAB_I2A11_VL_REDUCAO_RECUP", "TAB_I2B11_VL_REDUCAO_RECUP"]
    ced = load_mapping()["concepts"]["cedentes_com_risco"]
    assert all("A12" in c for c in ced["columns"])


def test_recompra_concepts_resolve():
    assert column("recompras") == ("VII", "TAB_VII_D_2_VL_RECOMPRA")
    assert column("recompras_contabil") == ("VII", "TAB_VII_D_3_VL_CONTAB_RECOMPRA")


def test_tabela_viii_has_no_sacado_identity():
    """Guard the finding: if the CVM ever publishes identities, this test fails and the D engine can be rebuilt."""
    spec = load_mapping()["concepts"]["maiores_sacados_valor"]
    assert spec["column"] == "VALOR" and spec["label"] == "SEQUENCIAL"
    assert "no CPF/CNPJ" in spec["note"]
