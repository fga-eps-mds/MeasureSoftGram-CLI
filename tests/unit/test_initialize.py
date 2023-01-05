import os
import tempfile

import pytest

from src.cli.commands.cmd_init import command_init


def setup():
    try:
        os.remove(".msgram")
    except OSError:
        pass


def teardown():
    try:
        os.remove(".msgram")
    except OSError:
        pass


def test_create_msgram_dir_and_file_with_success():
    temp_path = tempfile.mkdtemp()
    dir_path = f"{temp_path}/.msgram"

    args = {
        "dir_path": dir_path
    }

    command_init(args)

    assert os.path.isdir(dir_path) is True
    assert os.path.isfile(f"{dir_path}/msgram.json") is True


def test_init_should_return_folder_already_exist_error():
    temp_path = tempfile.mkdtemp()

    args = {
        "dir_path": temp_path
    }

    with pytest.raises(SystemExit) as e:
        command_init(args)

    assert e.value.code == 1


def test_init_should_return_no_args_error():
    args = {}

    with pytest.raises(SystemExit) as e:
        command_init(args)

    assert e.value.code == 1
