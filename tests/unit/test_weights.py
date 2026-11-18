import copy
import json

import pytest
from staticfiles import DEFAULT_PRE_CONFIG

from src.cli.commands import cmd_weights
from src.cli.commands.cmd_weights import command_weights
from src.cli.parsers import create_parser

# Respostas do protótipo 1 (grupos 1 a 3) + modifiability toda "igualmente".
G1 = ["3", "1", "1", "1", "1"]
G2 = ["2", "2"]
G3_CIRCULAR = ["1", "3", "2", "3", "1", "3"]
G3_OK = ["1", "3", "1", "1", "2", "2"]
G4_IGUAL = ["3"] * 6


@pytest.fixture(autouse=True)
def wide_console(monkeypatch):
    # sem terminal o rich usa 80 colunas e quebra as linhas longas; os testes comparam texto
    monkeypatch.setattr(cmd_weights.console, "_width", 200)


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config_dir = tmp_path / ".msgram"
    config_dir.mkdir()
    (config_dir / "msgram.json").write_text(json.dumps(DEFAULT_PRE_CONFIG, indent=4))
    return config_dir


def answer(monkeypatch, answers):
    """Substitui as perguntas do terminal por uma lista de respostas; devolve os prompts feitos."""
    it = iter(answers)
    prompts = []

    def fake(prompt, choices, default=None):
        prompts.append(prompt)
        value = next(it)
        if isinstance(value, BaseException):
            raise value
        assert value in choices, f"{value!r} não é opção de {prompt!r}"
        return value

    monkeypatch.setattr(cmd_weights, "ask_choice", fake)
    return prompts


def read(config_dir):
    return json.loads((config_dir / "msgram.json").read_text())


def weights_of(items):
    return [i["weight"] for i in items]


# ---------------------------------------------------------------- Cenário 1


def test_cenario_1_define_e_grava_os_pesos(project, monkeypatch, capsys):
    answer(monkeypatch, G1 + G2 + G3_CIRCULAR + ["1"] + G3_OK + G4_IGUAL + ["s"])

    command_weights({"config_path": project, "group": None})

    config = read(project)
    reliability = config["characteristics"][0]
    assert weights_of(config["characteristics"]) == [43, 43, 14]
    assert weights_of(reliability["subcharacteristics"]) == [17, 83]
    assert weights_of(reliability["subcharacteristics"][0]["measures"]) == [65, 7, 28]

    out = capsys.readouterr().out
    assert "8 grupos no modelo · 13 comparações · 4 grupos com uma entidade" in out
    assert "CR = 4,95 (acima de 0,10)" in out
    assert "Características (CR 0,00)" in out
    assert (
        "reliability × functional_suitability: reliability é moderadamente mais importante"
        in out
    )
    assert "reliability › testing_status › medidas (CR 0,06)" in out
    assert "✔ Pesos gravados em .msgram/msgram.json." in out


def test_so_o_campo_weight_muda_e_nenhum_arquivo_novo(project, monkeypatch):
    answer(monkeypatch, G1 + G2 + G3_OK + G4_IGUAL + ["s"])

    command_weights({"config_path": project, "group": None})

    def sem_pesos(node):
        if isinstance(node, dict):
            return {k: sem_pesos(v) for k, v in node.items() if k != "weight"}
        if isinstance(node, list):
            return [sem_pesos(v) for v in node]
        return node

    assert sem_pesos(read(project)) == sem_pesos(DEFAULT_PRE_CONFIG)
    assert sorted(p.name for p in project.iterdir()) == ["msgram.json"]


# ---------------------------------------------------------------- Cenário 4


def test_cenario_4_aceitar_grupo_inconsistente(project, monkeypatch, capsys):
    answer(monkeypatch, G1 + G2 + G3_CIRCULAR + ["2"] + G4_IGUAL + ["s"])

    command_weights({"config_path": project, "group": None})

    medidas = read(project)["characteristics"][0]["subcharacteristics"][0]["measures"]
    assert weights_of(medidas) == [34, 33, 33]
    assert "⚠ CR 4,95, acima de 0,10, aceito" in capsys.readouterr().out


def test_refazer_repete_as_perguntas_do_grupo(project, monkeypatch):
    prompts = answer(
        monkeypatch, G1 + G2 + G3_CIRCULAR + ["1"] + G3_OK + G4_IGUAL + ["s"]
    )

    command_weights({"config_path": project, "group": None})

    perguntas_g3 = [p for p in prompts if "[1] passed_tests  [2] test_builds" in p]
    assert len(perguntas_g3) == 2


# ---------------------------------------------------------------- Cenário 5


def test_cenario_5_responder_nao_mantem_o_arquivo(project, monkeypatch):
    antes = (project / "msgram.json").read_bytes()
    answer(monkeypatch, G1 + G2 + G3_OK + G4_IGUAL + ["n"])

    command_weights({"config_path": project, "group": None})

    assert (project / "msgram.json").read_bytes() == antes


