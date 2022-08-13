import pytest
from src.cli import jsonReader
from src.cli.exceptions import exceptions
# from io import StringIO


@pytest.mark.parametrize("file_name", ["sonar.txt", "sonar.xml", "sonar.jjson"])
def test_invalid_file_extension(file_name):
    """
    Test check_file_extension when an invalid extesion is provided
    """

    with pytest.raises(exceptions.InvalidMetricsJsonFile) as error:
        jsonReader.check_file_extension(file_name)

    assert str(error.value) == "Only JSON files are accepted."


def test_file_reader_success():
    """
    Test file_reader function success case
    """
    EXPECTED_SONAR_JSON_COMPONENTS = [
        {
            "id": "AX9GDsKlZuVL7NjXSAZ4",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI:tests/__init__.py",
            "name": "__init__.py",
            "qualifier": "UTS",
            "path": "tests/__init__.py",
            "language": "py",
            "measures": [
                {"metric": "security_rating", "value": "1.0", "bestValue": True},
                {"metric": "test_errors", "value": "0", "bestValue": True},
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                },
                {"metric": "test_failures", "value": "0", "bestValue": True},
            ],
        },
        {
            "id": "AX9Fg6R0WRlRH47OejaP",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI:measuresoftgram/cli.py",
            "name": "cli.py",
            "qualifier": "FIL",
            "path": "measuresoftgram/cli.py",
            "language": "py",
            "measures": [
                {"metric": "complexity", "value": "2"},
                {"metric": "functions", "value": "2"},
                {"metric": "ncloc", "value": "4"},
                {"metric": "coverage", "value": "100.0", "bestValue": True},
                {"metric": "security_rating", "value": "1.0", "bestValue": True},
                {
                    "metric": "comment_lines_density",
                    "value": "20.0",
                    "bestValue": False,
                },
                {"metric": "files", "value": "1"},
                {"metric": "test_errors", "value": "0", "bestValue": True},
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                },
                {"metric": "test_failures", "value": "0", "bestValue": True},
            ],
        },
        {
            "id": "AX9GDsKlZuVL7NjXSAZ3",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI:tests/hello_world_test.py",
            "name": "hello_world_test.py",
            "qualifier": "UTS",
            "path": "tests/hello_world_test.py",
            "language": "py",
            "measures": [
                {"metric": "security_rating", "value": "1.0", "bestValue": True},
                {"metric": "test_execution_time", "value": "2"},
                {"metric": "tests", "value": "2"},
                {"metric": "test_errors", "value": "0", "bestValue": True},
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                },
                {"metric": "test_failures", "value": "0", "bestValue": True},
            ],
        },
        {
            "id": "AX9Fg6R0WRlRH47OejaQ",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI:measuresoftgram",
            "name": "measuresoftgram",
            "qualifier": "DIR",
            "path": "measuresoftgram",
            "measures": [
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                },
                {"metric": "functions", "value": "2"},
                {"metric": "security_rating", "value": "1.0", "bestValue": True},
                {"metric": "files", "value": "1"},
                {"metric": "complexity", "value": "2"},
                {"metric": "ncloc", "value": "4"},
                {"metric": "coverage", "value": "100.0", "bestValue": True},
                {
                    "metric": "comment_lines_density",
                    "value": "20.0",
                    "bestValue": False,
                },
            ],
        },
        {
            "id": "AX9GDsKlZuVL7NjXSAZ5",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI:tests",
            "name": "tests",
            "qualifier": "DIR",
            "path": "tests",
            "measures": [
                {"metric": "test_execution_time", "value": "2"},
                {"metric": "test_failures", "value": "0", "bestValue": True},
                {"metric": "test_errors", "value": "0", "bestValue": True},
                {"metric": "security_rating", "value": "1.0", "bestValue": True},
                {"metric": "tests", "value": "2"},
            ],
        },
    ]

    components = jsonReader.file_reader("tests/unit/data/sonar.json")

    assert components == EXPECTED_SONAR_JSON_COMPONENTS


class TestOpenJsonFile:
    """
    Tests open_json_file function
    """

    def test_file_not_found(self):
        """
        Test when the file does not exists
        """

        with pytest.raises(exceptions.FileNotFound) as error:
            jsonReader.open_json_file("tests/utils/sona.json")

        assert str(error.value) == "The file was not found"

    def test_file_invalid_json(self):
        """
        Test when the file is an invalid JSON
        """

        with pytest.raises(exceptions.InvalidMetricsJsonFile) as error:
            jsonReader.open_json_file("tests/unit/data/invalid_json.json")

        assert "Failed to decode the JSON file." in str(error.value)


