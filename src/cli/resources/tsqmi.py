from src.cli.resources.characteristic import get_characteristic_value

from resources import calculate_tsqmi as core_calculate


def calculate_tsqmi(config, characteristics):
    tsqmi = config
    calculate_infos = {
        "key": "tsqmi",
        "characteristics": get_characteristic_value(
            characteristics, tsqmi["characteristics"]
        ),
    }

    headers = ["Id", "Value", "Created at"]
    return core_calculate({"tsqmi": calculate_infos}), headers
