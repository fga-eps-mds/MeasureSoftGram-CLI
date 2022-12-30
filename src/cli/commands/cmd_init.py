import logging
import sys

from termcolor import colored
from src.cli.exceptions import MeasureSoftGramCLIException

logger = logging.getLogger("msgram")

def command_init(args):
    try:
        file_path = args["file_path"]
        host_url = args["host"]

    except Exception as e:
        logger.warning(f"KeyError: args['{e}'] - non-existent parameters")
        logger.error("Exiting with error ...")
        sys.exit(1)
    
    logger.info(f"file_path: {file_path}")
    logger.info(f"host_url: {host_url}")
