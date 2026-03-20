import logging
from core.transformations import norm_diff
from src.cli.jsonReader import open_json_file
from src.cli.utils import (
    print_error,
    print_info,
    print_rule,
    validate_json_values,
)
from src.cli.exceptions import exceptions
import numpy as np

logger = logging.getLogger("msgram")


def read_planned_file(file_path, sort_key=None):
    try:
        json_data = open_json_file(file_path)
        return sorted(json_data, key=lambda x: x[sort_key]) if sort_key else json_data
    except exceptions.MeasureSoftGramCLIException as e:
        print_error(f"[red]Error reading planned file in {file_path}: {e}\n")
        print_rule()
        exit(1)


def read_calculated_file(file_path):
    try:
        calculated_data = []
        json = open_json_file(file_path)
        for item in json:
            characteristics = sorted(item["characteristics"], key=lambda x: x["key"])
            repository = item["repository"][0]["value"]
            version = item["version"][0]["value"]
            calculated_data.append(
                {
                    "repository": repository,
                    "version": version,
                    "characteristics": characteristics,
                }
            )

        return calculated_data
    except exceptions.MeasureSoftGramCLIException as e:
        print_error(f"[red]Error reading calculated file in {file_path}: {e}\n")
        print_rule()
        exit(1)


def command_norm_diff(args):
    try:
        rp_path = args["rp_path"]
        rd_path = args["rd_path"]
    except KeyError as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        exit(1)

    planned_data = read_planned_file(rp_path, sort_key="key")

    calculated_data = read_calculated_file(rd_path)

    planned_vector, calculated_vector = extract_values(
        planned_data, calculated_data, rp_path, rd_path
    )
    norm_diff_value = norm_diff(planned_vector, calculated_vector)

    print_info("\n[#A9A9A9]Norm diff calculation performed successfully![/]\n")

    print_info(
        "[#A9A9A9]The norm_diff value indicates the difference between the observed "
        "quality (Rd) and the planned target (Rp). A norm_diff of 0 means that the "
        "observed quality perfectly aligns with the planned target. If norm_diff is "
        "not equal to 0, it shows a deviation from the target. In this case, you "
        "should determine whether the performance is above or below the planned "
        "quality. For a detailed analysis of these differences, use the msgram diff "
        "command.[/]\n"
    )

    print(f"Norm Diff: {norm_diff_value}")
    print_rule()


def extract_values(planned_data, calculated_data, rp_path, rd_path):
    try:
        planned = planned_data
        calculated = []
        for item in calculated_data:
            for characteristic in item["characteristics"]:
                calculated.append(
                    {"key": characteristic["key"], "value": characteristic["value"]}
                )

        planned_keys = {item["key"].strip() for item in planned}
        calculated_keys = {item["key"].strip() for item in calculated}

        if planned_keys != calculated_keys:
            raise exceptions.MeasureSoftGramCLIException(
                "Planned and calculated files have different characteristics"
            )

        planned_dict = {item["key"].strip(): item["value"] for item in planned}
        calculated_dict = {item["key"].strip(): item["value"] for item in calculated}

        planned_values = [planned_dict[key] for key in planned_keys]
        calculated_values = [calculated_dict[key] for key in planned_keys]

        validate_json_values(planned_values, rp_path)
        validate_json_values(calculated_values, rd_path)

        return (np.array(planned_values), np.array(calculated_values))
    except exceptions.MeasureSoftGramCLIException as e:
        print_error(f"[red]Error extracting values: {e}\n")
        print_rule()
        exit(1)
