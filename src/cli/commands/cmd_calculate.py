import csv
import json
import logging
import re
from pathlib import Path

from anytree import Node, RenderTree

from rich import print
from rich.console import Console
from staticfiles import DEFAULT_PRE_CONFIG as pre_config

from src.cli.jsonReader import open_json_file, read_multiple_files
from src.cli.resources.characteristic import calculate_characteristics
from src.cli.resources.measure import calculate_measures
from src.cli.resources.tsqmi import calculate_tsqmi
from src.cli.resources.subcharacteristic import calculate_subcharacteristics
from src.cli.utils import print_error, print_info, print_panel, print_rule, print_table
from src.cli.exceptions import exceptions
from src.config.settings import DEFAULT_CONFIG_PATH, FILE_CONFIG
from src.cli.resources.perf_eff_measure import calculate_perf_eff_measures

logger = logging.getLogger("msgram")


def read_config_file(config_path):
    try:
        return open_json_file(config_path / FILE_CONFIG)
    except exceptions.MeasureSoftGramCLIException as e:
        print_error(
            f"[red]Error reading msgram.json config file in {config_path}: {e}\n"
        )
        print_rule()
        exit(1)


# calculate_sonar
# calculate_github


def calculate_metrics(extracted_path, config):
    data_calculated = []

    print(extracted_path)
    if not extracted_path.is_file():
        # should not aggregate
        # if not aggregate_metrics(input_format, extracted_path, config):
        #    print_error(
        #        "> [red] Failed to aggregate metrics, calculate was not performed. \n"
        #    )
        #    return data_calculated, False

        for file, file_name in read_multiple_files(extracted_path, "metrics"):
            print(file_name)
            if file_name.startswith("perf-eff_"):
                file_name = file_name[len("perf-eff_") :]
                result = calculate_perf_eff_measures(file_name, file)
                data_calculated.append(result)
            else:
                if file_name.startswith("github_"):
                    file_name = file_name[len("github_") :]
                result = calculate_all(file, file_name, config)
                data_calculated.append(result)

        return data_calculated, True
    else:
        try:
            file_name = extracted_path.name
            if extracted_path.name.startswith("github_"):
                file_name = file_name[len("github_") :]
            result = calculate_all(open_json_file(extracted_path), file_name, config)
            data_calculated.append(result)
            return data_calculated, True
        except exceptions.MeasureSoftGramCLIException as e:
            print_error(f"[red]Error calculating {extracted_path}: {e}\n")
            return data_calculated, False


def command_calculate(args):
    try:
        output_format: str = args["output_format"]
        # input_format: str = args["input_format"]
        config_path = args["config_path"]
        extracted_path = args["extracted_path"]

    except KeyError as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        exit(1)

    console = Console()
    console.clear()
    print_rule("Calculate")
    print_info("> [blue] Reading config file:[/]")

    config = read_config_file(config_path)

    print_info("\n> [blue] Reading extracted files:[/]")

    data_calculated, success = calculate_metrics(extracted_path, config)

    if success:
        print_info("\n[#A9A9A9]All calculations performed[/] successfully!")

    show_results(output_format, data_calculated, config_path)
    print_rule()

    print_panel(
        title="Done",
        menssage="> See the publications for more information: \n"
        "https://dl.acm.org/doi/10.1145/3239235.3267438 \n"
        "https://dl.acm.org/doi/10.1145/3422392.3422450 \n",
    )


def calculate_all(json_data, file_name, config):
    data_measures, _ = calculate_measures(json_data, config)
    data_subcharacteristics, _ = calculate_subcharacteristics(
        config, data_measures["measures"]
    )
    data_characteristics, _ = (
        calculate_characteristics(config, data_subcharacteristics["subcharacteristics"])
        if data_subcharacteristics["subcharacteristics"]
        else ([], [])
    )
    data_tsqmi, _ = (
        calculate_tsqmi(config, data_characteristics["characteristics"])
        if data_characteristics
        else ([], [])
    )

    version = re.search(r"\d{1,2}-\d{1,2}-\d{4}-\d{1,2}-\d{1,2}", file_name)[0]
    repository = file_name.split(version)[0][:-1]

    return {
        "repository": [{"key": "repository", "value": repository}],
        "version": [{"key": "version", "value": version}] if version else [],
        "measures": data_measures["measures"] if data_measures else [],
        "subcharacteristics": (
            data_subcharacteristics["subcharacteristics"]
            if data_subcharacteristics
            else []
        ),
        "characteristics": (
            data_characteristics["characteristics"] if data_characteristics else []
        ),
        "tsqmi": data_tsqmi["tsqmi"] if data_tsqmi else [],
    }


