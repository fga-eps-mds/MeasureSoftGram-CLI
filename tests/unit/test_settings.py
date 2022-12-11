import json
import os
from unittest import mock
import pytest
from src.cli.exceptions import exceptions
from src.config.settings import config_file_json, get_organization, get_product_id, get_repositories
from io import StringIO

VALID_CONFIG = '{"organization":{"name": "fga-eps-mds","id": 1},"product":{"name":"MeasureSoftGram","id":3}' + \
               ',"repositories":[{"2022-1-MeasureSoftGram-CLI":1},{"2022-1-MeasureSoftGram-Core":2},{"2022-' + \
               '1-MeasureSoftGram-Service":3},{"2022-1-MeasureSoftGram-Front":4}]}'
VALID_HOST = "https://measuresoftgram-service.herokuapp.com/"

def setup_succes():
    f = open(".measuresoftgram", "w")
    f.write(VALID_CONFIG)
    f.close()

def teardown():
    try:
        os.remove(".measuresoftgram")
    except Exception:
        pass

def test_config_file_json_succes(mocker):

    setup_succes()

    mocker.patch("builtins.open", mocker.mock_open(read_data=VALID_CONFIG))
    mocker.patch("json.load", return_value=VALID_CONFIG)

    res = VALID_CONFIG.replace('"', '\'').replace(' ', '')

    assert str(config_file_json()).replace(' ', '') in res

    teardown()

def test_config_file_json_fail():

    with pytest.raises(SystemExit) as e:
        config_file_json()

    assert str(e.value) == '0'

