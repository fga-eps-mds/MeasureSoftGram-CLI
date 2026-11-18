"""US13.02 — Definir os pesos do modelo por comparação no terminal (fga-eps-mds/2026.2-MeasureSoftGram-DOC#135).

Cada teste marca os critérios que cobre com @pytest.mark.us("US13.02-CAn"), um por cenário BDD da US.
As respostas vão pela entrada padrão, uma por linha, como se fossem digitadas.
"""

import json

import pytest

from tests.e2e.support import SONAR_DIR

# Respostas do protótipo 1 da US (grupos 1 a 3) e modifiability toda "igualmente".
G1 = ["3", "1", "1", "1", "1"]  # R = M; R e M moderadamente mais que F
G2 = ["2", "2"]  # maturity fortemente mais que testing_status
G3_OK = [
    "1",
    "3",
    "1",
    "1",
    "2",
    "2",
]  # passed > builds (7), passed > coverage (3), coverage > builds (5)
G3_CIRCULAR = [
    "1",
    "3",
    "2",
    "3",
    "1",
    "3",
]  # passed > builds, coverage > passed, builds > coverage (7)
G4_IGUAL = ["3"] * 6

QUESTION = "Qual é mais importante?"


def typed(*answers):
    return "\n".join(answers) + "\n"


@pytest.fixture
def config(msgram, tmp_path):
    cfg = tmp_path / "cfg"
    assert msgram("init", "-cp", cfg).returncode == 0
    return cfg


def read(cfg):
    return json.loads((cfg / "msgram.json").read_text())


def weights(items):
    return [item["weight"] for item in items]


def without_weights(node):
    if isinstance(node, dict):
        return {k: without_weights(v) for k, v in node.items() if k != "weight"}
    if isinstance(node, list):
        return [without_weights(v) for v in node]
    return node


@pytest.mark.us("US13.02-CA1")
def test_ca1_define_os_pesos_por_comparacao(msgram, config):
    antes = read(config)

    result = msgram(
        "weights", "-cp", config, input=typed(*G1, *G2, *G3_OK, *G4_IGUAL, "s")
    )

    assert result.returncode == 0, result.stdout
    data = read(config)
    reliability = data["characteristics"][0]
    assert weights(data["characteristics"]) == [43, 43, 14]
    assert weights(reliability["subcharacteristics"]) == [17, 83]
    assert weights(reliability["subcharacteristics"][0]["measures"]) == [65, 7, 28]
    assert without_weights(data) == without_weights(antes)
    assert sorted(p.name for p in config.iterdir()) == ["msgram.json"]

    out = result.stdout
    assert "8 grupos no modelo · 13 comparações · 4 grupos com uma entidade" in out
    assert "Características (CR 0,00)" in out
    assert "reliability × maintainability: igualmente importantes" in out
    assert "antes → depois" in out
    assert out.count("Gravar os novos pesos") == 1


@pytest.mark.us("US13.02-CA2")
@pytest.mark.parametrize(
    "answers, peso_a, peso_b",
    [
        (["3"], 50, 50),
        (["1", "1"], 75, 25),
        (["1", "2"], 83, 17),
        (["1", "3"], 88, 12),
        (["1", "4"], 90, 10),
    ],
)
def test_ca2_frase_escolhida_e_pesos(msgram, config, answers, peso_a, peso_b):
    result = msgram(
        "weights",
        "-cp",
        config,
        "--group",
        "reliability/subcharacteristics",
        input=typed(*answers, "s"),
    )

    assert result.returncode == 0, result.stdout
    subs = read(config)["characteristics"][0]["subcharacteristics"]
    assert [s["key"] for s in subs] == ["testing_status", "maturity"]
    assert weights(subs) == [peso_a, peso_b]


@pytest.mark.us("US13.02-CA3")
def test_ca3_grupo_com_uma_entidade_nao_pergunta(msgram, config):
    antes = (config / "msgram.json").read_bytes()

    result = msgram(
        "weights", "-cp", config, "--group", "reliability/maturity/measures"
    )

    assert result.returncode == 0, result.stdout
    assert QUESTION not in result.stdout
    assert "uma entidade, peso 100 sem perguntas" in result.stdout
    assert (config / "msgram.json").read_bytes() == antes


@pytest.mark.us("US13.02-CA4")
def test_ca4_contradicao_refazer_o_grupo(msgram, config):
    result = msgram(
        "weights",
        "-cp",
        config,
        input=typed(*G1, *G2, *G3_CIRCULAR, "1", *G3_OK, *G4_IGUAL, "s"),
    )

    assert result.returncode == 0, result.stdout
    out = result.stdout
    assert "CR = 4,95 (acima de 0,10)" in out
    assert "Suas respostas se contradizem." in out
    assert "Conflito mais provável" not in out  # as três comparações empatam
    assert out.count("[1] passed_tests  [2] test_builds") == 2  # o grupo recomeçou
    medidas = read(config)["characteristics"][0]["subcharacteristics"][0]["measures"]
    assert weights(medidas) == [65, 7, 28]


