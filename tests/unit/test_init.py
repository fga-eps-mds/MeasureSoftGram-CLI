import os
import sys
import pytest
import tempfile
import shutil

from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.cli.commands.cmd_init import command_init

INIT_ARGS = {
    'config_path': '.testmsgram'
}


@pytest.mark.parametrize(
    "init_arg",
    ['config_path']
)
def test_init_invalid_args(init_arg):
    captured_output = StringIO()
    sys.stdout = captured_output

    with pytest.raises(SystemExit):
        command_init({})

    sys.stdout = sys.__stdout__
    assert f"KeyError: args['{init_arg}'] - non-existent parameters" in captured_output.getvalue()


def test_init_config_file():
    temp_path = tempfile.mkdtemp()
    config_path = f'{temp_path}/{INIT_ARGS["config_path"]}'

    captured_output = StringIO()
    sys.stdout = captured_output

    command_init({'config_path': Path(config_path)})
    sys.stdout = sys.__stdout__

    assert len(os.listdir(config_path)) == 1
    assert os.listdir(config_path)[0] == 'msgram.json'

    assert "The file config: '.testmsgram/msgram.json' was created successfully." in captured_output.getvalue()

    shutil.rmtree(temp_path)


def test_init_replace_file():
    config_path = tempfile.mkdtemp()

    captured_output = StringIO()
    sys.stdout = captured_output

    shutil.copy(
        "tests/unit/data/msgram.json",
        f"{config_path}/msgram.json"
    )

    with patch('builtins.input', return_value='n'):
        command_init({'config_path': Path(config_path)})
        sys.stdout = sys.__stdout__

    assert len(os.listdir(config_path)) == 1
    assert os.listdir(config_path)[0] == 'msgram.json'

    assert f"The file config: '{config_path.split('/')[-1]}/msgram.json' not changed..." in captured_output.getvalue()

    shutil.rmtree(config_path)
