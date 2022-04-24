
from src.cli import exceptions
from src.cli.jsonReader import (check_file_extension,
                                open_json_file)

BASE_URL = "http://localhost:5000/"


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
    characteristics = list(file_characteristics.keys())

    core_characteristics.sort()
    characteristics.sort()

    if characteristics != core_characteristics:
        raise exceptions.InvalidCharacteristic("The characteristic is not in MeasureSoftGram data base")

    for char in file_characteristics.keys():
        if not all(elem in file_characteristics[char]["subcharacteristics"]
                   for elem in available_pre_configs["characteristics"][char]["subcharacteristics"]):
            raise exceptions.InvalidSubcharacteristic("The sub-characteristic is not in MeasureSoftGram data base")

    for sub in file_subcharacteristics.keys():
        if not all(elem in file_subcharacteristics[sub]["measures"]
                   for elem in available_pre_configs["subcharacteristics"][sub]["measures"]):
            raise exceptions.InvalidMeasure("The measure is not in MeasureSoftgram data base")

    return True


def validate_weight_value(weight):
    return 0 < weight <= 100


def validate_preconfig_post(status_code, response):
    if status_code == 201:
        print(
            f"\nYour Pre Configuration was created with sucess!\nPre Configuration ID: {response['_id']}"
        )
    else:
        print(
            f"\nThere was an ERROR while creating your Pre Configuration:  {response['error']}"
        )