def test_cenario_5_ctrl_c_no_meio_mantem_o_arquivo(project, monkeypatch, capsys):
    antes = (project / "msgram.json").read_bytes()
    answer(monkeypatch, G1 + ["2", KeyboardInterrupt()])

    with pytest.raises(SystemExit) as saida:
        command_weights({"config_path": project, "group": None})

    assert saida.value.code == 130
    assert (project / "msgram.json").read_bytes() == antes
    assert "não foi alterado" in capsys.readouterr().out


# ---------------------------------------------------------------- Cenário 6


def test_cenario_6_sem_configuracao(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    prompts = answer(monkeypatch, [])

    with pytest.raises(SystemExit) as saida:
        command_weights({"config_path": tmp_path / ".msgram", "group": None})

    assert saida.value.code == 1
    assert prompts == []
    out = capsys.readouterr().out
    assert "Nenhum arquivo de configuração encontrado em .msgram/msgram.json" in out
    assert "msgram init" in out


# ---------------------------------------------------------------- Cenário 8


def test_cenario_8_perguntas_refletem_o_arquivo_atual(project, monkeypatch):
    config = copy.deepcopy(DEFAULT_PRE_CONFIG)
    modifiability = config["characteristics"][1]["subcharacteristics"][0]
    modifiability["measures"] = [
        m for m in modifiability["measures"] if m["key"] != "technical_debt_ratio"
    ]
    (project / "msgram.json").write_text(json.dumps(config, indent=4))
    prompts = answer(monkeypatch, G1 + G2 + G3_OK + ["3"] * 3 + ["s"])

    command_weights({"config_path": project, "group": None})

    medidas = read(project)["characteristics"][1]["subcharacteristics"][0]["measures"]
    assert [m["key"] for m in medidas] == [
        "non_complex_file_density",
        "commented_file_density",
        "duplication_absense",
    ]
    assert weights_of(medidas) == [34, 33, 33]
    assert sum("Qual é mais importante" in p for p in prompts) == 3 + 1 + 3 + 3


# ---------------------------------------------------------------- Cenário 9 (--group)


def test_cenario_9_redefinir_so_um_grupo(project, monkeypatch, capsys):
    answer(monkeypatch, ["3", "s"])

    command_weights({"config_path": project, "group": "reliability/subcharacteristics"})

    config = read(project)
    esperado = copy.deepcopy(DEFAULT_PRE_CONFIG)
    esperado["characteristics"][0]["subcharacteristics"][0]["weight"] = 50
    esperado["characteristics"][0]["subcharacteristics"][1]["weight"] = 50
    assert config == esperado
    assert "Os demais grupos não foram alterados." in capsys.readouterr().out


def test_group_invalido_lista_os_caminhos_validos(project, monkeypatch, capsys):
    prompts = answer(monkeypatch, [])

    with pytest.raises(SystemExit) as saida:
        command_weights({"config_path": project, "group": "reliability/xyz"})

    assert saida.value.code == 1
    assert prompts == []
    out = capsys.readouterr().out
    assert "Grupo inexistente: reliability/xyz" in out
    assert "reliability/testing_status/measures" in out


# ---------------------------------------------------------------- Cenário 3


def test_cenario_3_grupo_de_uma_entidade_sem_perguntas(project, monkeypatch, capsys):
    prompts = answer(monkeypatch, [])

    command_weights({"config_path": project, "group": "reliability/maturity/measures"})

    assert prompts == []
    assert "Nenhum peso a alterar." in capsys.readouterr().out


# ---------------------------------------------------------------- parser


def test_subcomando_weights_no_parser():
    args = create_parser().parse_args(["weights", "--group", "characteristics"])
    assert args.func is command_weights
    assert args.group == "characteristics"


# ---------------------------------------------------------------- diagnóstico do conflito

# modifiability: non_complex (A), commented (B), duplication (C), technical_debt (D)
# A > B, A > C, D > A (contradiz), B > C, B > D, C > D
G4_COM_CONFLITO = ["1", "1", "1", "2", "2", "1", "1", "1", "1", "2", "1", "1"]


def test_aviso_aponta_a_comparacao_em_conflito(project, monkeypatch, capsys):
    answer(monkeypatch, G1 + G2 + G3_OK + G4_COM_CONFLITO + ["2", "n"])

    command_weights({"config_path": project, "group": None})

    out = capsys.readouterr().out
    assert (
        "Conflito mais provável: non_complex_file_density × technical_debt_ratio. "
        "Sugestão: igualmente importantes"
    ) in out


def test_aviso_nao_aponta_conflito_no_caso_circular(project, monkeypatch, capsys):
    answer(monkeypatch, G1 + G2 + G3_CIRCULAR + ["2"] + G4_IGUAL + ["n"])

    command_weights({"config_path": project, "group": None})

    out = capsys.readouterr().out
    assert "CR = 4,95 (acima de 0,10)" in out
    assert "Conflito mais provável" not in out
