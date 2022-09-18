import os
import copy
import json
from io import StringIO

import pytest

from src.cli.commands import parse_init
from tests.test_helpers import read_json
from src.cli.exceptions import exceptions
from src.cli.commands.parse_init.utils import validate_user_file

DUMMY_HOST = "http://dummy_host.com/"
EXPECTED_INIT_DATA = {
    "organization": {
        "name": "fga-eps-mds",
        "id": 1
    },
    "product": {
        "name": "MeasureSoftGram",
        "id": 1
    },
    "repositories": [
        {"2022-1-MeasureSoftGram-CLI": 1},
        {"2022-1-MeasureSoftGram-Core": 1},
        {"2022-1-MeasureSoftGram-Front": 1},
        {"2022-1-MeasureSoftGram-Service": 1}
    ]
}


class DummyResponse:
    def __init__(self, status_code, mocked_data):
        self.status_code = status_code
        self.text = json.dumps(mocked_data)


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


def test_init_create_file(mocker):
    mocker.patch(
        "src.clients.service_client.ServiceClient.make_post_request",
        return_value=DummyResponse(201, {"id": 1})
    )
    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_init("tests/unit/data/init.json", DUMMY_HOST)

        assert EXPECTED_INIT_DATA == read_json(".measuresoftgram")
        assert "'.measuresoftgram' init file created with success" in fake_out.getvalue()
        assert os.path.exists(".measuresoftgram")


def test_init_file_already_exists(mocker):
    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        with open('.measuresoftgram', 'w') as file:
            file.write(json.dumps(EXPECTED_INIT_DATA, indent=4))

        return_code = parse_init("tests/unit/data/init.json", DUMMY_HOST)

        assert return_code == 1
        assert "Error: Init file already exists. Check the file '.measuresoftgram'" in fake_out.getvalue()


def test_user_init_invalid_file():
    user_init_file_data = read_json("tests/unit/data/init.json")

    with pytest.raises(exceptions.InvalidMeasuresoftgramFormat):
        invalid_data = copy.deepcopy(user_init_file_data)
        invalid_data.pop("organization_name")
        validate_user_file(invalid_data)

    with pytest.raises(exceptions.InvalidMeasuresoftgramFormat):
        invalid_data = copy.deepcopy(user_init_file_data)
        invalid_data["organization_name"] = ""
        validate_user_file(invalid_data)

    with pytest.raises(exceptions.InvalidMeasuresoftgramFormat):
        invalid_data = copy.deepcopy(user_init_file_data)
        invalid_data["product_name"] = ""
        validate_user_file(invalid_data)

    with pytest.raises(exceptions.InvalidMeasuresoftgramFormat):
        invalid_data = copy.deepcopy(user_init_file_data)
        invalid_data["repositories"] = "Repositórios"
        validate_user_file(invalid_data)

    with pytest.raises(exceptions.InvalidMeasuresoftgramFormat):
        invalid_data = copy.deepcopy(user_init_file_data)
        invalid_data["repositories"][0] = "invalid_url/com"
        validate_user_file(invalid_data)
