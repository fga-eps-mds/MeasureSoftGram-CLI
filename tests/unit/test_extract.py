import os
import copy
from io import StringIO

import pytest
import tempfile
import shutil

from tests.test_helpers import read_json

from src.cli.commands import command_extract
from src.cli.commands.cmd_extract import get_infos_from_name, command_extract


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
    filename = "metrics/fga-eps-mds-2022-1-MeasureSoftGram-Service-09-11-2022-16-11-42-develop.json"

    name, created_at = get_infos_from_name(filename)
    assert name == "fga-eps-mds-2022-1-MeasureSoftGram-Service-extracted.msgram"
    assert created_at == "2022-09-11T16:11:00"

def test_not_get_file_infos_wrong_name():
    filename = "metrics/wrong-name.json"

    with pytest.raises(SystemExit) as e:
        _ = get_infos_from_name(filename)
    
    assert e.value.code == 1