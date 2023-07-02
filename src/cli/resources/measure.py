import logging

from resources import calculate_measures as core_calculate
from src.config.settings import SUPPORTED_MEASURES

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


def calculate_measures(
    json_data,
    config: dict = {
        "characteristics": [{"subcharacteristics": [{"measures": [{"key": ""}]}]}]
    },
):
    extracted = get_metric_value(json_data)

    calculate_infos = []
    for measures in SUPPORTED_MEASURES:
        calculate_infos.append(
            {
                "key": list(measures.keys())[0],
                "parameters": {
                    metric: extracted[metric] if extracted.get(metric) else None
                    for metric in list(measures.values())[0]["metrics"]
                },
            }
        )
        new_metrics = []
        for measure in calculate_infos:
            if measure.get("parameters", None) and all(measure["parameters"].values()):
                new_metrics.append(measure)

        calculate_infos = new_metrics

    headers = ["Id", "Name", "Description", "Value", "Created at"]
    return core_calculate({"measures": calculate_infos}, config), headers