class TestValidateMetricsPost:
    """
    Tests validate_metrics_post function
    """

    @pytest.mark.parametrize("status_code", [200, 201, 204])
    def test_post_success(self, status_code):
        """
        Test when a success status code is returned
        """

        # with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        message = jsonReader.validate_metrics_post(status_code)

        assert "OK: Data sent successfully" == message

    @pytest.mark.parametrize("status_code", [400, 500, 404, 422])
    def test_post_failure(self, status_code):
        """
        Test when an error is returned
        """

        # with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        message = jsonReader.validate_metrics_post(status_code)

        assert (
            f'FAIL: The host service server returned a {status_code} error. Trying again'
            == message
        )


class TestCheckMetricsValues:
    """
    Tests check_metrics_values function
    """

    INVALID_CHECK_METRICS_VALUES_PARAMS = [
        (
            {
                "components": [
                    {
                        "key": "MeasureSoftGram-CLI:tests/__init__.py",
                        "measures": [
                            {
                                "metric": "security_rating",
                                "value": "1.0",
                            },
                            {
                                "metric": "test_errors",
                                "value": None,
                            },
                        ],
                    }
                ]
            },
            'Invalid metric value in "MeasureSoftGram-CLI:tests/__init__.py" component for the "test_errors" metric',
        ),
        (
            {
                "components": [
                    {
                        "key": "MeasureSoftGram-CLI:tests/__init__.py",
                        "measures": [
                            {
                                "metric": "security_rating",
                                "value": "1.0",
                            },
                            {
                                "metric": "test_failures",
                                "value": "",
                            },
                        ],
                    }
                ]
            },
            'Invalid metric value in "MeasureSoftGram-CLI:tests/__init__.py" component for the "test_failures" metric',
        ),
        (
            {
                "components": [
                    {
                        "key": "MeasureSoftGram-CLI:tests/__init__.py",
                        "measures": [
                            {
                                "metric": "files",
                                "value": "NaN",
                            },
                            {
                                "metric": "test_failures",
                                "value": "0.0",
                            },
                        ],
                    }
                ]
            },
            'Invalid metric value in "MeasureSoftGram-CLI:tests/__init__.py" component for the "files" metric',
        ),
    ]

    @pytest.mark.parametrize(
        "json_data, error_msg", INVALID_CHECK_METRICS_VALUES_PARAMS
    )
    def test_invalid_metric_value(self, json_data, error_msg):
        """
        Test invalid metric values
        """

        with pytest.raises(exceptions.InvalidMetricException) as error:
            jsonReader.check_metrics_values(json_data)

        assert error_msg in str(error.value)

    @pytest.mark.parametrize(
        "json_data",
        [
            {},
            {"components": [{}]},
            {"components": [{"measures": [{"metric": "a"}]}]},
        ],
    )
    def test_key_error(self, json_data):
        """
        Test invalid JSON
        """

        with pytest.raises(exceptions.InvalidMetricsJsonFile) as error:
            jsonReader.check_metrics_values(json_data)

        assert (
            "Failed to validate Sonar JSON metrics. Please check if the file is a valid Sonar JSON"
            in str(error.value)
        )


class TestCheckSonarFormat:
    """
    Tests check_sonar_format function
    """

    INVALID_CHECK_SONAR_FORMAT_PARAMS = [
        (
            {},
            "Invalid Sonar JSON keys. Missing keys are: paging, baseComponent, components",
        ),
        (
            {"baseComponent": {}, "paging": {}},
            "Invalid Sonar JSON keys. Missing keys are: components",
        ),
        (
            {
                "paging": {},
                "baseComponent": {"qualifier": "qualifier"},
                "components": {},
            },
            "Invalid Sonar baseComponent keys. Missing keys are: id, key, name, measures",
        ),
        (
            {
                "paging": {},
                "baseComponent": {
                    "id": "",
                    "key": "",
                    "name": "",
                    "qualifier": "",
                    "measures": "",
                },
                "components": {},
            },
            "Invalid Sonar JSON components value. It must have at least one component",
        ),
    ]

    @pytest.mark.parametrize("json_data, error_msg", INVALID_CHECK_SONAR_FORMAT_PARAMS)
    def test_check_sonar_format_invalid_json(self, json_data, error_msg):
        """
        Test invalid Sonar JSON data
        """

        with pytest.raises(exceptions.InvalidMetricsJsonFile) as error:
            jsonReader.check_sonar_format(json_data)

        assert error_msg in str(error.value)
