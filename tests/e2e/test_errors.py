"""Erros por comando: código de saída, mensagem legível e nenhum traceback (a fixture `msgram` já barra traceback).

Os casos marcados com xfail(strict=True) são bugs conhecidos: documentam o comportamento esperado sem quebrar a CI.
Quando o bug for corrigido o teste passa, o strict faz o xfail falhar e obriga a tirar a marca.
"""

import pytest

from tests.e2e.support import PERF_CSV_1, SONAR_DIR, UNIT_DATA, write_default_config


def bug(reason):
    return pytest.mark.xfail(strict=True, reason=f"bug: {reason}")


# (args, código de saída esperado, trecho da mensagem). Caminhos relativos ao tmp_path, que é o cwd do msgram;
# "cfg" tem o msgram.json padrão e "ep" é uma pasta vazia.
CASES = [
    pytest.param(
        ["extract", "-ep", "ep"], 1, "It is necessary to pass sonar_path, github_repository or the pe_ parameters",
        id="extract-sem-fonte",
    ),
    pytest.param(
        ["extract", "-ep", "nao-existe", "-sp", SONAR_DIR], 1, "extract directory", id="extract-ep-inexistente",
    ),
    pytest.param(["extract", "-ep", "ep", "-sp", "ep"], 1, "No JSON files found", id="extract-sp-sem-json"),
    pytest.param(
        ["extract", "-ep", "ep", "-sp", SONAR_DIR, "-gl", "US"], 1,
        "gh_repository must be specified", id="extract-gh-sem-gr",
    ),
    pytest.param(
        ["extract", "-ep", "ep", "-gr", "a/b", "-gd", "errado"], 1,
        "Range of dates for filter must be in format", id="extract-data-invalida",
    ),
    pytest.param(
        ["extract", "-ep", "ep", "-p1", PERF_CSV_1], 1, "Some pe_ parameters",
        id="extract-pe-incompleto",
    ),
    pytest.param(
        ["extract", "-ep", "ep", "-gr", "fga-eps-mds/repo"], 1, None,
        id="extract-gr-sem-rede", marks=bug("msgram-parser 1.2.2 dá UnboundLocalError quando a rede falha"),
    ),
    pytest.param(
        ["calculate", "-ep", "ep", "-cp", "nao-existe"], 1, "Error reading msgram.json", id="calculate-sem-config",
    ),
    pytest.param(["calculate", "-o", "xyz"], 2, "invalid choice: 'xyz'", id="calculate-formato-invalido"),
    pytest.param(
        ["calculate", "-ep", "ep", "-cp", "cfg"], 1, "No metrics files found",
        id="calculate-sem-metrics", marks=bug("a decidir: sem .metrics só avisa e termina com 0"),
    ),
    pytest.param(
        ["list", "-cp", "nao-existe"], 1, "O arquivo de configuração não foi encontrado",
        id="list-sem-config",
    ),
    pytest.param(
        ["diff", "-rp", UNIT_DATA / "missmatch-planned.json", "-rd", UNIT_DATA / "calculated.json"], 1,
        "The size between planned and developed release vectors is not equal", id="diff-tamanhos-diferentes",
    ),
    pytest.param(
        ["diff"], 2, "the following arguments are required: -rd/--rd_path, -rp/--rp_path", id="diff-sem-argumentos",
    ),
    pytest.param(
        ["norm_diff", "-rp", UNIT_DATA / "missmatch-planned.json", "-rd", UNIT_DATA / "calculated.json"], 1,
        "Planned and calculated files have different characteristics", id="norm-diff-chaves-diferentes",
    ),
    pytest.param(
        ["norm_diff"], 2, "the following arguments are required: -rp/--rp_path, -rd/--rd_path",
        id="norm-diff-sem-argumentos",
    ),
]


@pytest.mark.parametrize("args, returncode, message", CASES)
def test_command_error(msgram, tmp_path, args, returncode, message):
    write_default_config(tmp_path / "cfg")
    (tmp_path / "ep").mkdir()

    result = msgram(*args)

    output = result.stdout + result.stderr
    assert result.returncode == returncode, output
    if message:
        assert message in output


@bug("init com msgram.json existente e sem terminal (stdin fechado) dá EOFError no Confirm.ask")
def test_init_existing_config_without_terminal_keeps_file(msgram, tmp_path):
    write_default_config(tmp_path / "cfg")
    before = (tmp_path / "cfg" / "msgram.json").read_text()

    result = msgram("init", "-cp", "cfg", input="")

    assert result.returncode == 0
    assert "not changed" in result.stdout
    assert (tmp_path / "cfg" / "msgram.json").read_text() == before


def test_init_existing_config_answer_no_keeps_file(msgram, tmp_path):
    write_default_config(tmp_path / "cfg")
    (tmp_path / "cfg" / "msgram.json").write_text("{}")

    result = msgram("init", "-cp", "cfg", input="n\n")

    assert result.returncode == 0, result.stdout
    assert "not changed" in result.stdout
    assert (tmp_path / "cfg" / "msgram.json").read_text() == "{}"
