from io import StringIO
from src.cli.commands import parse_show


class DummyResponse:
    def __init__(self, status_code, mocked_data):
        self.status_code = status_code
        self.res = mocked_data

    def json(self):
        return self.res


def test_pre_configs_show(mocker):
    mocked_pre_config = {
        "_id": "62656d15f354349ee4abfc7b",
        "name": "TESTa essa joça",
        "characteristics": {
            "reliability": {
                "expected_value": 70,
                "weight": 50,
                "subcharacteristics": ["testing_status"],
                "weights": {"testing_status": 100.0},
            },
            "maintainability": {
                "expected_value": 30,
                "weight": 50,
                "subcharacteristics": ["modifiability"],
                "weights": {"modifiability": 100.0},
            },
        },
        "subcharacteristics": {
            "testing_status": {
                "weights": {"passed_tests": 100.0},
                "measures": ["passed_tests"],
            },
            "modifiability": {
                "weights": {"non_complex_file_density": 100.0},
                "measures": ["non_complex_file_density"],
            },
        },
        "measures": ["passed_tests", "non_complex_file_density"],
        "created_at": "2022-04-24 15:30:29+00:00",
    }

    mocker.patch("requests.get", return_value=DummyResponse(200, mocked_pre_config))

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_show("abcd")

        expected_lines = [
            "Name: TESTa essa joça",
            "ID: 62656d15f354349ee4abfc7b",
            "Created at: 04/24/2022 12:30:29",
            "reliability (weigth: 50)",
            "testing_status (weigth: 100.0)",
            "passed_tests (weigth: 100.0)",
            "maintainability (weigth: 50)",
            "modifiability (weigth: 100.0)",
            "non_complex_file_density (weigth: 100.0)",
        ]

        for line in expected_lines:
            assert line in fake_out.getvalue()


def test_error_in_pre_config_list(mocker):
    error_res = {"error": "Generic Not Found Error"}

    mocker.patch("requests.get", return_value=DummyResponse(404, error_res))

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_show("abcd")

        assert error_res["error"] in fake_out.getvalue()
