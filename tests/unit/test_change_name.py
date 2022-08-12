import pytest
from io import StringIO
from src.cli.commands import parse_change_name


class DummyResponse:
    def __init__(self, status_code, res_data):
        self.status_code = status_code
        self.res_data = res_data

    def json(self):
        return self.res_data


def test_change_name_sucess(mocker):
    res_data = {
        "_id": "6261b76c974ddbc76bdea7af",
        "name": "pre-config-one",
        "characteristics": {},
        "subcharacteristics": {},
        "measures": [],
        "created_at": "2022-04-21 19:58:36+00:00",
    }

    mocker.patch("requests.patch", return_value=DummyResponse(200, res_data))

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_change_name("6261b76c974ddbc76bdea7af", "pre-config-1")

        expected = (
            'Your Pre Configuration name was succesfully changed to "pre-config-one"'
        )

        assert expected in fake_out.getvalue()


@pytest.mark.parametrize(
    "status_code, error_msg",
    [
        (
            404,
            "There was an ERROR while changing your Pre Configuration name: "
            + "There is no pre configurations with ID 6261b76c974ddbc76bdea7af",
        ),
        (
            422,
            "There was an ERROR while changing your Pre Configuration name: "
            + "The pre config name is already in use",
        ),
    ],
)
def test_change_name_error(mocker, status_code, error_msg):
    res_data = {"error": error_msg}

    mocker.patch("requests.patch", return_value=DummyResponse(status_code, res_data))

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_change_name("6261b76c974ddbc76bdea7af", "pre-config-1")

        assert error_msg in fake_out.getvalue()
