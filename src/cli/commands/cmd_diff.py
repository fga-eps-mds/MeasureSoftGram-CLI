import csv
import json
import logging
from pathlib import Path

from rich import print
from rich.console import Console

from core.transformations import diff

from src.cli.jsonReader import open_json_file
from src.cli.utils import (
    print_diff_table,
    print_error,
    print_info,
    print_panel,
    print_rule,
    validate_json_values,
)
from src.cli.exceptions import exceptions
from src.config.settings import DEFAULT_CONFIG_PATH

logger = logging.getLogger("msgram")


def read_config_file(config_path):
    try:
        json = open_json_file(config_path)

        return sorted(json, key=lambda x: x["key"])
    except exceptions.MeasureSoftGramCLIException as e:
        print_error(f"[red]Error reading config file in {config_path}: {e}\n")
        print_rule()
        exit(1)


def read_calculated_file(extracted_calculation):
    try:
        calculated_data = []

        json = open_json_file(extracted_calculation)

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
        print_error(
            f"[red]Error reading calculated file in {extracted_calculation}: {e}\n"
        )
        print_rule()
        exit(1)


def calculate_diff(planned, calculated, rp_path, rd_path):
    formated_result = []

    try:
        for calculated_item in calculated:
            diff_values = []
            if len(calculated_item["characteristics"]) != len(planned):
                raise exceptions.MeasureSoftGramCLIException(
                    "The size between planned and developed release vectors is not equal."
                )

            data_planned, data_calculated = extract_values(
                planned, calculated_item["characteristics"], rp_path, rd_path
            )

            diff_calculated = diff(data_planned, data_calculated)

            for index in range(len(planned)):
                diff_values.append(
                    {
                        "key": planned[index]["key"],
                        "planned": planned[index]["value"],
                        "developed": calculated_item["characteristics"][index]["value"],
                        "diff": diff_calculated[index],
                    }
                )

            formated_result.append(
                {
                    "repository": calculated_item["repository"],
                    "version": calculated_item["version"],
                    "characteristics": diff_values,
                }
            )

        return formated_result, True
    except exceptions.MeasureSoftGramCLIException as e:
        print_error(f"[red]Error calculating: {e}\n")
        return formated_result, False


def command_diff(args):
    try:
        output_format: str = args["output_format"]
        config_path = args["rp_path"]
        extracted_calculation = args["rd_path"]

    except KeyError as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        exit(1)

    console = Console()
    console.clear()
    print_rule("Calculate")
    print_info("> [blue] Reading config file:[/]")

    planned = read_config_file(config_path)

    print_info("\n> [blue] Reading calculated file:[/]")

    calculated = read_calculated_file(extracted_calculation)

    diff_calculated, success = calculate_diff(
        planned, calculated, config_path, extracted_calculation
    )

    if success:
        print_info("\n[#A9A9A9]Diff calculation performed[/] successfully!")
    else:
        exit(1)

    show_results(output_format, diff_calculated, config_path)
    print_rule()

    print_panel(
        title="Done",
        menssage="> See the publications for more information: \n"
        "https://dl.acm.org/doi/10.1145/3239235.3267438 \n"
        "https://dl.acm.org/doi/10.1145/3422392.3422450 \n",
    )


def show_results(output_format, data_calculated, config_path):
    show_tabulate(data_calculated)

    if output_format == "csv":
        print_info("Exporting CSV...")
        export_csv(data_calculated, config_path)

    elif output_format == "json":
        print_info("Exporting JSON...")
        export_json(data_calculated, config_path)


def show_tabulate(data_calculated):
    for calculated in data_calculated:
        characteristics = {
            item["key"]: {k: v for k, v in item.items() if k != "key"}
            for item in calculated["characteristics"]
        }
        print_diff_table(
            characteristics,
            f"{calculated['repository']} - {calculated['version']}",
            "Characteristics",
        )


def export_json(data_calculated: list, file_path: Path = DEFAULT_CONFIG_PATH):
    file_path = file_path.parent.joinpath("calc_diff_msgram.json")
    with open(file_path, "w", encoding="utf-8") as write_file:
        json.dump(
            data_calculated,
            write_file,
            indent=4,
        )
    print_info(f"[blue]Success:[/] {file_path.name} [blue]exported as JSON")


def export_csv(data_calculated: list, file_path: Path = Path("DEFAULT_CONFIG_PATH")):
    file_path = file_path.parent.joinpath("calc_diff_msgram.csv")

    with open(file_path, "w", newline="") as csv_file:
        fieldnames = [
            "repository",
            "version",
            "characteristic",
            "planned",
            "developed",
            "diff",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in data_calculated:
            for row in data["characteristics"]:
                writer.writerow(
                    {
                        "repository": data["repository"],
                        "version": data["version"],
                        "characteristic": row.get("key", ""),
                        "planned": row.get("planned", ""),
                        "developed": row.get("developed", ""),
                        "diff": row.get("diff", ""),
                    }
                )

    print(f"Success: {file_path.name} exported as CSV")


def extract_values(planned, calculated, rp_path, rd_path):
    vector_calculated = []
    vector_planned = []

    for x in range(len(planned)):
        if planned[x]["key"] != calculated[x]["key"]:
            raise exceptions.MeasureSoftGramCLIException(
                "Planned and calculated files have differents characteristics"
            )
        else:
            vector_calculated.append(calculated[x]["value"])
            vector_planned.append(planned[x]["value"])

    validate_json_values(vector_planned, rp_path)
    validate_json_values(vector_calculated, rd_path)

    return vector_planned, vector_calculated
