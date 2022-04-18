from src.cli import exceptions
import json

from src.cli.create import (validate_weight_value)

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

    core_format = available_pre_configs
    check_file_extension(absolute_path)

    j = check_file_existance(absolute_path)
    preconfig_json_file = json.load(j)

    preconfig_file_name = preconfig_json_file["pre_config_name"]

    file_characteristics = read_file_characteristics(preconfig_json_file)
    file_sub_characteristics = read_file_sub_characteristics(preconfig_json_file)
    file_measures = read_file_measures(preconfig_json_file)

    validate_core_available(core_format,
                            file_characteristics[0], file_sub_characteristics[0], file_measures[0])

    preconfig = {
        "name": preconfig_file_name,
        "characteristics": file_characteristics,
        "subcharacteristics": file_sub_characteristics,
        "measures": file_measures,
    }

    return preconfig


def read_file_characteristics(preconfig_json_file):

    characteristics = {}
    char_sub_list = []

    for characteristic in preconfig_json_file["characteristics"]:

        characteristic_auxiliar = {
            "expected_value": characteristic["expected_value"],
            "weight": characteristic["weight"]}

        for subcharacteristic in characteristic["subcharacteristics"]:
            char_sub_list.append(subcharacteristic["name"])

            characteristic_auxiliar.update({"subcharacteristics": char_sub_list})
        char_sub_list = []

        characteristics.update({characteristic["name"]: characteristic_auxiliar})

    return characteristics


def read_file_sub_characteristics(preconfig_json_file):

    subcharacteristics = {}
    sub_mea_list = []
    for characteristic in preconfig_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:

            subcharacteristic_auxiliar = {
                "weights": {characteristic["name"]: subcharacteristic["weight"]},
            }

            for measure in subcharacteristic["measures"]:
                sub_mea_list.append(measure["name"])

                subcharacteristic_auxiliar.update({"measures": sub_mea_list})
            sub_mea_list = []

            subcharacteristics.update(
                {subcharacteristic["name"]: subcharacteristic_auxiliar})

    return subcharacteristics


def read_file_measures(preconfig_json_file):

    measures = {}

    for characteristic in preconfig_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:

            sub_name = subcharacteristic["name"]

            for measure in subcharacteristic["measures"]:

                measure_auxiliar = {"weights": {sub_name: measure["weight"]}}

                measures.update({measure["name"]: measure_auxiliar})

    return measures


def validate_file_characteristics(preconfig_json_file):

    sum_of_characteristics_weights = 0
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

        if not validate_weight_value(characteristic["weight"]):
            raise exceptions.InvalidCharacteristic(
                "ERROR: {} does not have weight value inside parameters (0 to 100).".format(characteristic["name"])
            )

        if "expected_value" not in characteristic.keys():
            raise exceptions.InvalidCharacteristic(
                "The file don't have expected_value field"
            )

        if not validate_expected_value(characteristic["expected_value"]):
            raise exceptions.InvalidCharacteristic("The expected value does not inside parameters (0 to 100) ")

        if "weight" in characteristic.keys():
            sum_of_characteristics_weights = sum_of_characteristics_weights + characteristic["weight"]

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

    sum_of_characteristics_weights = round_sum_of_weights(sum_of_characteristics_weights)

    if validate_sum_of_weights(sum_of_characteristics_weights) is False:
        raise exceptions.InvalidCharacteristic(
            "The sum of characteristics weights of is not 100")

    return [characteristics_names, characteristics_weights]


def validate_file_sub_characteristics(preconfig_json_file):

    sub_characteristics_names = []

    for characteristic in preconfig_json_file["characteristics"]:

        sum_of_subcharacteristics_weights = 0
        sub_characteristics_weights = {}

        for subcharacteristic in characteristic["subcharacteristics"]:

            if "name" not in subcharacteristic.keys():
                raise exceptions.InvalidSubcharacteristic(
                    "ERROR: Expected sub-characteristic name field."
                )

            if "weight" not in subcharacteristic.keys():
                raise exceptions.InvalidSubcharacteristic(
                    "ERROR: {} does not have weight field defined.".format(subcharacteristic["name"])
                )

            if not validate_weight_value(subcharacteristic["weight"]):
                raise exceptions.InvalidSubcharacteristic(
                    "ERROR: {} does not have weight value inside parameters (0 to 100).".format(
                        subcharacteristic["name"])
                )

            if "weight" in subcharacteristic.keys():
                sum_of_subcharacteristics_weights = sum_of_subcharacteristics_weights + subcharacteristic["weight"]

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

        sum_of_subcharacteristics_weights = round_sum_of_weights(sum_of_subcharacteristics_weights)

        if validate_sum_of_weights(sum_of_subcharacteristics_weights) is False:
            raise exceptions.InvalidSubcharacteristic(
                "The sum of subcharacteristics weights is not 100")

    return [sub_characteristics_names, sub_characteristics_weights]


def validate_file_measures(preconfig_json_file):

    measures_names = []
    measures_weights = {}

    for characteristic in preconfig_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:

            sum_of_measures_weights = 0

            for measure in subcharacteristic["measures"]:

                if "name" not in measure.keys():
                    raise exceptions.InvalidMeasure(
                        "ERROR: Expected measure name field."
                    )

                if "weight" not in measure.keys():
                    raise exceptions.InvalidMeasure(
                        "ERROR: {} does not have weight field defined.".format(measure["name"])
                    )

                if not validate_weight_value(measure["weight"]):
                    raise exceptions.InvalidMeasure(
                        "ERROR: {} does not have weight value inside parameters (0 to 100).".format(measure["name"])
                    )

                if "weight" in measure.keys():
                    sum_of_measures_weights = sum_of_measures_weights + measure["weight"]

                measures_names.append(measure["name"])
                measures_weights.update({measure["name"]: measure["weight"]})

            sum_of_measures_weights = round_sum_of_weights(sum_of_measures_weights)

            print(sum_of_measures_weights)

            if validate_sum_of_weights(sum_of_measures_weights) is False:
                raise exceptions.InvalidMeasure(
                    "The sum of measures weights is not 100")

    return [measures_names, measures_weights]


def round_sum_of_weights(sum_weights):

    if 0 < round(100 - sum_weights, 2) <= 0.01:
        sum_weights = 100

    return sum_weights


def validate_sum_of_weights(sum_weights):

    if sum_weights != 100.0:
        return False

    return True


def validate_expected_value(expected_value):
    return 0 < expected_value <= 100


def validate_core_available(available_pre_configs, file_characteristics, file_subcharacteristics, file_measures):

    for i in range(len(file_characteristics)):
        if file_characteristics[i] not in available_pre_configs["characteristics"].keys():
            raise exceptions.InvalidCharacteristic("The characteristic is not in MeasureSoftGram data base")

    for i in range(len(file_subcharacteristics)):
        if file_subcharacteristics[i] not in available_pre_configs["subcharacteristics"].keys():
            raise exceptions.InvalidSubcharacteristic("The subcharacteristic is not in MeasureSoftGram data base")

    for i in range(len(file_measures)):
        if file_measures[i] not in available_pre_configs["measures"].keys():
            raise exceptions.InvalidMeasure("The measure is not in MeasureSoftGram data base")

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
