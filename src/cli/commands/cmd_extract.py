import re
import sys
import json

import datetime as dt

from termcolor import colored

from src.cli.jsonReader import folder_reader
from src.cli.exceptions import exceptions
from src.cli.utils import print_import_files

# from src.cli.parsers.sonarqube import Sonarqube
from core.parsers.sonarqube import Sonarqube


def get_infos_from_name(filename: str) -> str:
    """
    filename: str = fga-eps-mds-2022-1-MeasureSoftGram-Service-09-11-2022-16-11-42-develop.json
    """
    file_date = re.search(r"\d{1,2}-\d{1,2}-\d{4}-\d{1,2}-\d{1,2}", filename)
    file_name = filename[:file_date.regs[0][0] - 1].split('/')[1]

    if not file_date:
        message = (
            "Could not extract creation date from file. Was the file name "
            "to contain a date in the format dd-mm-yyyy-hh-mm"
        )
        print(colored(message, "red"))
        print(colored(f"filename: {filename}", "red"))
        sys.exit(1)

    date_str = file_date[0]
    month, day, year, hour, minutes = date_str.split("-")

    return f'{file_name}-extracted.msgram', dt.datetime.strptime(
        f"{year}-{month}-{day} {hour}:{minutes}",
        "%Y-%m-%d %H:%M",
    ).isoformat()


def command_extract(args):
    try:
        output_origin = args["output_origin"]
        dir_path = args["dir_path"]
        language_extension = args["language_extension"]

    except Exception as e:
        print(f"KeyError: args['{e}'] - non-existent parameters")
        sys.exit(1)  

    print(f"--> Starting to parser extract for {output_origin} output...\n")

    try:
        components, files = folder_reader(f"{dir_path}")
    except (exceptions.MeasureSoftGramCLIException, FileNotFoundError):
        print("Error: The folder was not found")
        return

    print_import_files(files)

    parser = Sonarqube() if output_origin == 'sonarqube' else None
    for filename, component in zip(files, components):
        print(f"--> Extracting {output_origin} metrics from {filename}...")
        name, created_at = get_infos_from_name(filename)

        result = parser.extract_supported_metrics(component)

        print(f"\n--> Saving results from in {name}...")
        with open(name, 'w') as f:
            f.write(json.dumps(result, indent=4))

    print("\nAttempt to extract metrics from all files in the directory finished!")