def show_results(output_format, data_calculated, config_path):

    if output_format == "tabular":
        show_tabulate(data_calculated[0])

    elif output_format == "raw":
        print(data_calculated[0])

    elif output_format == "tree":
        show_tree(data_calculated[0], pre_config)

    elif len(data_calculated) == 0:
        print_info(
            f"[yellow]WARNING: No extracted file read so no {output_format} was generated!"
        )

    elif output_format == "csv":
        print_info("Exporting CSV...")
        export_csv(data_calculated, config_path)

    elif output_format == "json":
        print_info("Exporting JSON...")
        export_json(data_calculated, config_path)


def show_tabulate(data_calculated):
    tsqmi = data_calculated["tsqmi"][0]
    characteristics = {c["key"]: c["value"] for c in data_calculated["characteristics"]}
    subcharacteristics = {
        sc["key"]: sc["value"] for sc in data_calculated["subcharacteristics"]
    }
    measures = {m["key"]: m["value"] for m in data_calculated["measures"]}

    print_table(measures, "measures", "measures")
    print_table(subcharacteristics, "subcharacteristics", "subcharacteristics")
    print_table(characteristics, "characteristics", "characteristics")
    print_table(tsqmi, "tsqmi", "tsqmi")


def get_obj_by_element(object_list: list, element_key: str, element_to_find):
    return next((obj for obj in object_list if obj[element_key] == element_to_find), {})


def show_tree(data_calculated, pre_config):
    tsqmi = data_calculated["tsqmi"][0]
    characteristics = data_calculated["characteristics"]
    subcharacteristics = data_calculated["subcharacteristics"]
    measures = data_calculated["measures"]

    print("Overview - tree:\n\n")
    tsqmi_tree = Node(f"[green]{tsqmi['key']}: {tsqmi['value']}")

    for char_c, char in zip(pre_config["characteristics"], characteristics):
        char_tree = Node(f"[red]{char['key']}: {char['value']}", parent=tsqmi_tree)

        for subchar_c in char_c["subcharacteristics"]:
            subchar = get_obj_by_element(subcharacteristics, "key", subchar_c["key"])
            if subchar:
                sub_char_tree = Node(
                    f"[blue]{subchar['key']} {subchar['value']}", parent=char_tree
                )

                for measure_c in subchar_c["measures"]:
                    measure = get_obj_by_element(measures, "key", measure_c["key"])
                    if measure:
                        Node(
                            f"[yellow]{measure['key']} {measure['value']}",
                            parent=sub_char_tree,
                        )

    for pre, fill, node in RenderTree(tsqmi_tree):
        print(f"{pre}{node.name}")


def export_json(data_calculated: list, file_path: Path = DEFAULT_CONFIG_PATH):
    file_path = file_path.joinpath("calc_msgram.json")
    with open(file_path, "w", encoding="utf-8") as write_file:
        json.dump(
            data_calculated,
            write_file,
            indent=4,
        )
    print_info(f"[blue]Success:[/] {file_path.name} [blue]exported as JSON")


def export_csv(data_calculated: list, file_path: Path = Path("DEFAULT_CONFIG_PATH")):
    file_path = file_path.joinpath("calc_msgram.csv")

    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        csv_header = []
        csv_rows = []

        for item in data_calculated:
            if isinstance(item, dict):
                header_column = []
                columns = []

                for _, value in item.items():
                    for column in value:
                        header_column.append(column["key"])
                        columns.append(column["value"])

                csv_header.extend(header_column)
                csv_rows.append(columns)

        writer.writerow(csv_header)
        writer.writerows(csv_rows)

    print(f"Success: {file_path.name} exported as CSV")
