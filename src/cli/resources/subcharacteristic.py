from src.cli.resources.measure import get_measure_value

from resources import calculate_subcharacteristics as core_calculate


def calculate_subcharacteristics(config, measures):
    subchars = [sc['subcharacteristics'] for sc in config['characteristics']]
    calculate_infos = []

    # from rich.traceback import install
    # install(show_locals=True)
    for subchar in subchars:
        calculate_infos.append({
            'key': subchar[0]['key'],
            'measures': get_measure_value(measures, subchar[0]['measures'])
        })

    headers = ["Id", "Name", "Description", "Value", "Created at"]
    return core_calculate({'subcharacteristics': calculate_infos}), headers
