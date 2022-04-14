from src.cli import exceptions
import json

from src.cli.create import (validate_weight_sum,
                            validate_weight_value)

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


def preconfig_file_reader(absolute_path):

    check_file_extension(absolute_path)

    j = check_file_existance(absolute_path)
    preconfig_json_file = json.load(j)

    preconfig = preconfig_json_file["preconfig"]
    preconfig_file_characteristics = preconfig["preconfig"]["characteristics"]
    preconfig_file_subcharacteristics = preconfig["preconfig"]["subcharacteristics"]
    preconfig_file_measures = preconfig["preconfig"]["measures"]

    validate_file_characteristics(preconfig_file_characteristics)
    validate_file_subcharacteristics(preconfig_file_subcharacteristics)
    validate_file_measures(preconfig_file_measures)

    validate_weight_sum(preconfig_file_measures.items())

    return preconfig


def validate_file_characteristics(preconfig_file_characteristics):

    for characteristic in preconfig_file_characteristics.items():
        if "subcharacteristics" not in characteristic[1].keys():
            raise exceptions.InvalidCharacteristic(
                "ERROR: {characteristic[0]} (does not have subcharacteristics field in preconfig file)")

        if len(characteristic[1]["subcharacteristics"]) <= 0:
            raise exceptions.InvalidCharacteristic(
                "ERROR: {characteristic[0]} (must have at least one sub-characteristic)")


def validate_file_subcharacteristics(preconfig_file_subcharacteristics):
    for subcharacteristic in preconfig_file_subcharacteristics.items():
        if "measures" not in subcharacteristic[1].keys():
            raise exceptions.InvalidSubcharacteristic(
                "ERROR: {characteristic[0]} (does not have measures field in preconfig file)")

        if len(subcharacteristic[1]["measures"]) <= 0:
            raise exceptions.InvalidSubcharacteristic(
                "ERROR: {characteristic[0]} (must have at least one measure)")


def validate_file_measures(preconfig_file_measures):
    for measure in preconfig_file_measures.items():
        if not validate_weight_value(float(measure[1]["weight"])):
            raise exceptions.InvalidWeightValue(
                f"ERROR: {measure[0]} measure has weight outside valid parameters (must be between 0 and 100).")

    return True


def file_reader(absolute_path):

    check_file_extension(absolute_path)

    f = check_file_existance(absolute_path)
    json_file = json.load(f)
    check_sonar_format(json_file)

    components = json_file["components"]

    return components


def check_file_existance(absolute_path):

    try:
        file = open(absolute_path, "r")
    except FileNotFoundError:
        raise exceptions.FileNotFound("ERRO: arquivo não encontrado")

    return file


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
        raise exceptions.InvalidFileTypeException(
            "ERRO: Apenas arquivos JSON são aceitos"
        )
    return True


def validate_metrics_post(response_status, response):
    if response_status == 201:
        print("\nThe imported metrics were saved for the pre-configuration")
    else:
        print("\nThere was a ERROR while saving your Metrics:\n")

        for key, value in response.items():
            field_name = "General" if key == "__all__" else key

            print(f"\t{field_name} => {value}")
