from src.cli.resources.measure import get_measure_value

from resources import calculate_subcharacteristics as core_calculate


def get_subcharacteristic_value(subchars, char):
    subchar_calculated = []
    for subchar in char:
        subchar_key = subchar["key"]

        subchar_calculated.append(
            {
                "key": subchar_key,
                "value": {m["key"]: m["value"] for m in subchars}.get(
                    subchar_key, None
                ),
                "weight": subchar["weight"],
            }
        )

    return subchar_calculated


def calculate_subcharacteristics(config, measures):
    calculate_infos = []

    for characteristic in config["characteristics"]:
        subcharacteristics = characteristic.get("subcharacteristics", [])
        for subchar in subcharacteristics:
            if measures:
                subchar_info = {
                    "key": subchar["key"],
                    "measures": get_measure_value(measures, subchar["measures"]),
                }
                calculate_infos.append(subchar_info)

    headers = ["Id", "Name", "Description", "Value", "Created at"]
    return core_calculate({"subcharacteristics": calculate_infos}), headers
