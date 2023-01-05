import re
import os
import sys
import json
import logging

import datetime as dt

from termcolor import colored

from src.cli.jsonReader import folder_reader
from src.cli.exceptions import exceptions
from src.cli.utils import print_import_files

from parsers.sonarqube import Sonarqube

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
        print(colored(message, "red"))
        print(colored(f"filename: {filename}", "red"))
        sys.exit(1)

    file_name = filename[:file_date.regs[0][0] - 1].split('/')[1]

    date_str = file_date[0]
    month, day, year, hour, minutes = date_str.split("-")

    return f'{file_name}-extracted.msgram', dt.datetime.strptime(
        f"{year}-{month}-{day} {hour}:{minutes}",
        "%Y-%m-%d %H:%M",
    ).isoformat()


def command_extract(args):
    try:
        output_origin = args["output_origin"]
        config_dir_path = args["config_dir_path"]
        dir_path = args["dir_path"]
        language_extension = args["language_extension"]

    except Exception as e:
        logger.error(f"KeyError: args['{e}'] - non-existent parameters")
        exit(1)

    if not os.path.isdir(config_dir_path):
        logger.error(f"FileNotFoundError: config directory \"{config_dir_path}\" does not exists")
        sys.exit(1)

    logger.info(f"--> Starting to parser extract for {output_origin} output...\n")

    logger.debug(f"output_origin: {output_origin}")
    logger.debug(f"dir_path: {dir_path}")
    logger.debug(f"language_extension: {language_extension}")

    try:
        components, files = folder_reader(f"{dir_path}")
    except (exceptions.MeasureSoftGramCLIException, FileNotFoundError):
        logger.error("Error: The folder was not found")
        sys.exit(1)

    print_import_files(files)

    parser = Sonarqube() if output_origin == 'sonarqube' else None
    for filename, component in zip(files, components):
        logger.info(f"--> Extracting {output_origin} metrics from {filename}...")
        name, created_at = get_infos_from_name(filename)

        result = parser.extract_supported_metrics(component)

        logger.info(f"\n--> Saving results from in {name}...")
        with open(f"{config_dir_path}/{name}", 'w') as f:
            f.write(json.dumps(result, indent=4))

    logger.info("\nAttempt to extract metrics from all files in the directory finished!")
