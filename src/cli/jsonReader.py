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


def preconfig_file_reader(absolute_path, available_pre_configs):

    check_file_extension(absolute_path)

    j = check_file_existance(absolute_path)
    preconfig_json_file = json.load(j)

    preconfig_file_name = preconfig_json_file["pre_config_name"]

    file_characteristics = read_file_characteristics(preconfig_json_file)
    file_sub_characteristics = read_file_sub_characteristics(preconfig_json_file)
    file_measures = read_file_measures(preconfig_json_file)

    preconfig = {
        "name": preconfig_file_name,
        "characteristics": file_characteristics[0],
        "subcharacteristics": file_sub_characteristics[0],
        "measures": file_measures[0],
        "characteristics_weights": [file_characteristics[1]],
        "subcharacteristics_weights": [file_sub_characteristics[1]],
        "measures_weights": [file_measures[1]],
    }

    return preconfig


def read_file_characteristics(preconfig_json_file):
    characteristics_names = []
    characteristics_weights = {}

    for characteristic in preconfig_json_file["characteristics"]:
        if "name" not in characteristic.keys():
            raise exceptions.InvalidCharacteristic(
                "ERROR: Expected characteristic name field."
            )

        if "weight" not in characteristic.keys():
            raise exceptions.InvalidCharacteristic(
                "ERROR: {} does not have weight field defined.".format(characteristic["name"])
            )

        if "subcharacteristics" not in characteristic.keys():
            raise exceptions.InvalidCharacteristic(
                "ERROR: {} does not have subcharacteristics field defined.".format(characteristic["name"])
            )

        if characteristic["subcharacteristics"] is None or len(characteristic["subcharacteristics"]) == 0:
            raise exceptions.InvalidCharacteristic(
                "ERROR: {} needs to have at least one subcharacteristic defined.".format(characteristic["name"])
            )

        characteristics_names.append(characteristic["name"])
        characteristics_weights.update({characteristic["name"]: characteristic["weight"]})

    return [characteristics_names, characteristics_weights]


def read_file_sub_characteristics(preconfig_json_file):

    sub_characteristics_names = []
    sub_characteristics_weights = {}

    for characteristic in preconfig_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:

            if "name" not in subcharacteristic.keys():
                raise exceptions.InvalidSubcharacteristic(
                    "ERROR: Expected sub-characteristic name field."
                )

            if "weight" not in subcharacteristic.keys():
                raise exceptions.InvalidSubcharacteristic(
                    "ERROR: {} does not have weight field defined.".format(subcharacteristic["name"])
                )

            if "measures" not in subcharacteristic.keys():
                raise exceptions.InvalidSubcharacteristic(
                    "ERROR: {} does not have measures field defined.".format(subcharacteristic["name"])
                )

            if subcharacteristic["measures"] is None or len(subcharacteristic["measures"]) == 0:
                raise exceptions.InvalidSubcharacteristic(
                    "ERROR: {} needs to have at least one measure defined.".format(subcharacteristic["name"])
                )

            sub_characteristics_names.append(subcharacteristic["name"])
            sub_characteristics_weights.update({subcharacteristic["name"]: subcharacteristic["weight"]})

    return [sub_characteristics_names, sub_characteristics_weights]


def read_file_measures(preconfig_json_file):

    measures_names = []
    measures_weights = {}

    count_char = 0
    count_sub = 0
    count_meas = 0

    while count_char < len(preconfig_json_file["characteristics"]):
        count_sub = 0
        while count_sub < len(preconfig_json_file["characteristics"][count_char]["subcharacteristics"]):
            count_meas = 0
            while count_meas < len(preconfig_json_file["characteristics"]
                                   [count_char]["subcharacteristics"][count_sub]["measures"]):
                measures_names.append(
                    preconfig_json_file["characteristics"][count_char]["subcharacteristics"]
                    [count_sub]["measures"][count_meas]["name"])
                for item in preconfig_json_file["characteristics"][count_char]["subcharacteristics"][count_sub]["measures"][count_meas].items():
                    measures_weights.update({preconfig_json_file["characteristics"][count_char]["subcharacteristics"][count_sub]
                                             ["measures"][count_meas]["name"]: preconfig_json_file["characteristics"][
                        count_char]["subcharacteristics"][count_sub]
                        ["measures"][count_meas]["weight"]})
                count_meas += 1
            count_sub += 1
        count_char += 1

    return [measures_names, measures_weights]


# def validate_file_measures(preconfig_file_measures):
#     for measure in preconfig_file_measures.items():
#         if not validate_weight_value(float(measure[1]["weight"])):
#             raise exceptions.InvalidWeightValue(
#                 f"ERROR: {measure[0]} measure has weight outside valid parameters (must be between 0 and 100).")

#     return True


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
