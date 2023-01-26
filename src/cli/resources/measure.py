import logging

from resources import calculate_measures as core_calculate
from staticfiles import SONARQUBE_SUPPORTED_MEASURES

from src.cli.resources.metrics import get_metric_value

logger = logging.getLogger("msgram")


def get_measure_value(measures, subchar):
    measures_calculated = []
    for measure in subchar:
        measure_key = measure["key"]
        measures_calculated.append(
            {
                "key": measure_key,
                "value": {m["key"]: m["value"] for m in measures}[measure_key],
                "weight": measure["weight"],
            }
        )

    return measures_calculated


def calculate_measures(json_data):
    extracted = get_metric_value(json_data)

    calculate_infos = []
    for measures in SONARQUBE_SUPPORTED_MEASURES:
        calculate_infos.append(
            {
                "key": list(measures.keys())[0],
                "parameters": {
                    metric: extracted[metric] for metric in list(measures.values())[0]["metrics"]
                },
            }
        )

    headers = ["Id", "Name", "Description", "Value", "Created at"]
    return core_calculate({"measures": calculate_infos}), headers
