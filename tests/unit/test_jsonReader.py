import pytest
import tempfile
import shutil

from pathlib import Path

from src.cli import jsonReader
from src.cli.exceptions import exceptions
from tests.unit.data.file_reader_response import EXPECTED_SONAR_JSON_COMPONENTS


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
    components = jsonReader.file_reader(Path("tests/unit/data/sonar.json"))
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
            jsonReader.open_json_file(Path("tests/utils/sona.json"))

        assert str(error.value) == "The file was not found"

    def test_file_invalid_json(self):
        """
        Test when the file is an invalid JSON
        """
        with pytest.raises(exceptions.InvalidMetricsJsonFile) as error:
            jsonReader.open_json_file(Path("tests/unit/data/invalid_json.json"))

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

        assert "OK: Metrics uploaded successfully" == message

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
            "Invalid Sonar baseComponent TRK measures. Missing keys are: test_failures, test_errors, files, ncloc",
        ),
        (
            {
                "paging": {},
                "baseComponent": {
                    "id": "",
                    "key": "",
                    "name": "",
                    "qualifier": "",
                    "measures": [
                        {"metric": "test_failures"},
                        {"metric": "test_errors"},
                        {"metric": "files"},
                        {"metric": "ncloc"}
                    ],
                },
                "components": {},
            },
            "File with valid schema but no metrics data.",
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


def test_read_multiple_files():
    dirpath = tempfile.mkdtemp()
    shutil.copy(
        "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json",
        f"{dirpath}/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json"
    )

    file_names = [file_name for _, file_name in jsonReader.read_mult_files(Path(dirpath), 'json')]
    assert len(file_names) == 1
    assert file_names[0] == "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json"

    shutil.rmtree(dirpath)


def test_validate_empty_folder_pattern():
    dirpath = tempfile.mkdtemp()
    shutil.copy(
        "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json",
        f"{dirpath}/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json"
    )

    with pytest.raises(exceptions.MeasureSoftGramCLIException) as error:
        list(jsonReader.folder_reader(Path(dirpath), 'empty'))

    assert str(error.value) == "No files .empty found inside folder."

    shutil.rmtree(dirpath)
