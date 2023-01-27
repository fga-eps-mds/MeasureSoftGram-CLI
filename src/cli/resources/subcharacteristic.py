from src.cli.resources.measure import get_measure_value

from resources import calculate_subcharacteristics as core_calculate


def get_subcharacteristic_value(subchars, char):
    subchar_calculated = []
    for subchar in char:
        subchar_key = subchar["key"]

        subchar_calculated.append({
            "key": subchar_key,
            "value": {m['key']: m['value'] for m in subchars}[subchar_key],
            "weight": subchar['weight'],
        })

    return subchar_calculated


def calculate_subcharacteristics(config, measures):
    subchars = [sc['subcharacteristics'] for sc in config['characteristics']]
    calculate_infos = []

    for subchar in subchars:
        calculate_infos.append({
            'key': subchar[0]['key'],
            'measures': get_measure_value(measures, subchar[0]['measures'])
        })

    headers = ["Id", "Name", "Description", "Value", "Created at"]
    return core_calculate({'subcharacteristics': calculate_infos}), headers
