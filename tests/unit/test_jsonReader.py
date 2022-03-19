from measuresoftgram import jsonReader
import pytest
import json


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

    with pytest.raises(TypeError):
        jsonReader.check_file_extension(file_name)


def test_validSonarFormat():
    """
    Testa se um objeto json fornecido tem a formatação do Sonar
    """

    relativeFilePath = "tests/utils/sonar.json"
    f = open(relativeFilePath, "r")
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

    with pytest.raises(TypeError) as exec_info:
        jsonReader.check_sonar_format(jsonFile) is True

    assert exec_info.value.args[0] == "ERRO: Quantidade de atributos invalida."


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

    with pytest.raises(TypeError) as exec_info:
        jsonReader.check_sonar_format(jsonFile)

    assert exec_info.value.args[0] == "ERRO: Quantidade de atributos invalida."


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

    with pytest.raises(TypeError) as exec_info:
        jsonReader.check_sonar_format(jsonFile)

    assert exec_info.value.args[0] == "ERROR, atributos incorretos"


def test_validMetricValues():

    jsonFile = {
        "paging": {"pageIndex": 1, "pageSize": 100, "total": 5},
        "baseComponent": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [
                {"metric": "duplicated_lines_density", "value": "x", "bestValue": True}
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

    metrics = jsonFile["baseComponent"]["measures"]

    with pytest.raises(TypeError) as exec_info:
        jsonReader.check_metrics(metrics)

    assert (
        exec_info.value.args[0]
        == """
                ERRO: A métrica "duplicated_lines_density" é invalida.
                Valor: "x"
            """
    )


def test_fileReaderList():

    metrics = jsonReader.file_reader(r"tests/utils/sonar.json")
    expectedMetrics = [
        {"metric": "duplicated_lines_density", "value": "0.0", "bestValue": True},
        {"metric": "functions", "value": "2"},
        {"metric": "test_execution_time", "value": "2"},
        {"metric": "test_failures", "value": "0", "bestValue": True},
        {"metric": "test_errors", "value": "0", "bestValue": True},
        {"metric": "security_rating", "value": "1.0", "bestValue": True},
        {"metric": "tests", "value": "2"},
        {"metric": "files", "value": "1"},
        {"metric": "complexity", "value": "2"},
        {"metric": "ncloc", "value": "4"},
        {"metric": "coverage", "value": "100.0", "bestValue": True},
        {"metric": "comment_lines_density", "value": "20.0", "bestValue": False},
    ]

    assert metrics == expectedMetrics


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

    with pytest.raises(TypeError):
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

    with pytest.raises(TypeError):
        jsonReader.check_sonar_format(jsonFile)

    assert "ERRO: Atributo de baseComponet invalido."


def test_ifThereIsLessThanExpectedMetrics():
    """
    Testar se tem menos metricas do que o esperado
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

    with pytest.raises(TypeError):
        jsonReader.check_expected_metrics(jsonFile)

    assert "ERRO: Menos metricas do que o esperado."


def test_ifThereIsMoreThanExpectedMetrics():
    """
    Testar se tem mais metricas do que o esperado
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
                },
                {
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True,
                },
                {"metric": "functions", "value": "2"},
                {"metric": "test_execution_time", "value": "2"},
                {"metric": "test_failures", "value": "0", "bestValue": True},
                {"metric": "test_errors", "value": "0", "bestValue": True},
                {"metric": "security_rating", "value": "1.0", "bestValue": True},
                {"metric": "tests", "value": "2"},
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
        }
    }

    with pytest.raises(TypeError):
        jsonReader.check_expected_metrics(jsonFile)

    assert "ERRO: Mais metricas do que o esperado."


def test_ifThereIsAUnexpectedMetrics():
    """
    Testar se tem mais metricas do que o esperado
    """
    jsonFile = {
        "baseComponent": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [
                {"metric": "duplicated", "value": "0.0", "bestValue": True},
                {"metric": "functions", "value": "2"},
                {"metric": "test_execution_time", "value": "2"},
                {"metric": "test_failures", "value": "0", "bestValue": True},
                {"metric": "test_errors", "value": "0", "bestValue": True},
                {"metric": "security_rating", "value": "1.0", "bestValue": True},
                {"metric": "tests", "value": "2"},
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
    }

    with pytest.raises(TypeError):
        jsonReader.check_expected_metrics(jsonFile)

    assert "ERRO: Metrica diferente do que o esperado."
