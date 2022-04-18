import pytest
from io import StringIO
from tests.test_helpers import read_json
from src.cli import jsonReader, exceptions


@pytest.mark.parametrize("file_name", ["sonar.txt", "sonar.xml", "sonar.jjson"])
def test_invalid_file_extension(file_name):
    """
    Test check_file_extension when an invalid extesion is provided
    """

    with pytest.raises(exceptions.InvalidMetricsJsonFile) as error:
        jsonReader.check_file_extension(file_name)

    assert str(error.value) == "Only JSON files are accepted"


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
    def test_post_success(self, status_code, mocker):
        """
        Test when a success status code is returned
        """

        with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
            jsonReader.validate_metrics_post(status_code, {})

            assert (
                "The imported metrics were saved for the pre-configuration"
                in fake_out.getvalue()
            )

    @pytest.mark.parametrize(
        "status_code, response, additional_msg",
        [
            (400, {}, ""),
            (500, {}, ""),
            (404, {"pre_config_id": "123 is not a valid ID"}, "is not a valid ID"),
            (
                422,
                {
                    "__all__": "The metrics in this file are not the expected in the pre config. Missing metrics: a, b"
                },
                "The metrics in this file are not the expected in the pre config. Missing metrics: ",
            ),
        ],
    )
    def test_post_failure(self, status_code, response, additional_msg, mocker):
        """
        Test when an error is returned
        """

        with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
            jsonReader.validate_metrics_post(status_code, response)

            output = fake_out.getvalue()

            assert "There was an ERROR while saving your Metrics" in output

            if additional_msg:
                assert additional_msg in output


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


def test_valid_read_file_characteristics():
    file_characteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 100.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 100.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 100.0
                            }
                        ]
                    }
                ]
            }
        ]
    }
    characteristics = jsonReader.read_file_characteristics(file_characteristics)

    assert characteristics == {'Reliability': {'expected_value': 22,
                                               'weight': 100.0, 'subcharacteristics': ['Testing_status']}}


def test_valid_validate_file_characteristics():
    file_characteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 100.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 100.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 100.0
                            }
                        ]
                    }
                ]
            }
        ]
    }
    characteristics = jsonReader.validate_file_characteristics(file_characteristics)

    assert characteristics == ["Reliability"]


def test_invalid_validate_file_characteristics():

    file_characteristics_without_weights = {
        "characteristics": [
            {
                "name": "Reliability",
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 100.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 100.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 100.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidCharacteristic):
        jsonReader.validate_file_characteristics(file_characteristics_without_weights)

    file_characteristics_without_name = {
        "characteristics": [
            {
                "weight": 50,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 100.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 100.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 100.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidCharacteristic):
        jsonReader.validate_file_characteristics(file_characteristics_without_name)

    file_characteristics_without_subc = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 50,
                "expected_value": 22,
                "subcharacteristics": []
            }
        ]
    }

    with pytest.raises(exceptions.InvalidCharacteristic):
        jsonReader.validate_file_characteristics(file_characteristics_without_subc)

    file_characteristics_without_expected_value = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 100.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 100.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 100.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidCharacteristic):
        jsonReader.validate_file_characteristics(file_characteristics_without_expected_value)


def test_valid_read_file_sub_characteristics():
    file_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "expected_value": 35,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 40.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }
    subcharacteristics = jsonReader.read_file_sub_characteristics(file_subcharacteristics)

    assert subcharacteristics == {'Testing_status': {'weights': {'Reliability': 100.0},
                                                     'measures': ['passed_tests', 'test_builds', 'test_coverage']}}


def test_valid_validate_file_sub_characteristics():
    file_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 40.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }
    subcharacteristics = jsonReader.validate_file_sub_characteristics(file_subcharacteristics)

    assert subcharacteristics == ["Testing_status"]


def test_invalid_validate_file_sub_characteristics():
    file_without_name_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "weight": 30.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 40.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        jsonReader.validate_file_sub_characteristics(file_without_name_subcharacteristics)

    file_without_weight_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 40.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        jsonReader.validate_file_sub_characteristics(file_without_weight_subcharacteristics)

    file_without_measures_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        jsonReader.validate_file_sub_characteristics(file_without_measures_subcharacteristics)

    file_empty_measures_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": []
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        jsonReader.validate_file_sub_characteristics(file_empty_measures_subcharacteristics)


