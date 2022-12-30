import logging
import sys
from src.cli.exceptions import MeasureSoftGramCLIException


def command_import(args):
    try:
        output_origin = args["output_origin"]
        dir_path = args["dir_path"]
        language_extension = args["language_extension"]
        host = args["host"]

    except Exception as e:
        print(f"KeyError: args['{e}'] - non-existent parameters")
        print("Exiting with error ...")
        sys.exit(1)

