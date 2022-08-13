from src.cli.exceptions import exceptions
from src.cli.jsonReader import check_file_extension, open_json_file


def pre_config_file_reader(absolute_path, available_pre_configs):

    try:
        core_format = available_pre_configs
        check_file_extension(absolute_path)

        pre_config_json_file = open_json_file(absolute_path)

        pre_config_file_name = pre_config_json_file.get("pre_config_name", None)

        validate_file_characteristics(pre_config_json_file)
        validate_file_sub_characteristics(pre_config_json_file)
        validate_file_measures(pre_config_json_file)

        file_characteristics = read_file_characteristics(pre_config_json_file)
        file_sub_characteristics = read_file_sub_characteristics(pre_config_json_file)
        file_measures = read_file_measures(pre_config_json_file)

        validate_core_available(
            core_format, file_characteristics, file_sub_characteristics
        )

        pre_config = {
            "name": pre_config_file_name,
            "characteristics": file_characteristics,
            "subcharacteristics": file_sub_characteristics,
            "measures": file_measures,
        }

        return pre_config
    except KeyError as error:
        raise exceptions.InvalidMeasuresoftgramFormat(
            f"Invalid JSON format, key {error} does not exist"
        )


def read_file_characteristics(pre_config_json_file):

    characteristics = {}
    weights_auxiliar = {}
    char_sub_list = []

    for characteristic in pre_config_json_file["characteristics"]:

        characteristic_auxiliar = {"weight": characteristic["weight"]}
        weights_auxiliar = {}

        for subcharacteristic in characteristic["subcharacteristics"]:
            char_sub_list.append(subcharacteristic["name"])

            weights_auxiliar.update(
                {subcharacteristic["name"]: subcharacteristic["weight"]}
            )

            characteristic_auxiliar.update(
                {"subcharacteristics": char_sub_list, "weights": weights_auxiliar}
            )
        char_sub_list = []

        characteristics.update({characteristic["name"]: characteristic_auxiliar})

    return characteristics


def read_file_sub_characteristics(pre_config_json_file):

    subcharacteristics = {}
    weights_auxiliar = {}
    sub_mea_list = []

    for characteristic in pre_config_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:

            weights_auxiliar = {}
            subcharacteristic_auxiliar = {
                "weights": {characteristic["name"]: subcharacteristic["weight"]},
            }

            for measure in subcharacteristic["measures"]:
                sub_mea_list.append(measure["name"])

                weights_auxiliar.update({measure["name"]: measure["weight"]})
                subcharacteristic_auxiliar.update(
                    {"weights": weights_auxiliar, "measures": sub_mea_list}
                )
            sub_mea_list = []

            subcharacteristics.update(
                {subcharacteristic["name"]: subcharacteristic_auxiliar}
            )

    return subcharacteristics


def read_file_measures(pre_config_json_file):

    measures = []

    for characteristic in pre_config_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:
            for measure in subcharacteristic["measures"]:

                measures.append(measure["name"])

    return measures


def validate_file_characteristics(pre_config_json_file):

    sum_of_characteristics_weights = 0
    characteristics_names = []

    for characteristic in pre_config_json_file["characteristics"]:

        characteristics = characteristic.keys()

        check_in_keys(
            "name",
            characteristics,
            exceptions.UnableToReadFile,
            "Expected characteristic name field.",
        )

        check_in_keys(
            "weight",
            characteristics,
            exceptions.InvalidWeight,
            "{} characteristic does not have weight field defined.".format(
                characteristic["name"]
            ),
        )

        validate_weight_parameter(
            characteristic["weight"],
            exceptions.InvalidWeight,
            "{} does not have weight value inside parameters (0 to 100).".format(
                characteristic["name"]
            ),
        )

        if "weight" in characteristics:
            sum_of_characteristics_weights = (
                sum_of_characteristics_weights + characteristic["weight"]
            )

        check_in_keys(
            "subcharacteristics",
            characteristics,
            exceptions.UnableToReadFile,
            "{} does not have subcharacteristics field defined.".format(
                characteristic["name"]
            ),
        )

        if (
            characteristic["subcharacteristics"] is None
            or len(characteristic["subcharacteristics"]) == 0
        ):
            raise exceptions.UnableToReadFile(
                "{} needs to have at least one subcharacteristic defined.".format(
                    characteristic["name"]
                )
            )

        characteristics_names.append(characteristic["name"])

    if validate_sum_of_weights(sum_of_characteristics_weights) is False:
        raise exceptions.UnableToReadFile(
            "The sum of characteristics weights of is not 100"
        )

    return True


