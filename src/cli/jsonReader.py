from src.cli import exceptions
import json
import math

from src.cli.create import (validate_weight_value)

REQUIRED_SONAR_JSON_KEYS = ["paging", "baseComponent", "components"]

REQUIRED_SONAR_BASE_COMPONENT_KEYS = [
    "id",
    "key",
    "name",
    "qualifier",
    "measures",
]


def preconfig_file_reader(absolute_path, available_pre_configs):

    core_format = available_pre_configs
    check_file_extension(absolute_path)

    preconfig_json_file = open_json_file(absolute_path)

    preconfig_file_name = preconfig_json_file["pre_config_name"]

    file_characteristics = read_file_characteristics(preconfig_json_file)
    validate_file_characteristics(preconfig_json_file)

    file_sub_characteristics = read_file_sub_characteristics(preconfig_json_file)
    validate_file_sub_characteristics(preconfig_json_file)

    file_measures = read_file_measures(preconfig_json_file)
    validate_file_measures(preconfig_json_file)

    validate_core_available(core_format,
                            file_characteristics,
                            file_sub_characteristics)

    preconfig = {
        "name": preconfig_file_name,
        "characteristics": file_characteristics,
        "subcharacteristics": file_sub_characteristics,
        "measures": file_measures,
    }

    return preconfig


def read_file_characteristics(preconfig_json_file):

    characteristics = {}
    weights_auxiliar = {}
    char_sub_list = []

    for characteristic in preconfig_json_file["characteristics"]:

        characteristic_auxiliar = {"weight": characteristic["weight"]}
        weights_auxiliar = {}

        for subcharacteristic in characteristic["subcharacteristics"]:
            char_sub_list.append(subcharacteristic["name"])

            weights_auxiliar.update({subcharacteristic["name"]: subcharacteristic["weight"]})

            characteristic_auxiliar.update({"subcharacteristics": char_sub_list, "weights": weights_auxiliar})
        char_sub_list = []

        characteristics.update({characteristic["name"]: characteristic_auxiliar})

    return characteristics


def read_file_sub_characteristics(preconfig_json_file):

    subcharacteristics = {}
    weights_auxiliar = {}
    sub_mea_list = []

    for characteristic in preconfig_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:

            weights_auxiliar = {}
            subcharacteristic_auxiliar = {
                "weights": {characteristic["name"]: subcharacteristic["weight"]},
            }

            for measure in subcharacteristic["measures"]:
                sub_mea_list.append(measure["name"])

                weights_auxiliar.update({measure["name"]: measure["weight"]})
                subcharacteristic_auxiliar.update({"weights": weights_auxiliar, "measures": sub_mea_list})
            sub_mea_list = []

            subcharacteristics.update(
                {subcharacteristic["name"]: subcharacteristic_auxiliar})

    return subcharacteristics


def read_file_measures(preconfig_json_file):

    measures = []

    for characteristic in preconfig_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:
            for measure in subcharacteristic["measures"]:

                measures.append(measure["name"])

    return measures


def validate_file_characteristics(preconfig_json_file):

    sum_of_characteristics_weights = 0
    characteristics_names = []

    for characteristic in preconfig_json_file["characteristics"]:

        if "name" not in characteristic.keys():
            raise exceptions.InvalidCharacteristic(
                "Expected characteristic name field."
            )

        if "weight" not in characteristic.keys():
            raise exceptions.InvalidCharacteristic(
                "{} does not have weight field defined.".format(characteristic["name"])
            )

        if not validate_weight_value(characteristic["weight"]):
            raise exceptions.InvalidCharacteristic(
                "{} does not have weight value inside parameters (0 to 100).".format(characteristic["name"])
            )

        if "weight" in characteristic.keys():
            sum_of_characteristics_weights = sum_of_characteristics_weights + characteristic["weight"]

        if "subcharacteristics" not in characteristic.keys():
            raise exceptions.InvalidCharacteristic(
                "{} does not have subcharacteristics field defined.".format(characteristic["name"])
            )

        if characteristic["subcharacteristics"] is None or len(characteristic["subcharacteristics"]) == 0:
            raise exceptions.InvalidCharacteristic(
                "{} needs to have at least one subcharacteristic defined.".format(characteristic["name"])
            )

        characteristics_names.append(characteristic["name"])

    sum_of_characteristics_weights = round_sum_of_weights(sum_of_characteristics_weights)

    if validate_sum_of_weights(sum_of_characteristics_weights) is False:
        raise exceptions.InvalidCharacteristic(
            "The sum of characteristics weights of is not 100")

    return True


