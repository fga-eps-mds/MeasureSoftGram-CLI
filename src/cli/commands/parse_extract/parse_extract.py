import re

import sys

import datetime as dt

from termcolor import colored

from src.cli.jsonReader import folder_reader
from src.cli.exceptions import exceptions


def get_created_at_from_filename(filename: str) -> str:
    """
    filename: str = fga-eps-mds-2022-1-MeasureSoftGram-Service-09-11-2022-16-11-42-develop.json
    """
    result = re.search(r"\d{1,2}-\d{1,2}-\d{4}-\d{1,2}-\d{1,2}", filename)

    if not result:
        message = (
            "Could not extract creation date from file. Was the file name "
            "to contain a date in the format dd-mm-yyyy-hh-mm"
        )
        print(colored(message, "red"))
        print(colored(f"filename: {filename}", "red"))
        sys.exit(1)

    date_str = result[0]
    month, day, year, hour, minutes = date_str.split("-")

    return dt.datetime.strptime(
        f"{year}-{month}-{day} {hour}:{minutes}",
        "%Y-%m-%d %H:%M",
    ).isoformat()


def parse_extract(
    output_origin,
    dir_path,
    language_extension,
):
    print(f"--> Starting to parser extract for {output_origin} output...\n")

    try:
        components, files = folder_reader(f"{dir_path}")
    except (exceptions.MeasureSoftGramCLIException, FileNotFoundError):
        print("Error: The folder was not found")
        return

    print_import_files(files)

    for filename, component in zip(files, components):
        print(f"--> Extracting {output_origin} from {filename}...")
        created_at = get_created_at_from_filename(filename)

    print("\nAttempt to save all files in the directory finished!")
