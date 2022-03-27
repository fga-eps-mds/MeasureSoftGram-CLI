from src.cli import exceptions
import json
from .exceptions import FileNotFound, NullMetricValue
import requests

METRICS_SONAR = [
    "files",
    "functions",
    "complexity",
    "comment_lines_density",
    "duplicated_lines_density",
    "coverage",
    "ncloc",
    "tests",
    "test_errors",
    "test_failures",
    "test_execution_time",
    "security_rating",
]


def file_reader(absolute_path):
    metrics_validation_steps = 0

    check_file_extension(absolute_path)

    f = check_file_existance(absolute_path)
    json_file = json.load(f)
    check_sonar_format(json_file)

    metrics = json_file["baseComponent"]["measures"]

    check_metrics(metrics, metrics_validation_steps)
    check_expected_metrics(metrics, metrics_validation_steps)

    if metrics_validation_steps == 3:
        print("As métricas foram lidas com sucesso")

    print("As métricas foram lidas com sucesso")

    return metrics


def check_file_existance(absolute_path):

    try:
        file = open(absolute_path, "r")
    except FileNotFoundError:
        raise FileNotFound("ERRO: arquivo não encontrado")

    return file


def check_metrics(metrics, metrics_validation_steps):

    for metric in metrics:

        if metric["value"] is not None:
            try:
                float(metric["value"])
                metrics_validation_steps += 1
            except ValueError:
                raise TypeError(
                    """
                    ERRO: A métrica "{}" é invalida.
                    Valor: "{}"
                """.format(
                        metric["metric"], metric["value"]
                    )
                )
        else:
            raise NullMetricValue(
                """
                    ERRO: A métrica "{}" esta Nula
                """.format(
                    metric["metric"]
                )
            )
    metrics_validation_steps += 1


def check_expected_metrics(metrics, metrics_validation_steps):

    if len(metrics) != len(METRICS_SONAR):
        raise exceptions.InvalidMetricException(
            """
            ERRO: Quantidade de métricas recebidas é diferente das métricas esperadas.
            Quantidade de métricas recebidas: {}
            Quantidade de métricas esperadas: {}
        """.format(
                len(metrics), len(METRICS_SONAR)
            )
        )
    else:
        metrics_validation_steps += 1

    sorted_recieved_metrics = sorted(metrics, key=lambda d: d["metric"])
    sorted_expected_metrics = sorted(METRICS_SONAR)

    for recieved, expected in zip(sorted_recieved_metrics, sorted_expected_metrics):
        if recieved["metric"] != expected:
            raise exceptions.InvalidMetricException(
                """
                ERRO: As metricas informadas não coincidem com as métricas esperadas.
                Métrica informada: {}
                Métrica esperada: {}
            """.format(
                    recieved["metric"], expected
                )
            )
        else:
            metrics_validation_steps += 1

    return True


def check_sonar_format(json_file):
    attributes = list(json_file.keys())

    if len(attributes) != 3:
        raise exceptions.InvalidSonarFileAttributeException(
            "ERRO: Quantidade de atributos invalida"
        )
    if (
        attributes[0] != "paging"
        or attributes[1] != "baseComponent"
        or attributes[2] != "components"
    ):
        raise exceptions.InvalidSonarFileAttributeException(
            "ERRO: Atributos incorretos"
        )

    base_component = json_file["baseComponent"]
    base_component_attributs = list(base_component.keys())

    if len(base_component_attributs) != 5:
        raise exceptions.InvalidBaseComponentException(
            "ERRO: Quantidade de atributos de baseComponent invalida"
        )
    if (
        base_component_attributs[0] != "id"
        or base_component_attributs[1] != "key"
        or base_component_attributs[2] != "name"
        or base_component_attributs[3] != "qualifier"
        or base_component_attributs[4] != "measures"
    ):
        raise exceptions.InvalidBaseComponentException(
            "ERRO: Atributos de baseComponent incorretos"
        )

    return True


def check_file_extension(fileName):
    if fileName[-4:] != "json":
        raise exceptions.InvalidFileTypeException("ERRO: Apenas arquivos JSON são aceitos")
    return True


def sucess_read_metrics_message(metrics_validation_steps):
    if metrics_validation_steps == 3:
        print("As métricas foram lidas com sucesso")
    return True
