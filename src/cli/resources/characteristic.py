from src.cli.resources.subcharacteristic import get_subcharacteristic_value

from resources import calculate_characteristics as core_calculate


def get_characteristic_value(chars, tsqmi):
    char_calculated = []
    for char in tsqmi:
        char_key = char["key"]

        found = any(char_key == m["key"] for m in chars)
        if found:
            char_calculated.append(
                {
                    "key": char_key,
                    "value": {m["key"]: m["value"] for m in chars}[char_key],
                    "weight": char["weight"],
                }
            )

    return char_calculated


def calculate_characteristics(config, subchars):
    characteristics = config["characteristics"]
    calculate_infos = []

    for char in characteristics:
        char_info = {
            "key": char["key"],
            "subcharacteristics": get_subcharacteristic_value(
                subchars, char["subcharacteristics"]
            ),
        }
        if len(char_info["subcharacteristics"]) > 0:
            calculate_infos.append(char_info)

    headers = ["Id", "Name", "Description", "Value", "Created at"]

    return core_calculate({"characteristics": calculate_infos}), headers
