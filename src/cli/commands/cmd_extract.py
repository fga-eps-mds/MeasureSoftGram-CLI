from datetime import datetime
import json
import logging
import os
import re
import sys
from time import perf_counter

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
)

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

    return f"{file_name}-extracted.msgram"


def command_extract(args):
    time_init = perf_counter()
    try:
        output_origin = args["output_origin"]
        extracted_path = args["extracted_path"]
        data_path = args.get("data_path", None)
        language_extension = args["language_extension"]
        repository_path = args.get("repository_path", None)

    except Exception as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_warn(f"KeyError: args[{e}] - non-existent parameters")
        exit(1)

    if data_path is None and repository_path is None:
        logger.error(
            "It is necessary to pass the data_path or repository_path parameters"
        )
        print_warn(
            "It is necessary to pass the data_path or repository_path parameters"
        )
        sys.exit(1)

    console = Console()
    console.clear()
    print_rule("Extract metrics")
    parser = GenericParser()

    if repository_path and output_origin == "github":
        result = parser.parse(input_value=repository_path, type_input=output_origin)
        repository_name = repository_path.replace("/", "-")
        save_file_with_results(
            ".msgram",
            repository_path,
            name=f"github_{repository_name}-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}-extracted.msgram",
            result=result,
        )
        return

    if not os.path.isdir(extracted_path):
        logger.error(
            f'FileNotFoundError: extract directory "{extracted_path}" does not exists'
        )
        print_warn(
            f"FileNotFoundError: extract directory[blue]'{extracted_path}'[/]does not exists"
        )
        sys.exit(1)

    logger.debug(f"output_origin: {output_origin}")
    logger.debug(f"data_path: {data_path}")
    logger.debug(f"language_extension: {language_extension}")
    logger.debug(f"extracted_path: {extracted_path}")

    files = list(data_path.glob("*.json"))
    valid_files = len(files)

    print_info(f"\n> Extract and save metrics [[blue ]{output_origin}[/]]:")
    with make_progress_bar() as progress_bar:
        task_request = progress_bar.add_task(
            "[#A9A9A9]Extracting files: ", total=len(files)
        )
        progress_bar.advance(task_request)

        for component, filename, files_error in folder_reader(data_path, "json"):
            if files_error:
                progress_bar.update(task_request, advance=files_error)
                valid_files = valid_files - files_error

            name = get_infos_from_name(filename)
            result = parser.parse(input_value=component, type_input=output_origin)

            save_file_with_results(extracted_path, filename, name, result)

            progress_bar.advance(task_request)

        time_extract = perf_counter() - time_init
        print_info(
            f"\n\nMetrics successfully extracted [[blue bold]{valid_files}/{len(files)} "
            f"files - {time_extract:0.2f} seconds[/]]!"
        )
    print_panel(
        "> Run [#008080]msgram calculate all -ep 'extracted_path' -cp 'extracted_path' -o 'output_origin'"
    )


def save_file_with_results(extracted_path, filename, name, result):
    print(f"[dark_green]Reading:[/] [black]{filename}[/]")
    print(f"[dark_green]Save   :[/] [black]{name}[/]\n")

    with open(f"{extracted_path}/{name}", "w") as f:
        f.write(json.dumps(result, indent=4))
