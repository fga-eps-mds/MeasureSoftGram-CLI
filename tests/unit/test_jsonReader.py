from src.cli import jsonReader, exceptions
import pytest
import json
from io import StringIO
# from src.cli.jsonReader import validate_file_format
from tests.test_helpers import read_json


def test_fileNotExist():
    """
    Testar se o arquivo existe na pasta
    """
    relativeFilePath = "tests/utils/sona.json"
    with pytest.raises(exceptions.FileNotFound):
        jsonReader.check_file_existance(relativeFilePath)


def test_ValidFileExtension():
    """
    Testa se a extensão do arquivo é válida (ex: .json)
    """

    file_name = "sonar.json"

    assert jsonReader.check_file_extension(file_name) is True


def test_notValidFileExtension():
    """
    Testa se a extensão do arquivo não é válida (ex: .txt, .png, .pdf)
    """

    file_name = "sonar.txt"

    with pytest.raises(exceptions.InvalidFileTypeException):
        jsonReader.check_file_extension(file_name)


def test_validSonarFormat():
    """
    Testa se um objeto json fornecido tem a formatação do Sonar
    """

    filePath = "tests/unit/data/sonar.json"
    f = open(filePath, "r")
    jsonFile = json.load(f)

    assert jsonReader.check_sonar_format(jsonFile) is True


def test_ifThereIsLessThanExpectedSonarAttributes():
    """
    Testa se um objeto json fornecido possui menos atributos
    do que o esperado
    """

    jsonFile = {
        "paging": {"pageIndex": 1, "pageSize": 100, "total": 5},
        "baseComponent": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                }
            ],
        },
    }

    with pytest.raises(exceptions.InvalidSonarFileAttributeException) as exec_info:
        jsonReader.check_sonar_format(jsonFile) is True

    assert exec_info.value.args[0] == "ERRO: Quantidade de atributos invalida"


def test_ifThereIsMoreThanExpectedSonarAttributes():
    """
    Testa se um objeto json fornecido possui mais atributos
    do que o esperado
    """

    jsonFile = {
        "paging": {"pageIndex": 1, "pageSize": 100, "total": 5},
        "baseComponent": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                }
            ],
        },
        "components": [
            {
                "id": "AX9GDsKlZuVL7NjXSAZ4",
                "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI:tests/__init__.py",
                "name": "__init__.py",
                "qualifier": "UTS",
                "path": "tests/__init__.py",
                "language": "py",
                "measures": [
                    {"metric": "security_rating", "value": "1.0", "bestValue": True}
                ],
            }
        ],
        "someOtherAttribute": {"hello": "world", "value": None},
    }

    with pytest.raises(exceptions.InvalidSonarFileAttributeException) as exec_info:
        jsonReader.check_sonar_format(jsonFile)

    assert exec_info.value.args[0] == "ERRO: Quantidade de atributos invalida"


def test_expectedJsonMainAtributes():
    """
    Testa se o json recebido possui um atributo diferente dos 3 esperados:
    paging, baseComponets ou Components
    """

    jsonFile = {
        "paging": {"pageIndex": 1, "pageSize": 100, "total": 5},
        "base": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                }
            ],
        },
        "components": [
            {
                "id": "AX9GDsKlZuVL7NjXSAZ4",
                "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI:tests/__init__.py",
                "name": "__init__.py",
                "qualifier": "UTS",
                "path": "tests/__init__.py",
                "language": "py",
                "measures": [
                    {"metric": "security_rating", "value": "1.0", "bestValue": True}
                ],
            }
        ],
    }

    with pytest.raises(exceptions.InvalidSonarFileAttributeException) as exec_info:
        jsonReader.check_sonar_format(jsonFile)

    assert exec_info.value.args[0] == "ERRO: Atributos incorretos"


def test_validBaseComponentAttributs():
    """
    Testar se todos os atributos do baseComponent são validos
    """
    jsonFile = {
        "baseComponent": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                }
            ],
        }
    }

    with pytest.raises(exceptions.InvalidSonarFileAttributeException):
        jsonReader.check_sonar_format(jsonFile) is True


def test_notValidBaseComponentAttributs():
    """
    Testar se algum dos atributos do baseComponent não é valido
    """
    jsonFile = {
        "baseComponent": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "keys": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                }
            ],
        }
    }

    with pytest.raises(exceptions.InvalidSonarFileAttributeException):
        jsonReader.check_sonar_format(jsonFile)

    assert "ERRO: Atributo de baseComponet invalido."


def test_validate_metrics_post_success(mocker):
    """
    Test for validate_metrics_post_post function
    """

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        jsonReader.validate_metrics_post(response_status=201, response={})

        assert (
            "The imported metrics were saved for the pre-configuration"
            in fake_out.getvalue()
        )


def test_validate_metrics_post_error(mocker):
    """
    Test for validate_metrics_post_post function
    """

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        response = {
            "pre_config_id": "There is no pre configurations with ID 624b45ebac582da342adffc3"
        }

        jsonReader.validate_metrics_post(response_status=404, response=response)

        assert (
            "pre_config_id => There is no pre configurations with ID 624b45ebac582da342adffc3"
            in fake_out.getvalue()
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

    assert characteristics[0] == ["Reliability"]
    assert characteristics[1] == {"Reliability": 100.0}


def test_invalid_read_file_characteristics():

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
        jsonReader.read_file_characteristics(file_characteristics_without_weights)

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
        jsonReader.read_file_characteristics(file_characteristics_without_name)

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
        jsonReader.read_file_characteristics(file_characteristics_without_subc)

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
        jsonReader.read_file_characteristics(file_characteristics_without_expected_value)


def test_valid_read_file_sub_characteristics():
    file_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
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

    assert subcharacteristics[0] == ["Testing_status"]
    assert subcharacteristics[1] == {"Testing_status": 100}


def test_invalid_read_file_sub_characteristics():
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
        jsonReader.read_file_sub_characteristics(file_without_name_subcharacteristics)

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
        jsonReader.read_file_sub_characteristics(file_without_weight_subcharacteristics)

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
        jsonReader.read_file_sub_characteristics(file_without_measures_subcharacteristics)

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
        jsonReader.read_file_sub_characteristics(file_empty_measures_subcharacteristics)


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

    assert measures[0] == ["passed_tests", "test_builds", "test_coverage"]
    assert measures[1] == {"passed_tests": 40, "test_builds": 20, "test_coverage": 40}


def test_invalid_read_file_measures():
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
        jsonReader.read_file_measures(file_without_name_measures)

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
        jsonReader.read_file_measures(file_without_weigth_measures)

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
        jsonReader.read_file_measures(file_invalid_weight_measures)

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
        jsonReader.read_file_measures(file_invalid_weight_sum_measures)


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
