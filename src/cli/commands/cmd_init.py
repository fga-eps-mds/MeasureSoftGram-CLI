import logging
import sys
import os
import json

from termcolor import colored

from src.cli.exceptions import MeasureSoftGramCLIException
from staticfiles import DEFAULT_PRE_CONFIG

logger = logging.getLogger("msgram")


def command_init(args):
    try:
        dir_path = args["dir_path"]

    except Exception as e:
        logger.warning(f"KeyError: args['{e}'] - non-existent parameters")
        logger.error("Exiting with error ...")
        sys.exit(1)

    logger.info(dir_path)

    if os.path.isdir(dir_path):
        logger.warning(f"FileExistsError: directory \"{dir_path}\" already exists")
        logger.error("Exiting with error ...")
        sys.exit(1)

    os.mkdir(dir_path)
    with open(f"{dir_path}/msgram.json", "w") as f:
        f.write(json.dumps(DEFAULT_PRE_CONFIG, indent=4))