def validate_file_sub_characteristics(preconfig_json_file):

    sub_characteristics_names = []

    for characteristic in preconfig_json_file["characteristics"]:

        sum_of_subcharacteristics_weights = 0

        for subcharacteristic in characteristic["subcharacteristics"]:

            if "name" not in subcharacteristic.keys():
                raise exceptions.InvalidSubcharacteristic(
                    "Expected sub-characteristic name field."
                )

            if "weight" not in subcharacteristic.keys():
                raise exceptions.InvalidSubcharacteristic(
                    "{} does not have weight field defined.".format(subcharacteristic["name"])
                )

            if not validate_weight_value(subcharacteristic["weight"]):
                raise exceptions.InvalidSubcharacteristic(
                    "{} does not have weight value inside parameters (0 to 100).".format(
                        subcharacteristic["name"])
                )

            if "weight" in subcharacteristic.keys():
                sum_of_subcharacteristics_weights = sum_of_subcharacteristics_weights + subcharacteristic["weight"]

            if "measures" not in subcharacteristic.keys():
                raise exceptions.InvalidSubcharacteristic(
                    "{} does not have measures field defined.".format(subcharacteristic["name"])
                )

            if subcharacteristic["measures"] is None or len(subcharacteristic["measures"]) == 0:
                raise exceptions.InvalidSubcharacteristic(
                    "{} needs to have at least one measure defined.".format(subcharacteristic["name"])
                )

            sub_characteristics_names.append(subcharacteristic["name"])

        sum_of_subcharacteristics_weights = round_sum_of_weights(sum_of_subcharacteristics_weights)

        if validate_sum_of_weights(sum_of_subcharacteristics_weights) is False:
            raise exceptions.InvalidSubcharacteristic(
                "The sum of subcharacteristics weights is not 100")

    return True


def validate_file_measures(preconfig_json_file):

    measures_names = []

    for characteristic in preconfig_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:

            sum_of_measures_weights = 0

            for measure in subcharacteristic["measures"]:

                if "name" not in measure.keys():
                    raise exceptions.InvalidMeasure(
                        "Expected measure name field."
                    )

                if "weight" not in measure.keys():
                    raise exceptions.InvalidMeasure(
                        "{} does not have weight field defined.".format(measure["name"])
                    )

                if not validate_weight_value(measure["weight"]):
                    raise exceptions.InvalidMeasure(
                        "{} does not have weight value inside parameters (0 to 100).".format(measure["name"])
                    )

                if "weight" in measure.keys():
                    sum_of_measures_weights = sum_of_measures_weights + measure["weight"]

                measures_names.append(measure["name"])

            sum_of_measures_weights = round_sum_of_weights(sum_of_measures_weights)

            if validate_sum_of_weights(sum_of_measures_weights) is False:
                raise exceptions.InvalidMeasure(
                    "The sum of measures weights is not 100")

    return True


def round_sum_of_weights(sum_weights):

    if 0 < round(100 - sum_weights, 2) <= 0.01:
        sum_weights = 100

    return sum_weights


def validate_sum_of_weights(sum_weights):

    if sum_weights != 100.0:
        return False

    return True


