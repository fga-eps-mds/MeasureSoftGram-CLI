import re
from io import StringIO
from src.cli.commands import parse_list


class DummyResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return [
            {
                "_id": "62656d15f354349ee4abfc7b",
                "name": "pre-config-1",
                "created_at": "2022-04-24 15:30:29+00:00",
            },
            {
                "_id": "62656e79f354349ee4abfc7c",
                "name": "pre-config-2",
                "created_at": "2022-04-24 15:36:25+00:00",
            },
            {
                "_id": "62656e7ef354349ee4abfc7d",
                "name": "pre-config-3",
                "created_at": "2022-04-24 15:36:30+00:00",
            },
        ]


def test_pre_configs_list(mocker):
    mocker.patch("requests.get", return_value=DummyResponse(200))

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_list()

        output_lines = fake_out.getvalue().splitlines()

        assert len(output_lines) == 4

        header_regexp = re.compile(r"ID\s+Name\s+Created at\s+Metrics file")

        assert header_regexp.match(output_lines[0]) is not None

        line_regexp = re.compile(
            r"(?P<id>[0-9a-z]+)\s+(?P<name>[^\s]+)\s+"
            + r"(?P<created_at>\d{2,}/\d{2,}/\d{4,}\s\d{2,}:\d{2,}:\d{2,})\s+"
            + r"(?P<metrics_file>[^\s]+)"
        )

        expected_groups = [
            (
                "62656d15f354349ee4abfc7b",
                "pre-config-1",
                "04/24/2022 12:30:29",
                "-",
            ),
            (
                "62656e79f354349ee4abfc7c",
                "pre-config-2",
                "04/24/2022 12:36:25",
                "-",
            ),
            (
                "62656e7ef354349ee4abfc7d",
                "pre-config-3",
                "04/24/2022 12:36:30",
                "-",
            ),
        ]

        for i in range(1, 4):
            match_data = line_regexp.match(output_lines[i])

            assert (
                match_data is not None
            ), f"output_lines[{i}] does not match the expected line regexp"
            assert (
                match_data.groups() == expected_groups[i - 1]
            ), f"{match_data.groups()} != {expected_groups[i - 1]}"


def test_error_in_pre_config_list(mocker):
    mocker.patch("requests.get", return_value=DummyResponse(500))

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_list()

        assert (
            "Error: an error occurred while fetching your pre configurations"
            in fake_out.getvalue()
        )
