import argparse
import json
import sys
import requests
import signal
import textwrap
from pathlib import Path
from src.cli.jsonReader import (
    file_reader,
    validate_metrics_post
)
from src.cli.exceptions import MeasureSoftGramCLIException
from src.cli.create import (
    validate_preconfig_post,
    preconfig_file_reader
)

BASE_URL = "http://localhost:5000/"


def sigint_handler(*_):
    print("\n\nExiting MeasureSoftGram...")
    sys.exit(0)


def parse_import(file_path, id):
    try:
        components = file_reader(r"{}".format(file_path))
    except MeasureSoftGramCLIException as error:
        print("Error: ", error)
        return

    payload = {"pre_config_id": id, "components": components}

    response = requests.post(BASE_URL + "import-metrics", json=payload)

    validate_metrics_post(response.status_code, json.loads(response.text))


def parse_create(file_path):
    available_pre_config = requests.get(
        BASE_URL + "available-pre-configs", headers={"Accept": "application/json"}
    ).json()

    preconfig = preconfig_file_reader(r"{}".format(file_path), available_pre_config)

    response = requests.post(BASE_URL + "/pre-configs", json=preconfig)
    print(response.text)

    saved_preconfig = json.loads(response.text)

    validate_preconfig_post(response.status_code, saved_preconfig)


def get_available_preconfig_help_string():

    available_pre_configs = requests.get(
        BASE_URL + "available-pre-configs",
        headers={"Accept": "application/json"}
    ).json()

    message = "\nThese are all items available in the MeasureSoftGram database in the following order:\
            \nCharacteristics -> Subcharacteristics -> Measures -> Necessary Metrics"

    for characteristic in available_pre_configs["characteristics"]:
        message = message + (
            "\n\n    {}:".format(available_pre_configs["characteristics"][characteristic]["name"]))

        for subcharacteristic in available_pre_configs["subcharacteristics"]:
            if available_pre_configs["characteristics"][characteristic]["name"].lower().replace(" ", "_") in \
                    available_pre_configs["subcharacteristics"][subcharacteristic]["characteristics"]:
                message = message + (
                    "\n        {}:".format(available_pre_configs["subcharacteristics"][subcharacteristic]["name"]))

                for measure in available_pre_configs["measures"]:
                    if available_pre_configs["subcharacteristics"][subcharacteristic]["name"]\
                        .lower().replace(" ", "_") in \
                            available_pre_configs["measures"][measure]["subcharacteristics"]:
                        message = message + (
                            "\n            {}:".format(available_pre_configs["measures"][measure]["name"]))
                        message = message + \
                            ("\n                {}".format(
                                ', '.join(available_pre_configs["measures"][measure]["metrics"])))

    return message


def setup():
    parser = argparse.ArgumentParser(
        description="Command line interface for measuresoftgram"
    )
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    parser_import = subparsers.add_parser("import", help="Import a metrics file")

    parser_import.add_argument(
        "path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the data directory",
    )

    parser_import.add_argument(
        "id",
        type=str,
        help="Pre config ID",
    )

    # subparsers.add_parser("create", help="Create a new model pre configuration")

    parser_create = subparsers.add_parser(
        "create",
        help="Import preconfig by file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(get_available_preconfig_help_string())
    )

    parser_create.add_argument(
        "path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the data directory",
    )

    args = parser.parse_args()

    # if args is empty show help
    if not sys.argv[1:]:
        parser.print_help()
        return
    elif args.command == "import":
        parse_import(args.path, args.id)
    elif args.command == "create":
        parse_create(args.path)


def main():
    """Entry point for the application script"""

    signal.signal(signal.SIGINT, sigint_handler)

    try:
        setup()
    except KeyboardInterrupt:
        print("\nYou pressed Ctrl + C! No pre conf created.")
