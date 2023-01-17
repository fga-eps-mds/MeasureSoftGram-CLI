from src.cli.resources.characteristic import get_characteristic_value

from resources import calculate_sqc as core_calculate


def calculate_sqc(config, characteristics):
    sqc = config
    calculate_infos = {
        'key': 'sqc',
        'characteristics': get_characteristic_value(characteristics, sqc['characteristics'])
    }

    headers = ["Id", "Value", "Created at"]
    return core_calculate({'sqc': calculate_infos}), headers
