import re

from resources import (
    calculate_measures,
    calculate_subcharacteristics,
    calculate_characteristics,
)


def get_value_by_key(data, key):
    for entity in data:
        if entity["key"] == key:
            return entity["value"]


def make_subcharacteristics_input(calculated_measures):
    return {
        "subcharacteristics": [
            {
                "key": "time_behaviour",
                "measures": [
                    {
                        "key": "response_time",
                        "value": get_value_by_key(calculated_measures, "response_time"),
                        "weight": 100,
                    },
                ],
            },
            {
                "key": "resource_utilization",
                "measures": [
                    {
                        "key": "cpu_utilization",
                        "value": get_value_by_key(
                            calculated_measures, "cpu_utilization"
                        ),
                        "weight": 50,
                    },
                    {
                        "key": "memory_utilization",
                        "value": get_value_by_key(
                            calculated_measures, "memory_utilization"
                        ),
                        "weight": 50,
                    },
                ],
            },
        ]
    }


def make_characteristics_input(calculated_subcharacteristics):
    return {
        "characteristics": [
            {
                "key": "performance_efficiency",
                "subcharacteristics": [
                    {
                        "key": "time_behaviour",
                        "value": float(
                            get_value_by_key(
                                calculated_subcharacteristics, "time_behaviour"
                            )
                        ),
                        "weight": 50,
                    },
                    {
                        "key": "resource_utilization",
                        "value": float(
                            get_value_by_key(
                                calculated_subcharacteristics, "resource_utilization"
                            )
                        ),
                        "weight": 50,
                    },
                ],
            },
        ]
    }


def build_json_output(
    repository_name,
    calculated_characteristics,
    calculated_subcharacteristics,
    calculated_measures,
):
    version = re.search(r"\d{1,2}-\d{1,2}-\d{4}-\d{1,2}-\d{1,2}", repository_name)[0]
    repository = repository_name.split(version)[0][:-1]
    return {
        "repository": [{"key": "repository", "value": repository}],
        "version": [{"key": "version", "value": version}] if version else [],
        "measures": [
            {
                "key": "response_time",
                "value": get_value_by_key(
                    calculated_measures["measures"], "response_time"
                ),
            },
            {
                "key": "cpu_utilization",
                "value": get_value_by_key(
                    calculated_measures["measures"], "cpu_utilization"
                ),
            },
            {
                "key": "memory_utilization",
                "value": get_value_by_key(
                    calculated_measures["measures"],
                    "memory_utilization",
                ),
            },
        ],
        "subcharacteristics": [
            {
                "key": "time_behaviour",
                "value": float(
                    get_value_by_key(
                        calculated_subcharacteristics["subcharacteristics"],
                        "time_behaviour",
                    )
                ),
            },
            {
                "key": "resource_utilization",
                "value": float(
                    get_value_by_key(
                        calculated_subcharacteristics["subcharacteristics"],
                        "resource_utilization",
                    )
                ),
            },
        ],
        "characteristics": [
            {
                "key": "performance_efficiency",
                "value": float(
                    get_value_by_key(
                        calculated_characteristics["characteristics"],
                        "performance_efficiency",
                    )
                ),
            }
        ],
    }


def calculate_perf_eff_measures(repository_name, measures_input):
    calculated_measures = calculate_measures(measures_input)
    subcharacteristics_input = make_subcharacteristics_input(
        calculated_measures["measures"]
    )
    calculated_subcharacteristics = calculate_subcharacteristics(
        subcharacteristics_input
    )
    characteristics_input = make_characteristics_input(
        calculated_subcharacteristics["subcharacteristics"]
    )
    calculated_characteristics = calculate_characteristics(characteristics_input)
    return build_json_output(
        repository_name,
        calculated_characteristics,
        calculated_subcharacteristics,
        calculated_measures,
    )