def validate_file_sub_characteristics(pre_config_json_file):

    sub_characteristics_names = []

    for characteristic in pre_config_json_file["characteristics"]:

        sum_of_subcharacteristics_weights = 0

        for subcharacteristic in characteristic["subcharacteristics"]:

            subcharacteristics = subcharacteristic.keys()

            check_in_keys(
                "name",
                subcharacteristics,
                exceptions.UnableToReadFile,
                "Expected sub-characteristic name field.",
            )

            check_in_keys(
                "weight",
                subcharacteristics,
                exceptions.InvalidWeight,
                '"{}" subcharacteristic does not have weight field defined.'.format(
                    subcharacteristic["name"]
                ),
            )

            validate_weight_parameter(
                subcharacteristic["weight"],
                exceptions.InvalidWeight,
                '"{}" subcharacteristics does not have weight value inside parameters (0 to 100).'.format(
                    subcharacteristic["name"]
                ),
            )

            if "weight" in subcharacteristics:
                sum_of_subcharacteristics_weights = (
                    sum_of_subcharacteristics_weights + subcharacteristic["weight"]
                )

            check_in_keys(
                "measures",
                subcharacteristics,
                exceptions.UnableToReadFile,
                '"{}" subcharacteristic does not have measures field defined.'.format(
                    subcharacteristic["name"]
                ),
            )

            if (
                subcharacteristic["measures"] is None
                or len(subcharacteristic["measures"]) == 0
            ):
                raise exceptions.UnableToReadFile(
                    '"{}" subcharacteristic needs to have at least one measure defined.'.format(
                        subcharacteristic["name"]
                    )
                )

            sub_characteristics_names.append(subcharacteristic["name"])

        sum_of_subcharacteristics_weights = round_sum_of_weights(
            sum_of_subcharacteristics_weights
        )

        if validate_sum_of_weights(sum_of_subcharacteristics_weights) is False:
            raise exceptions.InvalidWeight(
                "The sum of subcharacteristics weights is not 100"
            )

    return True


def validate_file_measures(pre_config_json_file):

    measures_names = []

    for characteristic in pre_config_json_file["characteristics"]:
        for subcharacteristic in characteristic["subcharacteristics"]:

            sum_of_measures_weights = 0

            for measure in subcharacteristic["measures"]:

                measures = measure.keys()

                check_in_keys(
                    "name",
                    measures,
                    exceptions.UnableToReadFile,
                    "Expected measure name field.",
                )

                check_in_keys(
                    "weight",
                    measures,
                    exceptions.InvalidWeight,
                    "{} measure does not have weight field defined.".format(
                        measure["name"]
                    ),
                )

                validate_weight_parameter(
                    measure["weight"],
                    exceptions.InvalidWeight,
                    "{} measure does not have weight value inside parameters (0 to 100).".format(
                        measure["name"]
                    ),
                )

                if "weight" in measures:
                    sum_of_measures_weights = (
                        sum_of_measures_weights + measure["weight"]
                    )

                measures_names.append(measure["name"])

            if validate_sum_of_weights(sum_of_measures_weights) is False:
                raise exceptions.InvalidWeight("The sum of measures weights is not 100")

    return True


def validate_weight_parameter(weight, exception, exception_description):

    if not validate_weight_value(weight):
        raise exception(exception_description)

    return True


def check_in_keys(key_for_check, keys, exception, exception_description):

    if key_for_check not in keys:
        raise exception(exception_description)

    return True


def round_sum_of_weights(sum_weights):

    if 0 < round(100 - sum_weights, 2) <= 0.01:
        sum_weights = 100

    return sum_weights


def validate_sum_of_weights(sum_weights):

    sum_weights = round_sum_of_weights(sum_weights)

    if sum_weights != 100.0:
        return False

    return True


def validate_core_available(
    available_pre_configs, file_characteristics, file_subcharacteristics
):
    core_characteristics = list(available_pre_configs["characteristics"].keys())
    characteristics = list(file_characteristics.keys())

    core_characteristics.sort()
    characteristics.sort()

    for item in [x for x in characteristics if x not in core_characteristics]:
        raise exceptions.UnableToReadFile(
            'The characteristic "{}" is not in MeasureSoftGram database'.format(item)
        )

    for char in file_characteristics.keys():

        for item in [
            x
            for x in file_characteristics[char]["subcharacteristics"]
            if x
            not in available_pre_configs["characteristics"][char]["subcharacteristics"]
        ]:
            raise exceptions.UnableToReadFile(
                'The subcharacteristic "{}" is in a wrong characteristic'.format(item)
                + "or it is not in MeasureSoftgram database"
            )

    for sub in file_subcharacteristics.keys():

        for item in [
            x
            for x in file_subcharacteristics[sub]["measures"]
            if x not in available_pre_configs["subcharacteristics"][sub]["measures"]
        ]:
            raise exceptions.UnableToReadFile(
                'The measure "{}" is in a wrong subcharacteristic or it is not in MeasureSoftgram database'.format(
                    item
                )
            )

    return True


def validate_weight_value(weight):
    return 0 < weight <= 100


def validate_pre_config_post(status_code, response):
    if status_code == 201:
        print(
            f"\nYour Pre Configuration was created with success!\nPre Configuration ID: {response['_id']}"
        )
    else:
        print(
            f"\nThere was an ERROR while creating your Pre Configuration:  {response['error']}"
        )
