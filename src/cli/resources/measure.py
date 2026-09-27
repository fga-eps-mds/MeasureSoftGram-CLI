import logging

from resources import calculate_measures as core_calculate
from src.config.settings import SUPPORTED_MEASURES

from src.cli.aggregate_metrics import measures as source_measures
from src.cli.aggregate_metrics import metrics as source_metrics
from src.cli.resources.metrics import get_metric_value
from src.cli.utils import print_warn

logger = logging.getLogger("msgram")


def get_configured_measures(config):
    return [
        measure["key"]
        for characteristic in config["characteristics"]
        for subcharacteristic in characteristic["subcharacteristics"]
        for measure in subcharacteristic["measures"]
    ]


def get_missing_measures(extracted, config, calculated_measures):
    configured_measures = get_configured_measures(config)
    supported_metrics = {
        list(measure.keys())[0]: list(measure.values())[0]["metrics"]
        for measure in SUPPORTED_MEASURES
    }

    missing_measures = {}
    for metrics, measures in [
        (source_metrics["sonar"], source_measures["sonarqube"]),
        (source_metrics["github"], source_measures["github"]),
    ]:
        if not any(metric in extracted for metric in metrics):
            continue

        for measure_key in measures:
            if (
                measure_key in configured_measures
                and measure_key not in calculated_measures
            ):
                missing_measures[measure_key] = [
                    metric
                    for metric in supported_metrics[measure_key]
                    if not extracted.get(metric)
                ]

    return missing_measures


def get_measure_value(measures, subchar):
    measures_calculated = []
    for measure in subchar:
        measure_key = measure["key"]
        found = any(measure_key == m["key"] for m in measures)
        if found:
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
                "metrics": [
                    {
                        "key": metric,
                        "value": (
                            [float(value) for value in extracted[metric]]
                            if extracted.get(metric) and extracted[metric]
                            else None
                        ),
                    }
                    for metric in list(measures.values())[0]["metrics"]
                ],
            }
        )
        new_metrics = []
        for measure in calculate_infos:
            if measure.get("metrics", None) and all(
                metric["value"] for metric in measure["metrics"]
            ):
                new_metrics.append(measure)

        calculate_infos = new_metrics

    calculated_measures = [measure["key"] for measure in calculate_infos]
    missing_measures = get_missing_measures(extracted, config, calculated_measures)
    for measure_key, missing_metrics in missing_measures.items():
        print_warn(
            f"Measure '{measure_key}' could not be calculated. "
            f"Missing metrics: {', '.join(missing_metrics)}"
        )

    headers = ["Id", "Name", "Description", "Value", "Created at"]
    return core_calculate({"measures": calculate_infos}, config), headers