def test_valid_read_file_measures():
    file_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 40.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 20.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 40.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    measures = jsonReader.read_file_measures(file_measures)

    assert measures == {'passed_tests': {'weights': {'Testing_status': 40.0}}, 'test_builds': {
        'weights': {'Testing_status': 20.0}}, 'test_coverage': {'weights': {'Testing_status': 40.0}}}


def test_valid_validate_file_measures():
    file_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 32,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 40.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    measures = jsonReader.validate_file_measures(file_measures)

    assert measures == ["passed_tests", "test_builds", "test_coverage"]


def test_invalid_validate_file_measures():
    file_without_name_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {
                                "weight": 40.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidMeasure):
        jsonReader.validate_file_measures(file_without_name_measures)

    file_without_weigth_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidMeasure):
        jsonReader.validate_file_measures(file_without_weigth_measures)

    file_invalid_weight_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 120.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidMeasure):
        jsonReader.validate_file_measures(file_invalid_weight_measures)

    file_invalid_weight_sum_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "expected_value": 22,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                                "weight": 10.0
                            },
                            {
                                "name": "test_builds",
                                "weight": 30.0
                            },
                            {
                                "name": "test_coverage",
                                "weight": 30.0
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with pytest.raises(exceptions.InvalidMeasure):
        jsonReader.validate_file_measures(file_invalid_weight_sum_measures)


def test_valid_validate_core_available():

    available_pre_configs = read_json("tests/unit/data/measuresoftgramFormat.json")

    file_characteristics = ["reliability", "maintainability"]
    file_subcharacteristics = ["testing_status", "modifiability"]
    file_measures = ['passed_tests', 'test_builds', 'test_coverage',
                     'non_complex_file_density', 'commented_file_density', 'duplication_absense']

    jsonReader.validate_core_available(available_pre_configs, file_characteristics,
                                       file_subcharacteristics, file_measures)
    assert True


def test_invalid_validate_core_available():

    available_pre_configs = read_json("tests/unit/data/measuresoftgramFormat.json")

    file_characteristics = ["true", "maintainability"]
    file_subcharacteristics = ["testing_status", "modifiability"]
    file_measures = ['passed_tests', 'test_builds', 'test_coverage',
                     'non_complex_file_density', 'commented_file_density', 'duplication_absense']

    with pytest.raises(exceptions.InvalidCharacteristic):
        jsonReader.validate_core_available(available_pre_configs, file_characteristics,
                                           file_subcharacteristics, file_measures)

    file_characteristics = ["reliability", "maintainability"]
    file_subcharacteristics = ["testing_lol", "modifiability"]

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        jsonReader.validate_core_available(available_pre_configs, file_characteristics,
                                           file_subcharacteristics, file_measures)

    file_subcharacteristics = ["testing_status", "modifiability"]
    file_measures = ['passed_tests', 'test_builds', 'wow',
                     'non_complex_file_density', 'commented_file_density', 'duplication_absense']

    with pytest.raises(exceptions.InvalidMeasure):
        jsonReader.validate_core_available(available_pre_configs, file_characteristics,
                                           file_subcharacteristics, file_measures)


def test_round_of_sum_weights():
    sum_weights = 99.99

    sum_weights = jsonReader.round_sum_of_weights(sum_weights)
    assert sum_weights == 100


def test_validate_sum_of_weights():
    sum_weights = 100

    validate = jsonReader.validate_sum_of_weights(sum_weights)
    assert validate is True

    sum_weights = 99.99

    validate = jsonReader.validate_sum_of_weights(sum_weights)
    assert validate is False


def test_validate_expected_value():

    expected_value = 80

    validate = jsonReader.validate_expected_value(expected_value)
    assert validate is True

    expected_value = 120

    validate = jsonReader.validate_expected_value(expected_value)
    assert validate is False


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
