import csv
import json
import logging
import re
from pathlib import Path

from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.tree import Tree
from staticfiles import DEFAULT_PRE_CONFIG as pre_config

from src.cli.jsonReader import open_json_file, read_mult_files
from src.cli.resources.characteristic import calculate_characteristics
from src.cli.resources.measure import calculate_measures
from src.cli.resources.sqc import calculate_sqc
from src.cli.resources.subcharacteristic import calculate_subcharacteristics
from src.cli.utils import print_error, print_info, print_panel, print_rule, print_table
from src.cli.exceptions import exceptions
from src.config.settings import DEFAULT_CONFIG_PATH, FILE_CONFIG

logger = logging.getLogger("msgram")


def command_calculate(args):
    try:
        output_format: str = args["output_format"]
        config_path: Path = args["config_path"]
        extracted_path: Path = args["extracted_path"]
    except Exception as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        exit(1)

    console = Console()
    console.clear()
    print_rule("Calculate")
    print_info("> [blue] Reading config file:[/]")

    try:
        config = open_json_file(config_path / FILE_CONFIG)
    except exceptions.MeasureSoftGramCLIException as e:
        print(f"[red]Error reading msgram.json config file in {config_path}: {e}\n")
        print_rule()
        exit(1)

    print_info("\n> [blue] Reading extracted files:[/]")

    isfile = extracted_path.is_file()
    data_calculated = []
    success = False

    if not isfile:
        for file, file_name in read_mult_files(extracted_path, "msgram"):
            result = calculate_all(file, file_name, config)
            data_calculated.append(result)
            success = True
    else:
        try:
            data_calculated = calculate_all(open_json_file(extracted_path), extracted_path.name, config)
            success = True
            output_format = Prompt.ask("\n\n[black]Display as:", choices=["tabular", "tree", "raw"])
        except exceptions.MeasureSoftGramCLIException as e:
            print(f"[red]Error calculating {extracted_path}: {e}\n")

    if success:
        print_info("\n[#A9A9A9]All calculations performed[/] successfully!")

    show_results(output_format, data_calculated, config_path)
    print_rule()

    print_panel(
        title="Done",
        menssage="> See our docs for more information: \n"
        " https://github.com/fga-eps-mds/2022-2-MeasureSoftGram-CLI",
    )


def calculate_all(json_data, file_name, config):
    data_measures, _ = calculate_measures(json_data)

    data_subcharacteristics, _ = calculate_subcharacteristics(
        config, data_measures["measures"]
    )

    data_characteristics, _ = calculate_characteristics(
        config, data_subcharacteristics["subcharacteristics"]
    )

    data_sqc, _ = calculate_sqc(config, data_characteristics["characteristics"])

    version = re.search(r"\d{1,2}-\d{1,2}-\d{4}-\d{1,2}-\d{1,2}", file_name)[0]
    repository = file_name.split(version)[0][:-1]

    return {
        "repository": [{"key": "repository", "value": repository}],
        "version": [{"key": "version", "value": version}],
        "measures": data_measures["measures"],
        "subcharacteristics": data_subcharacteristics["subcharacteristics"],
        "characteristics": data_characteristics["characteristics"],
        "sqc": data_sqc["sqc"],
    }


def show_results(output_format, data_calculated, config_path):
    if output_format == "tabular":
        show_tabulate(data_calculated)

    elif output_format == "raw":
        print(data_calculated)

    elif output_format == "tree":
        show_tree(data_calculated)

    elif len(data_calculated) == 0:
        print_info(f"[yellow]WARNING: No extracted file readed so no {output_format} was generated!")

    elif output_format == "csv":
        print_info("Exporting CSV...")
        export_csv(data_calculated, config_path)

    elif output_format == "json":
        print_info("Exporting JSON...")
        export_json(data_calculated, config_path)


def show_tabulate(data_calculated):
    sqc = data_calculated["sqc"][0]
    characteristics = {c["key"]: c["value"] for c in data_calculated["characteristics"]}
    subcharacteristics = {sc["key"]: sc["value"] for sc in data_calculated["subcharacteristics"]}
    measures = {m["key"]: m["value"] for m in data_calculated["measures"]}

    print_table(measures, "measures", "measures")
    print_table(subcharacteristics, "subcharacteristics", "subcharacteristics")
    print_table(characteristics, "characteristics", "characteristics")
    print_table(sqc, "sqc", "sqc")


def get_obj_by_element(object_list: list, element_key: str, element_to_find):
    return next((obj for obj in object_list if obj[element_key] == element_to_find), {})


def show_tree(data_calculated):
    sqc = data_calculated["sqc"][0]
    characteristics = data_calculated["characteristics"]
    subcharacteristics = data_calculated["subcharacteristics"]
    measures = data_calculated["measures"]

    print("Overview - tree:\n\n")
    sqc_tree = Tree(f"[green]{sqc['key']}: {sqc['value']}")

    for char_c, char in zip(pre_config["characteristics"], characteristics):
        char_tree = sqc_tree.add(f"[red]{char['key']}: {char['value']}")

        for subchar_c in char_c["subcharacteristics"]:
            subchar = get_obj_by_element(subcharacteristics, "key", subchar_c["key"])
            sub_char_tree = char_tree.add(f"[blue]{subchar['key']} {subchar['value']}")

            for measure_c in subchar_c["measures"]:
                measure = get_obj_by_element(measures, "key", measure_c["key"])
                sub_char_tree.add(f"[yellow]{measure['key']} {measure['value']}")

    print(sqc_tree)


def export_json(data_calculated: list, file_path: Path = DEFAULT_CONFIG_PATH):
    file_path = file_path.joinpath("calc_msgram.json")
    with open(file_path, "w", encoding="utf-8") as write_file:
        json.dump(
            data_calculated,
            write_file,
            indent=4,
        )
    print_info(f"[blue]Success:[/] {file_path.name} [blue]exported as JSON")


def export_csv(data_calculated: list, file_path: Path = DEFAULT_CONFIG_PATH):
    file_path = file_path.joinpath("calc_msgram.csv")
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

    print_info(f"[blue]Success:[/] {file_path.name} [blue]exported as CSV")
