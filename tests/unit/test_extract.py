import os

import pytest

from src.cli.commands.cmd_extract import get_infos_from_name


def setup():
    try:
        os.remove(".measuresoftgram")
    except OSError:
        pass


def teardown():
    try:
        os.remove(".measuresoftgram")
    except OSError:
        pass


def test_get_file_infos():
    file_path = "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json"

    file_name = get_infos_from_name(file_path)
    assert "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop-extracted.msgram" in file_name

def test_not_get_file_infos_wrong_name():
    filename = "metrics/wrong-name.json"

    with pytest.raises(SystemExit) as e:
        _ = get_infos_from_name(filename)

    assert e.value.code == 1
