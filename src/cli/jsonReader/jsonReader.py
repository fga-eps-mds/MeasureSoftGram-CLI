import json
import math
from pathlib import Path

import rich.progress
from rich import print

from src.cli.exceptions import exceptions

REQUIRED_SONAR_JSON_KEYS = ["paging", "baseComponent", "components"]
REQUIRED_TRK_MEASURES = ["test_failures", "test_errors", "files", "ncloc"]
REQUIRED_SONAR_BASE_COMPONENT_KEYS = [
    "id",
    "key",
    "name",
    "qualifier",
    "measures",
]


def file_reader(path_file):
    json_data = open_json_file(path_file, True)

    check_sonar_format(json_data)
    check_metrics_values(json_data)

    components = json_data["components"]
    components.append(json_data["baseComponent"])
    return components


def read_mult_files(directory: Path, pattern: str):
    for path_file in directory.glob(f"*.{pattern}"):
        try:
            yield open_json_file(path_file), path_file.name
        except exceptions.MeasureSoftGramCLIException:
            print(f"[red]Error calculating {path_file.name}: Failed to decode the JSON file.\n")


def folder_reader(dir_path, pattern):
    num_files_error = 0
    if not list(dir_path.glob(f"*.{pattern}")):
        raise exceptions.MeasureSoftGramCLIException(f"No files .{pattern} found inside folder.")

    for path_file in dir_path.glob(f"*.{pattern}"):
        try:
            yield file_reader(path_file), path_file.name, num_files_error
            num_files_error = 0
        except exceptions.MeasureSoftGramCLIException as e:
            print(f"[green]Reading:[/] [black]{path_file.name}[/]")
            print(f"[red]Error  : {e}\n")
            num_files_error += 1


def open_json_file(path_file: Path, disable=False):
    try:
        with rich.progress.open(
            path_file,
            "rb",
            description=path_file.name,
            disable=disable,
            style="bar.back",
            complete_style="bar.complete",
            finished_style="bar.finished",
            pulse_style="bar.pulse",
        ) as file:
            return json.load(file)

    except FileNotFoundError:
        raise exceptions.FileNotFound("The file was not found")
    except IsADirectoryError:
        raise exceptions.UnableToOpenFile(f"File {path_file.name} is a directory")
    except json.JSONDecodeError as error:
        raise exceptions.InvalidMetricsJsonFile(f"Failed to decode the JSON file. {error}")


def get_missing_keys_str(attrs, required_attrs):
    missing_keys = [req_key for req_key in required_attrs if req_key not in attrs]
    return ", ".join(missing_keys)


def check_sonar_format(json_data):
    attributes = list(json_data.keys())
    missing_keys = get_missing_keys_str(attributes, REQUIRED_SONAR_JSON_KEYS)

    if len(missing_keys) > 0:
        raise exceptions.InvalidMetricsJsonFile(
            f"Invalid Sonar JSON keys. Missing keys are: {missing_keys}"
        )

    base_component = json_data["baseComponent"]
    base_component_attrs = list(base_component.keys())
    missing_keys = get_missing_keys_str(base_component_attrs, REQUIRED_SONAR_BASE_COMPONENT_KEYS)

    if len(missing_keys) > 0:
        raise exceptions.InvalidMetricsJsonFile(
            f"Invalid Sonar baseComponent keys. Missing keys are: {missing_keys}"
        )

    base_component_measures = base_component["measures"]
    base_component_measures_attrs = [bc["metric"] for bc in base_component_measures]
    missing_keys = get_missing_keys_str(base_component_measures_attrs, REQUIRED_TRK_MEASURES)

    if len(missing_keys) > 0:
        raise exceptions.InvalidMetricsJsonFile(
            f"Invalid Sonar baseComponent TRK measures. Missing keys are: {missing_keys}"
        )

    if len(json_data["components"]) == 0:
        raise exceptions.InvalidMetricsJsonFile("File with valid schema but no metrics data.")


def check_file_extension(file_name):
    if file_name.split(".")[-1] != "json":
        raise exceptions.InvalidMetricsJsonFile("Only JSON files are accepted.")


def raise_invalid_metric(key, metric):
    raise exceptions.InvalidMetricException(
        f'Invalid metric value in "{key}" component for the "{metric}" metric'
    )


def check_metrics_values(json_data):
    try:
        for component in json_data["components"]:
            for measure in component["measures"]:
                value = measure["value"]

                try:
                    if value is None or math.isnan(float(value)):
                        raise_invalid_metric(component["key"], measure["metric"])
                except (ValueError, TypeError):
                    raise_invalid_metric(component["key"], measure["metric"])
    except KeyError as e:
        raise exceptions.InvalidMetricsJsonFile(
            "Failed to validate Sonar JSON metrics. Please check if the file is a valid Sonar JSON"
        ) from e


def validate_metrics_post(response_status):
    if 200 <= response_status <= 299:
        return "OK: Metrics uploaded successfully"

    return f"FAIL: The host service server returned a {response_status} error. Trying again"