def validate_core_available(available_pre_configs, file_characteristics, file_subcharacteristics):
    core_characteristics = list(available_pre_configs["characteristics"].keys())
    characteristics = list(file_characteristics["characteristics"].keys())

    core_characteristics.sort()
    characteristics.sort()

    if characteristics != core_characteristics:
        raise exceptions.InvalidCharacteristic("The characteristic is not in MeasureSoftGram data base")

    for char in file_characteristics["characteristics"].keys():
        if not all(elem in file_characteristics["characteristics"][char]["subcharacteristics"]
                   for elem in available_pre_configs["characteristics"][char]["subcharacteristics"]):
            raise exceptions.InvalidSubcharacteristic("The sub-characteristic is not in MeasureSoftGram data base")

    for sub in file_subcharacteristics["subcharacteristics"].keys():
        if not all(elem in file_subcharacteristics["subcharacteristics"][sub]["measures"]
                   for elem in available_pre_configs["subcharacteristics"][sub]["measures"]):
            raise exceptions.InvalidMeasure("The measure is not in MeasureSoftgram data base")

    return True


def file_reader(absolute_path):
    check_file_extension(absolute_path)

    json_data = open_json_file(absolute_path)

    check_sonar_format(json_data)

    check_metrics_values(json_data)

    return json_data["components"]


def open_json_file(absolute_path):
    try:
        with open(absolute_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise exceptions.FileNotFound("The file was not found")
    except OSError as error:
        raise exceptions.UnableToOpenFile(f"Failed to open the file. {error}")
    except json.JSONDecodeError as error:
        raise exceptions.InvalidMetricsJsonFile(
            f"Failed to decode the JSON file. {error}"
        )


def get_missing_keys_str(attrs, required_attrs):
    missing_keys = []

    for req_key in required_attrs:
        if req_key not in attrs:
            missing_keys.append(req_key)

    return ", ".join(missing_keys)


def check_sonar_format(json_data):
    attributes = list(json_data.keys())
    missing_keys = get_missing_keys_str(attributes, REQUIRED_SONAR_JSON_KEYS)

    if len(missing_keys) > 0:
        raise exceptions.InvalidMetricsJsonFile(
            f"Invalid Sonar JSON keys. Missing keys are: {missing_keys}"
        )

    base_component = json_data["baseComponent"]
    base_component_attrs = list(base_component.keys())
    missing_keys = get_missing_keys_str(
        base_component_attrs, REQUIRED_SONAR_BASE_COMPONENT_KEYS
    )

    if len(missing_keys) > 0:
        raise exceptions.InvalidMetricsJsonFile(
            f"Invalid Sonar baseComponent keys. Missing keys are: {missing_keys}"
        )

    if len(json_data["components"]) == 0:
        raise exceptions.InvalidMetricsJsonFile(
            "Invalid Sonar JSON components value. It must have at least one component"
        )


def check_file_extension(file_name):
    if file_name.split(".")[-1] != "json":
        raise exceptions.InvalidMetricsJsonFile("Only JSON files are accepted")


def raise_invalid_metric(key, metric):
    raise exceptions.InvalidMetricException(
        'Invalid metric value in "{}" component for the "{}" metric'.format(key, metric)
    )


def check_metrics_values(json_data):
    try:
        for component in json_data["components"]:
            for measure in component["measures"]:
                value = measure["value"]

                try:
                    if value is None or math.isnan(float(value)):
                        raise_invalid_metric(component["key"], measure["metric"])
                except (ValueError, TypeError):
                    raise_invalid_metric(component["key"], measure["metric"])
    except KeyError:
        raise exceptions.InvalidMetricsJsonFile(
            "Failed to validate Sonar JSON metrics. Please check if the file is a valid Sonar JSON"
        )


def validate_metrics_post(response_status, response):
    if 200 <= response_status <= 299:
        print("\nThe imported metrics were saved for the pre-configuration")
    else:
        print("\nThere was an ERROR while saving your Metrics\n")

        if len(response) == 0:
            return

        for key, value in response.items():
            field_name = "General" if key == "__all__" else key

            print(f"\t{field_name} => {value}")
