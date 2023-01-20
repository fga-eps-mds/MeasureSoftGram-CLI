import csv
import json
import logging
import re
from pathlib import Path

from rich import print
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.tree import Tree
from staticfiles import DEFAULT_PRE_CONFIG as pre_config

from src.cli.jsonReader import open_json_file, read_mult_files
from src.cli.resources.characteristic import calculate_characteristics
from src.cli.resources.measure import calculate_measures
from src.cli.resources.sqc import calculate_sqc
from src.cli.resources.subcharacteristic import calculate_subcharacteristics
from src.cli.utils import print_info, print_panel, print_rule, print_table, print_warn
from src.config.settings import CSV_DEFAULT_FILE_PATH, FILE_CONFIG, JSON_DEFAULT_FILE_PATH

logger = logging.getLogger("msgram")


def command_calculate(args):
    print(args)
    try:
        output_format: str = args["output_format"]
        config_path: Path = args["config_path"]
        extracted_path: Path = args["extracted_path"]
    except Exception as e:
        logger.error(f"KeyError: args['{e}'] - non-existent parameters")
        print.warn(f"KeyError: args['{e}'] - non-existent parameters")
        exit(1)

    console = Console()
    console.clear()
    print_rule("Calculate")
    print_info("> [blue] Reading config file:[/]")

    config = open_json_file(config_path / FILE_CONFIG)

    print_info("\n> [blue] Reading extracted files:[/]")

    isfile = extracted_path.is_file()
    data_calculated = []

    if not isfile:
        for file, file_name in read_mult_files(extracted_path, "msgram"):
            result = calculate_all(file, file_name, config)
            data_calculated.append(result)
    else:
        data_calculated = calculate_all(open_json_file(extracted_path), extracted_path.name, config)
        output_format = Prompt.ask("[black]Display as:", choices=["tabular", "tree", "raw"])

    print_info(f"\n[#A9A9A9]All calculations performed[/] successfully!")
    print_rule()

    if output_format == "tabular":
        show_tabulate(data_calculated)

    elif output_format == "raw":
        show_json(data_calculated)

    elif output_format == "tree":
        show_tree(data_calculated)

    elif output_format == "csv":
        print_info("Exporting CSV...")
        export_csv(data_calculated)
        print_info("[blue] Success:[/] exported as CSV")

    elif output_format == "json":
        print_info("Exporting JSON...")
        export_json(data_calculated)
        print_info("[blue] Success:[/] exported as JSON")

    else:
        print("--")


def calculate_all(json_data, file_name, config):
    data_measures, headers_measures = calculate_measures(json_data)

    data_subcharacteristics, headers_subcharacteristics = calculate_subcharacteristics(
        config, data_measures["measures"]
    )

    data_characteristics, headers_characteristics = calculate_characteristics(
        config, data_subcharacteristics["subcharacteristics"]
    )

    data_sqc, headers_sqc = calculate_sqc(config, data_characteristics["characteristics"])

    version = re.search(r"\d{1,2}-\d{1,2}-\d{4}-\d{1,2}-\d{1,2}", file_name)[0]
    repository = file_name.split(version)[0][:-1]

    return {
        "measures": data_measures["measures"],
        "subcharacteristics": data_subcharacteristics["subcharacteristics"],
        "characteristics": data_characteristics["characteristics"],
        "sqc": data_sqc["sqc"],
        "repository": [{"key": "repositoy", "value": repository}],
        "version": [{"key": "version", "value": version}],
    }


def export_json(data_calculated: list, file_path: Path = JSON_DEFAULT_FILE_PATH):
    with open(file_path, "w", encoding="utf-8") as write_file:
        json.dump(
            data_calculated,
            write_file,
            indent=4,
        )


def export_csv(data_calculated: list, file_path: Path = CSV_DEFAULT_FILE_PATH):
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        csv_header = []
        csv_rows = []

        for row in data_calculated:
            header_column = []
            columns = []
            for _, value in row.items():
                for column in value:
                    header_column.append(column["key"])
                    columns.append(column["value"])
            csv_header.append(header_column)
            csv_rows.append(columns)

        writer.writerow(csv_header[0])
        writer.writerows(csv_rows)
