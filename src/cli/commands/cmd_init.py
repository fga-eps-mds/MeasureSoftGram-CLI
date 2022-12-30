import logging
import sys

from termcolor import colored
from src.cli.exceptions import MeasureSoftGramCLIException


def command_init(args):
    try:
        file_path = args["file_path"]
        host_url = args["host"]

    except Exception as e:
        print(f"KeyError: args['{e}'] - non-existent parameters")
        print("Exiting with error ...")
        sys.exit(1)
