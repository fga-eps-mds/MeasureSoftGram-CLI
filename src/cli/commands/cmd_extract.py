from datetime import datetime
import json
import logging
import os
import re
import sys
from time import perf_counter
from pathlib import Path

from rich import print
from rich.console import Console
from genericparser import GenericParser

from src.cli.jsonReader import folder_reader
from src.cli.utils import (
    make_progress_bar,
    print_info,
    print_panel,
    print_rule,
    print_warn,
    is_valid_date_range,
)
from src.cli.resources.perf_eff_parser import parse_performance_efficiency_data

logger = logging.getLogger("msgram")


def get_infos_from_name(filename: str) -> str:
    """
    filename: str = fga-eps-mds-2022-1-MeasureSoftGram-Service-09-11-2022-16-11-42-develop.json
    """
    file_date = re.search(r"\d{1,2}-\d{1,2}-\d{4}-\d{1,2}-\d{1,2}", filename)

    if not file_date:
        message = (
            "Could not extract creation date from file. Was the file name "
            "to contain a date in the format dd-mm-yyyy-hh-mm"
        )
        print_warn(message)
        print_warn(f"filename: {filename}")
        sys.exit(1)

    file_name = filename.split(".")[0]

    return f"{file_name}-extracted.metrics"


def parse_input_quotes(user_input):
    # Aspas para normalizar
    quotes = "“‘«”’»"

    if user_input:
        # Remove aspas no início
        user_input = user_input[1:] if user_input[0] in quotes else user_input

        # Remove aspas no final
        user_input = user_input[:-1] if user_input[-1] in quotes else user_input

    return user_input


def extract_github(
    extracted_path: Path,
    gh_repository: str,
    gh_date_range: str,
    gh_label: str,
    gh_workflows: str,
    parser: GenericParser,
):
    input_origin = "github"
    if gh_date_range is not None and not is_valid_date_range(gh_date_range):
        logger.error(
            "Error: Range of dates for filter must be in format 'dd/mm/yyyy-dd/mm/yyyy'"
        )
        print_warn(
            "Error: Range of dates for filter must be in format 'dd/mm/yyyy-dd/mm/yyyy'"
        )
        sys.exit(1)
    filters = {
        "labels": gh_label if gh_label else "US,User Story,User Stories",
        "workflows": gh_workflows.split(",") if gh_workflows else "build",
        "dates": gh_date_range if gh_date_range else None,
    }
    print_info(f"\n> Extract and save metrics [[blue ]{input_origin}[/]]:")
    result = parser.parse(
        input_value=gh_repository, type_input=input_origin, filters=filters
    )
    repository_name = gh_repository.replace("/", "-")
    save_file_with_results(
        extracted_path,
        gh_repository,
        name=f"github_{repository_name}-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}-extracted.metrics",
        result=result,
    )


def extract_sonar(extracted_path: Path, sonar_path: Path, parser: GenericParser):
    time_init = perf_counter()
    input_origin = "sonarqube"

    logger.debug(f"input_origin: {input_origin}")
    logger.debug(f"data_path: {sonar_path}")
    logger.debug(f"extracted_path: {extracted_path}")

    files = list(sonar_path.glob("*.json"))

    if not files:
        print_warn(f"No JSON files found in the specified data_path: {sonar_path}\n")
        sys.exit(1)

    valid_files = len(files)

    print_info(f"\n> Extract and save metrics [[blue ]{input_origin}[/]]:")
    with make_progress_bar() as progress_bar:
        task_request = progress_bar.add_task(
            "[#A9A9A9]Extracting files: ", total=len(files)
        )
        progress_bar.advance(task_request)

        for component, filename, files_error in folder_reader(sonar_path, "json"):
            if files_error:
                progress_bar.update(task_request, advance=files_error)
                valid_files = valid_files - files_error

            name = get_infos_from_name(filename)
            result = parser.parse(input_value=component, type_input=input_origin)

            save_file_with_results(extracted_path, filename, name, result)

            progress_bar.advance(task_request)

        time_extract = perf_counter() - time_init
        print_info(
            f"\n\nMetrics successfully extracted [[blue bold]{valid_files}/{len(files)} "
            f"files - {time_extract:0.2f} seconds[/]]!"
        )


def extract_perf_eff():
    pass


def command_extract(args):
    try:
        extracted_path = args["extracted_path"]
        sonar_path = args.get("sonar_path", None)
        gh_repository = args.get("gh_repository", None)
        gh_label = args.get("gh_label", None)
        gh_workflows = args.get("gh_workflows", None)
        gh_date_range = args.get("gh_date_range", None)
        pe_release1 = args.get("pe_release_1", None)
        pe_release2 = args.get("pe_release_2", None)
        pe_repository_name = args.get("pe_repository_name", None)

    except Exception as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_warn(f"KeyError: args[{e}] - non-existent parameters")
        exit(1)

    pe_params = (
        (pe_release1 is not None)
        + (pe_release2 is not None)
        + (pe_repository_name is not None)
    )
    if pe_params > 0 and pe_params < 3:
        print_warn(
            "Error: Some pe_ parameters for extracting the performance efficiency data are missing"
        )
        exit()

    # First check if sonar_path and gh_repository are none
    if (sonar_path is None) and (gh_repository is None) and (pe_params == 0):
        logger.error(
            "It is necessary to pass sonar_path, github_repository or the pe_ parameters"
        )
        print_warn(
            "It is necessary to pass sonar_path, github_repository or the pe_ parameters"
        )
        sys.exit(1)

    console = Console()
    console.clear()
    print_rule("Extract metrics")
    parser = GenericParser()

    if not os.path.isdir(extracted_path):
        logger.error(
            f'FileNotFoundError: extract directory "{extracted_path}" does not exists'
        )
        print_warn(
            f"FileNotFoundError: extract directory[blue]'{extracted_path}'[/]does not exists"
        )
        sys.exit(1)

    # Github repository is defined so we should generate github metrics
    if gh_repository:
        extract_github(
            extracted_path, gh_repository, gh_date_range, gh_label, gh_workflows, parser
        )
    elif gh_label or gh_workflows or gh_date_range:
        logger.error(
            "Error: gh_repository must be specified in order to use gh_ parameters"
        )
        print_warn(
            "Error: gh_repository must be specified in order to use gh_ parameters"
        )
        sys.exit(1)

    if pe_params == 3:
        input_origin = "performance-efficiency"
        print_info(f"\n> Extract and save metrics [[blue ]{input_origin}[/]]:")
        # All pe_params are set, so we should extract the performance efficiency data
        parsed_data = parse_performance_efficiency_data(
            pe_release1, pe_release2, pe_repository_name
        )
        save_file_with_results(
            extracted_path,
            pe_repository_name,
            name=f"perf-eff_{pe_repository_name}-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}-extracted.metrics",
            result=parsed_data,
        )

    # Sonargube path is defined so we should generate sonar metrics
    if sonar_path:
        extract_sonar(extracted_path, sonar_path, parser)

    print_panel(
        "> Run [#008080]msgram calculate all -ep 'extracted_path' -cp 'extracted_path' -o 'input_origin'"
    )


def save_file_with_results(extracted_path, filename, name, result):
    print(f"[dark_green]Reading:[/] [black]{filename}[/]")
    print(f"[dark_green]Save   :[/] [black]{name}[/]\n")

    with open(f"{extracted_path}/{name}", "w") as f:
        f.write(json.dumps(result, indent=2))
