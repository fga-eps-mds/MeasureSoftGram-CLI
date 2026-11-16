from io import StringIO
from pathlib import Path
import sys
import json
import tempfile
from src.cli.commands.cmd_init import command_init

from src.cli.commands.cmd_list import command_list, print_json_tree
from tests.unit.cli_output import normalize_cli_output

import pytest

INIT_ARGS = {"config_path": ".testmsgram"}


def test_print_json_tree():
    file = open("tests/unit/data/newmsgram.json")
    data = json.load(file)

    captured_output = StringIO()
    sys.stdout = captured_output

    characteristics = data.get("characteristics", [])

    result = print_json_tree(characteristics[0])

    fileExpected = open("tests/unit/data/expected_list.txt")

    compare = fileExpected.read()

    result = normalize_cli_output(result)
    compare = normalize_cli_output(compare)

    assert result == compare


def test_cmd_list():
    temp_path = tempfile.mkdtemp()
    config_path = f'{temp_path}/{INIT_ARGS["config_path"]}'

    captured_output = StringIO()
    sys.stdout = captured_output

    command_init({"config_path": Path(config_path)})

    command_list({"config_path": Path(config_path)})
    sys.stdout = sys.__stdout__

    output = normalize_cli_output(captured_output.getvalue())
    assert (
        "Para editar o arquivo de configuração utilize em seu terminal o seguinte comando:"
        in output
    )


def test_cmd_list_if_path_not_exists():
    captured_output = StringIO()
    sys.stdout = captured_output

    with pytest.raises(SystemExit):
        command_list({"config_path": Path.cwd() / "invalid_path"})

    sys.stdout = sys.__stdout__

    output = normalize_cli_output(captured_output.getvalue())
    assert "O arquivo de configuração não foi encontrado." in output


def test_print_json_tree_technical_debt_ratio():
    file = open("tests/unit/data/newmsgram.json")
    data = json.load(file)

    maintainability = next(
        characteristic
        for characteristic in data.get("characteristics", [])
        if characteristic.get("key") == "maintainability"
    )
    maintainability["subcharacteristics"][0]["measures"].append(
        {
            "key": "technical_debt_ratio",
            "weight": 25,
            "min_threshold": 0,
            "max_threshold": 20,
        }
    )

    result = normalize_cli_output(print_json_tree(maintainability))

    assert (
        "│ │ │ technical_debt_ratio │ │ │ Peso: 25% │ │ │ Métrica(s): "
        "│ │ │ └─sqale_debt_ratio │ │ │ │ Valores de referência: Min = 0 e Max = 20"
        in result
    )
