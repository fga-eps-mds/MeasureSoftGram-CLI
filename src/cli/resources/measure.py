import logging

from src.cli.jsonReader import open_json_file

from src.cli.resources.metrics import get_metric_value

from staticfiles import SONARQUBE_SUPPORTED_MEASURES
from resources import calculate_measures as core_calculate

logger = logging.getLogger("msgram")


def calculate_measures(file_path):
    json_data = open_json_file(file_path)
    extracted = get_metric_value(json_data)

    calculate_infos = []
    for measures in SONARQUBE_SUPPORTED_MEASURES:
        calculate_infos.append({
            'key': list(measures.keys())[0],
            'parameters': {
                metric: extracted[metric]
                for metric in list(measures.values())[0]['metrics']
            }
        })

    headers = ["Id", "Name", "Description", "Value", "Created at"]
    return core_calculate({'measures': calculate_infos}), headers
