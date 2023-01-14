from src.cli.resources.subcharacteristic import get_subcharacteristic_value

from resources import calculate_characteristics as core_calculate


def calculate_characteristics(config, subchars):
    characteristics = config['characteristics']
    calculate_infos = []

    for char in characteristics:
        calculate_infos.append({
            'key': char['key'],
            'subcharacteristics': get_subcharacteristic_value(subchars, char['subcharacteristics'])
        })

    headers = ["Id", "Name", "Description", "Value", "Created at"]
    return core_calculate({'characteristics': calculate_infos}), headers
