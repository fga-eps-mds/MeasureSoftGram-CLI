from src.cli import exceptions
import json


METRICS_SONAR = [
    "files",
    "functions",
    "complexity",
    "comment_lines_density",
    "duplicated_lines_density",
    "coverage",
    "ncloc",
    "tests",
    "test_errors",
    "test_failures",
    "test_execution_time",
    "security_rating",
]

REQUIRED_SONAR_JSON_KEYS = ["paging", "baseComponent", "components"]

REQUIRED_SONAR_BASE_COMPONENT_KEYS = [
    "id",
    "key",
    "name",
    "qualifier",
    "measures",
]


def file_reader(absolute_path):
    check_file_extension(absolute_path)

    json_data = open_json_file(absolute_path)

    check_sonar_format(json_data)

    return json_data["components"]


def open_json_file(absolute_path):
    try:
        with open(absolute_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise exceptions.FileNotFound("The file was not found")
    except OSError as error:
        raise exceptions.UnableToOpenFile(f"Failed to open the file. Error: {error}")
    except json.JSONDecodeError as error:
        raise exceptions.InvalidMetricsJsonFile(
            f"Failed to decode the JSON file. Error: {error}"
        )


def get_missing_keys_str(attrs, required_attrs):
    missing_keys = []

    for req_key in required_attrs:
        if req_key not in attrs:
            missing_keys.append(req_key)

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
    missing_keys = get_missing_keys_str(
        base_component_attrs, REQUIRED_SONAR_BASE_COMPONENT_KEYS
    )

    if len(missing_keys) > 0:
        raise exceptions.InvalidMetricsJsonFile(
            f"Invalid Sonar baseComponent keys. Missing keys are: {missing_keys}"
        )

    if len(json_data["components"]) == 0:
        raise exceptions.InvalidMetricsJsonFile(
            "Invalid Sonar JSON components value. It must have at least one component"
        )


def check_file_extension(fileName):
    if fileName[-4:] != "json":
        raise exceptions.InvalidMetricsJsonFile("Only JSON files are accepted")


def validate_metrics_post(response_status, response):
    if response_status == 201:
        print("\nThe imported metrics were saved for the pre-configuration")
    else:
        print("\nThere was a ERROR while saving your Metrics:\n")

        for key, value in response.items():
            field_name = "General" if key == "__all__" else key

            print(f"\t{field_name} => {value}")
