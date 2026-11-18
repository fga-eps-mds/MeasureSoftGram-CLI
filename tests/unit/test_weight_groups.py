import copy

import pytest
from staticfiles import DEFAULT_PRE_CONFIG

from src.cli.resources.weight_groups import (
    InvalidGroupPath,
    apply_weights,
    find_group,
    list_groups,
)


@pytest.fixture
def config():
    return copy.deepcopy(DEFAULT_PRE_CONFIG)


# ---------------------------------------------------------------- list_groups


def test_modelo_padrao_tem_oito_grupos_na_ordem_do_prototipo(config):
    assert [g.path for g in list_groups(config)] == [
        "characteristics",
        "reliability/subcharacteristics",
        "reliability/testing_status/measures",
        "reliability/maturity/measures",
        "maintainability/subcharacteristics",
        "maintainability/modifiability/measures",
        "functional_suitability/subcharacteristics",
        "functional_suitability/functional_completeness/measures",
    ]


def test_rotulos_dos_grupos(config):
    labels = {g.path: g.label for g in list_groups(config)}
    assert labels["characteristics"] == "Características"
    assert (
        labels["reliability/subcharacteristics"] == "reliability › subcaracterísticas"
    )
    assert (
        labels["reliability/testing_status/measures"]
        == "reliability › testing_status › medidas"
    )


def test_entidades_e_pesos_atuais_na_ordem_do_arquivo(config):
    grupo = list_groups(config)[2]
    assert grupo.entities == ["passed_tests", "test_builds", "test_coverage"]
    assert grupo.weights == {"passed_tests": 33, "test_builds": 33, "test_coverage": 34}


def test_resumo_do_cabecalho_do_prototipo(config):
    groups = list_groups(config)
    com_perguntas = [g for g in groups if len(g.entities) > 1]
    assert len(groups) == 8
    assert len(com_perguntas) == 4
    assert sum(g.comparisons for g in groups) == 13


def test_grupos_refletem_o_arquivo_no_momento(config):
    # Cenário 8: medida removida à mão
    sub = config["characteristics"][1]["subcharacteristics"][0]
    sub["measures"] = [m for m in sub["measures"] if m["key"] != "technical_debt_ratio"]
    grupo = find_group(list_groups(config), "maintainability/modifiability/measures")
    assert grupo.entities == [
        "non_complex_file_density",
        "commented_file_density",
        "duplication_absense",
    ]
    assert grupo.comparisons == 3


def test_list_groups_nao_altera_o_config(config):
    antes = copy.deepcopy(config)
    list_groups(config)
    assert config == antes


# ---------------------------------------------------------------- find_group


def test_find_group_por_caminho(config):
    grupo = find_group(list_groups(config), "reliability/subcharacteristics")
    assert grupo.entities == ["testing_status", "maturity"]


def test_caminho_invalido_lista_os_caminhos_validos(config):
    with pytest.raises(InvalidGroupPath) as erro:
        find_group(list_groups(config), "reliability/inexistente")
    assert "reliability/subcharacteristics" in erro.value.valid_paths
    assert len(erro.value.valid_paths) == 8


# ---------------------------------------------------------------- apply_weights


def test_apply_weights_muda_so_o_campo_weight(config):
    novo = apply_weights(
        config,
        {
            "characteristics": {
                "reliability": 43,
                "maintainability": 43,
                "functional_suitability": 14,
            }
        },
    )
    assert [c["weight"] for c in novo["characteristics"]] == [43, 43, 14]

    # tirando o weight das características, todo o resto é idêntico
    for c in novo["characteristics"]:
        c["weight"] = None
    esperado = copy.deepcopy(config)
    for c in esperado["characteristics"]:
        c["weight"] = None
    assert novo == esperado


def test_apply_weights_em_medidas(config):
    novo = apply_weights(
        config,
        {
            "reliability/testing_status/measures": {
                "passed_tests": 65,
                "test_builds": 7,
                "test_coverage": 28,
            }
        },
    )
    medidas = novo["characteristics"][0]["subcharacteristics"][0]["measures"]
    assert [m["weight"] for m in medidas] == [65, 7, 28]
    assert (
        medidas[0]["min_threshold"]
        == config["characteristics"][0]["subcharacteristics"][0]["measures"][0][
            "min_threshold"
        ]
    )


def test_apply_weights_nao_altera_o_original_nem_outros_grupos(config):
    antes = copy.deepcopy(config)
    novo = apply_weights(
        config,
        {"reliability/subcharacteristics": {"testing_status": 17, "maturity": 83}},
    )
    assert config == antes
    assert [c["weight"] for c in novo["characteristics"]] == [34, 33, 33]
    assert [s["weight"] for s in novo["characteristics"][0]["subcharacteristics"]] == [
        17,
        83,
    ]


def test_apply_weights_com_entidade_que_nao_esta_no_grupo_gera_erro(config):
    with pytest.raises(ValueError):
        apply_weights(config, {"characteristics": {"security": 100}})
