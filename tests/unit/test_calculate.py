import json
from io import StringIO

from tabulate import tabulate

from src.cli.commands.parse_calculate.utils import (
    calculate_measures,
    calculate_characteristics,
    calculate_subcharacteristics,
    calculate_sqc
)
from src.cli.commands.parse_calculate.parse_calculate import parse_calculate

DUMMY_HOST = "http://dummy_host.com/"
EXPECTED_HEADERS = ['Id', 'Name', 'Description', 'Value', 'Created at']
EXPECTED_HEADERS_SQC = ['Id', 'Value', 'Created at']
EXPECTED_DATA_MEASURES = [
    [5, 'Commented File Density', None, 0.04575803981623277, '2022-09-18T13:54:58.598413-03:00']
]
EXPECTED_DATA_CHARACTERISTICS = [
    [2, 'Maintainability', None, 0.6954297796580421, '2022-09-18T14:23:46.526590-03:00']
]
EXPECTED_DATA_SUBCHARACTERISTICS = [
    [1, 'Modifiability', None, 0.6954297796580421, '2022-09-18T14:32:16.524653-03:00']
]
EXPECTED_DATA_SQC = [
    [1093, 0.6388928513249956, '2022-09-18T14:33:50.135692-03:00']
]


class DummyResponse:
    def __init__(self, status_code, res_data):
        self.status_code = status_code
        self.res_data = res_data

    def json(self):
        return self.res_data


def test_calculate_all_tabular_format(mocker):
    mocker.patch(
        "src.cli.commands.parse_calculate.parse_calculate.calculate_measures",
        return_value=(EXPECTED_DATA_MEASURES, EXPECTED_HEADERS)
    )
    mocker.patch(
        "src.cli.commands.parse_calculate.parse_calculate.calculate_characteristics",
        return_value=(EXPECTED_DATA_CHARACTERISTICS, EXPECTED_HEADERS)
    )
    mocker.patch(
        "src.cli.commands.parse_calculate.parse_calculate.calculate_subcharacteristics",
        return_value=(EXPECTED_DATA_SUBCHARACTERISTICS, EXPECTED_HEADERS)
    )
    mocker.patch(
        "src.cli.commands.parse_calculate.parse_calculate.calculate_sqc",
        return_value=(EXPECTED_DATA_SQC, EXPECTED_HEADERS_SQC)
    )
    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_calculate(DUMMY_HOST, 1, 1, 1, "tabular")

        assert "Calculated Measures:" in fake_out.getvalue()
        assert tabulate(EXPECTED_DATA_MEASURES, EXPECTED_HEADERS) in fake_out.getvalue()

        assert "Calculated Characteristics:" in fake_out.getvalue()
        assert tabulate(EXPECTED_DATA_CHARACTERISTICS, EXPECTED_HEADERS) in fake_out.getvalue()

        assert "Calculated Subcharacteristics:" in fake_out.getvalue()
        assert tabulate(EXPECTED_DATA_SUBCHARACTERISTICS, EXPECTED_HEADERS) in fake_out.getvalue()

        assert "Calculated SQC:" in fake_out.getvalue()
        assert tabulate(EXPECTED_DATA_SQC, EXPECTED_HEADERS_SQC) in fake_out.getvalue()


def test_calculate_all_json_format(mocker):
    mocker.patch(
        "src.cli.commands.parse_calculate.parse_calculate.calculate_measures",
        return_value=(EXPECTED_DATA_MEASURES, EXPECTED_HEADERS)
    )
    mocker.patch(
        "src.cli.commands.parse_calculate.parse_calculate.calculate_characteristics",
        return_value=(EXPECTED_DATA_CHARACTERISTICS, EXPECTED_HEADERS)
    )
    mocker.patch(
        "src.cli.commands.parse_calculate.parse_calculate.calculate_subcharacteristics",
        return_value=(EXPECTED_DATA_SUBCHARACTERISTICS, EXPECTED_HEADERS)
    )
    mocker.patch(
        "src.cli.commands.parse_calculate.parse_calculate.calculate_sqc",
        return_value=(EXPECTED_DATA_SQC, EXPECTED_HEADERS_SQC)
    )
    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_calculate(DUMMY_HOST, 1, 1, 1, "json")

        assert json.dumps(EXPECTED_DATA_MEASURES) in fake_out.getvalue()
        assert json.dumps(EXPECTED_DATA_CHARACTERISTICS) in fake_out.getvalue()
        assert json.dumps(EXPECTED_DATA_SUBCHARACTERISTICS) in fake_out.getvalue()
        assert json.dumps(EXPECTED_DATA_SQC) in fake_out.getvalue()


def test_calculate_measures_success(mocker):
    res_data = [
        {
            "id": 5,
            "key": "commented_file_density",
            "name": "Commented File Density",
            "description": None,
            "latest": {
                "id": 9147,
                "measure_id": 5,
                "value": 0.04575803981623277,
                "created_at": "2022-09-18T13:54:58.598413-03:00"
            }
        }
    ]
    mocker.patch(
        "src.clients.service_client.ServiceClient.calculate_entity",
        return_value=DummyResponse(201, res_data)
    )
    extracted_data, headers = calculate_measures(DUMMY_HOST)

    assert EXPECTED_HEADERS == headers
    assert EXPECTED_DATA_MEASURES == extracted_data


def test_calculate_characteristics_success(mocker):
    res_data = [
        {
            "id": 2,
            "key": "maintainability",
            "name": "Maintainability",
            "description": None,
            "latest": {
                "id": 3361,
                "characteristic_id": 2,
                "value": 0.6954297796580421,
                "created_at": "2022-09-18T14:23:46.526590-03:00"
            }
        }
    ]

    mocker.patch(
        "src.clients.service_client.ServiceClient.calculate_entity",
        return_value=DummyResponse(201, res_data)
    )
    extracted_data, headers = calculate_characteristics(DUMMY_HOST)

    assert EXPECTED_HEADERS == headers
    assert EXPECTED_DATA_CHARACTERISTICS == extracted_data


def test_calculate_subcharacteristics_success(mocker):
    res_data = [
        {
            "id": 1,
            "key": "modifiability",
            "name": "Modifiability",
            "description": None,
            "latest": {
                "id": 3351,
                "subcharacteristic_id": 1,
                "value": 0.6954297796580421,
                "created_at": "2022-09-18T14:32:16.524653-03:00"
            }
        }
    ]

    mocker.patch(
        "src.clients.service_client.ServiceClient.calculate_entity",
        return_value=DummyResponse(201, res_data)
    )
    extracted_data, headers = calculate_subcharacteristics(DUMMY_HOST)

    assert EXPECTED_HEADERS == headers
    assert EXPECTED_DATA_SUBCHARACTERISTICS == extracted_data


def test_calculate_sqc_success(mocker):
    res_data = {
        "id": 1093,
        "value": 0.6388928513249956,
        "created_at": "2022-09-18T14:33:50.135692-03:00"
    }

    mocker.patch(
        "src.clients.service_client.ServiceClient.calculate_entity",
        return_value=DummyResponse(201, res_data)
    )
    extracted_data, headers = calculate_sqc(DUMMY_HOST)

    assert EXPECTED_HEADERS_SQC == headers
    assert EXPECTED_DATA_SQC == extracted_data
