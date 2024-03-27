from io import StringIO
from pathlib import Path
import sys
import json
import tempfile
from src.cli.commands.cmd_init import command_init

from src.cli.commands.cmd_list import command_list, print_json_tree

import re

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

    # O padrão de regex para cores no formato [#FFFFFF] e [#458B00]
    color_pattern = r"\[#\w+\]"

    # Substituir todas as ocorrências do padrão pelo texto vazio
    result = re.sub(color_pattern, "", result)
    result = re.sub("\n", "", result)
    compare = re.sub("\n", "", compare)

    assert result == compare


def test_cmd_list():
    temp_path = tempfile.mkdtemp()
    config_path = f'{temp_path}/{INIT_ARGS["config_path"]}'

    captured_output = StringIO()
    sys.stdout = captured_output

    command_init({"config_path": Path(config_path)})

    command_list({"config_path": Path(config_path)})
    sys.stdout = sys.__stdout__

    assert (
        "Para editar o arquivo de configuração utilize em seu terminal o seguinte comando:"
        in captured_output.getvalue()
    )


def test_cmd_list_if_path_not_exists():
    captured_output = StringIO()
    sys.stdout = captured_output

    with pytest.raises(SystemExit):
        command_list({"config_path": Path.cwd() / "invalid_path"})

    sys.stdout = sys.__stdout__

    assert "O arquivo de configuração não foi encontrado." in captured_output.getvalue()