@pytest.mark.us("US13.02-CA4")
def test_ca4_contradicao_aceitar(msgram, config):
    result = msgram(
        "weights",
        "-cp",
        config,
        input=typed(*G1, *G2, *G3_CIRCULAR, "2", *G4_IGUAL, "s"),
    )

    assert result.returncode == 0, result.stdout
    assert "⚠ CR 4,95, acima de 0,10, aceito" in result.stdout
    medidas = read(config)["characteristics"][0]["subcharacteristics"][0]["measures"]
    assert weights(medidas) == [34, 33, 33]


@pytest.mark.us("US13.02-CA5")
def test_ca5_responder_nao_mantem_o_arquivo(msgram, config):
    antes = (config / "msgram.json").read_bytes()

    result = msgram(
        "weights", "-cp", config, input=typed(*G1, *G2, *G3_OK, *G4_IGUAL, "n")
    )

    assert result.returncode == 0, result.stdout
    assert (config / "msgram.json").read_bytes() == antes


@pytest.mark.us("US13.02-CA5")
def test_ca5_interromper_no_meio_mantem_o_arquivo(msgram, config):
    antes = (config / "msgram.json").read_bytes()

    # a entrada acaba no meio do grupo 2, como se o usuário saísse
    result = msgram("weights", "-cp", config, input=typed(*G1, "2"))

    assert result.returncode == 130
    assert "não foi alterado" in result.stdout
    assert (config / "msgram.json").read_bytes() == antes


@pytest.mark.us("US13.02-CA6")
def test_ca6_projeto_sem_configuracao(msgram, tmp_path):
    result = msgram("weights")

    assert result.returncode == 1
    assert (
        "Nenhum arquivo de configuração encontrado em .msgram/msgram.json"
        in result.stdout
    )
    assert "msgram init" in result.stdout
    assert QUESTION not in result.stdout
    assert not (tmp_path / ".msgram").exists()


@pytest.mark.us("US13.02-CA7")
def test_ca7_list_e_calculate_usam_os_novos_pesos(msgram, config, tmp_path):
    extracted = tmp_path / "extracted"
    extracted.mkdir()
    assert msgram("extract", "-sp", SONAR_DIR, "-ep", extracted).returncode == 0

    def tsqmi():
        result = msgram("calculate", "-ep", extracted, "-cp", config, "-o", "json")
        assert result.returncode == 0, result.stdout
        (calculated,) = json.loads((config / "calc_msgram.json").read_text())
        return {
            c["key"]: c["value"] for c in calculated["characteristics"]
        }, calculated["tsqmi"][0]["value"]

    chars_antes, tsqmi_antes = tsqmi()
    assert (
        msgram(
            "weights", "-cp", config, input=typed(*G1, *G2, *G3_OK, *G4_IGUAL, "s")
        ).returncode
        == 0
    )
    chars_depois, tsqmi_depois = tsqmi()

    assert tsqmi_depois != pytest.approx(tsqmi_antes)
    assert chars_depois["reliability"] != pytest.approx(chars_antes["reliability"])

    listing = msgram("list", "-cp", config).stdout
    assert "Peso: 43%" in listing
    assert "Peso: 14%" in listing
    assert "Para definir os pesos por comparação, use: msgram weights" in listing


@pytest.mark.us("US13.02-CA8")
def test_ca8_recalcula_com_as_entidades_do_arquivo(msgram, config):
    data = read(config)
    modifiability = data["characteristics"][1]["subcharacteristics"][0]
    modifiability["measures"] = [
        m for m in modifiability["measures"] if m["key"] != "technical_debt_ratio"
    ]
    (config / "msgram.json").write_text(json.dumps(data, indent=4))

    result = msgram(
        "weights", "-cp", config, input=typed(*G1, *G2, *G3_OK, "3", "3", "3", "s")
    )

    assert result.returncode == 0, result.stdout
    assert "8 grupos no modelo · 10 comparações" in result.stdout
    assert result.stdout.count(QUESTION) == 10
    medidas = read(config)["characteristics"][1]["subcharacteristics"][0]["measures"]
    assert [m["key"] for m in medidas] == [
        "non_complex_file_density",
        "commented_file_density",
        "duplication_absense",
    ]
    assert weights(medidas) == [34, 33, 33]


@pytest.mark.us("US13.02-CA9")
def test_ca9_redefinir_so_um_grupo(msgram, config):
    assert (
        msgram(
            "weights", "-cp", config, input=typed(*G1, *G2, *G3_OK, *G4_IGUAL, "s")
        ).returncode
        == 0
    )
    antes = read(config)

    result = msgram(
        "weights",
        "-cp",
        config,
        "--group",
        "reliability/subcharacteristics",
        input=typed("3", "s"),
    )

    assert result.returncode == 0, result.stdout
    assert "Os demais grupos não foram alterados." in result.stdout
    esperado = json.loads(json.dumps(antes))
    for sub in esperado["characteristics"][0]["subcharacteristics"]:
        sub["weight"] = 50
    assert read(config) == esperado


@pytest.mark.us("US13.02-CA9")
def test_ca9_caminho_invalido_lista_os_validos(msgram, config):
    result = msgram("weights", "-cp", config, "--group", "reliability/xyz")

    assert result.returncode == 1
    assert "Grupo inexistente: reliability/xyz" in result.stdout
    assert "reliability/testing_status/measures" in result.stdout
    assert QUESTION not in result.stdout
