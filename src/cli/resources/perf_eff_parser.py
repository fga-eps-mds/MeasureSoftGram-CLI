from pathlib import Path
import pandas as pd
from src.cli.exceptions import exceptions
from src.cli.utils import (
    print_error,
    print_rule,
)


def parse_performance_efficiency_data(path1: Path, path2: Path, repo_name: str):
    try:
        release1_df = pd.read_csv(path1)
        release2_df = pd.read_csv(path2)

        release1_endpoints = []
        release2_endpoints = []

        for column_name, _ in release1_df.items():
            if "ENDPOINT" in str(column_name):
                release1_endpoints.append(column_name)

        for column_name, _ in release2_df.items():
            if "ENDPOINT" in str(column_name):
                release2_endpoints.append(column_name)

        endpoint_calls_1 = release1_df[release1_endpoints].values.tolist()
        endpoint_calls_2 = release2_df[release2_endpoints].values.tolist()

        measures = {
            "measures": [
                {
                    "key": "cpu_utilization",
                    "releases": [
                        {
                            "metrics": release1_df["cpu_app"].values.tolist(),
                            "endpoint_calls": endpoint_calls_1,
                        },
                        {
                            "metrics": release2_df["cpu_app"].values.tolist(),
                            "endpoint_calls": endpoint_calls_2,
                        },
                    ],
                },
                {
                    "key": "memory_utilization",
                    "releases": [
                        {
                            "metrics": release1_df["memory_app"].values.tolist(),
                            "endpoint_calls": endpoint_calls_1,
                        },
                        {
                            "metrics": release2_df["memory_app"].values.tolist(),
                            "endpoint_calls": endpoint_calls_2,
                        },
                    ],
                },
                {
                    "key": "response_time",
                    "releases": [
                        {
                            "metrics": release1_df["response_time"].values.tolist(),
                            "endpoint_calls": endpoint_calls_1,
                        },
                        {
                            "metrics": release2_df["response_time"].values.tolist(),
                            "endpoint_calls": endpoint_calls_2,
                        },
                    ],
                },
            ]
        }
        return measures
    except exceptions.MeasureSoftGramCLIException as e:
        print_error(f"[red]Error parsing csv files: {e}\n")
        print_rule()
        exit(1)
