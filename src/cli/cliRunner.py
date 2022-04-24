import argparse
import json
import sys
import requests
import signal
from pathlib import Path
from src.cli.exceptions import MeasureSoftGramCLIException
from src.cli.jsonReader import file_reader, validate_metrics_post
from src.cli.create import (
    define_characteristic,
    define_sublevel,
    validate_preconfig_post,
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


def parse_create():
    print("Creating a new pre conf")

    available_pre_config = requests.get(
        BASE_URL + "available-pre-configs", headers={"Accept": "application/json"}
    ).json()

    [user_characteristics, caracteristics_weights] = define_characteristic(
        available_pre_config
    )

    [user_sub_characteristic, sub_characteristic_weights] = define_sublevel(
        user_characteristics,
        available_pre_config,
        "characteristics",
        "subcharacteristics",
    )

    [user_measures, measures_weights] = define_sublevel(
        user_sub_characteristic,
        available_pre_config,
        "subcharacteristics",
        "measures",
    )

    data = {
        "characteristics": user_characteristics,
        "subcharacteristics": user_sub_characteristic,
        "measures": user_measures,
        "characteristics_weights": caracteristics_weights,
        "subcharacteristics_weights": sub_characteristic_weights,
        "measures_weights": measures_weights,
    }

    response = requests.post(BASE_URL + "/pre-configs", json=data)

    saved_preconfig = json.loads(response.text)

    validate_preconfig_post(response.status_code, saved_preconfig)


def parse_change_name(pre_config_id, new_name):
    response = requests.patch(
        BASE_URL + f"pre-configs/{pre_config_id}", json={"name": new_name}
    )

    response_data = response.json()

    if 200 <= response.status_code <= 299:
        print(
            f'Your Pre Configuration name was succesfully changed to "{response_data["name"]}"'
        )
    else:
        print(
            f"There was an ERROR while changing your Pre Configuration name:  {response_data['error']}"
        )


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

    subparsers.add_parser("create", help="Create a new model pre configuration")

    change_name = subparsers.add_parser(
        "change-name", help="Change pre configuration name"
    )

    change_name.add_argument(
        "pre_config_id",
        type=str,
        help="Pre config ID",
    )

    change_name.add_argument(
        "new_name",
        type=str,
        help="New pre configuration name",
    )

    args = parser.parse_args()

    # if args is empty show help
    if not sys.argv[1:]:
        parser.print_help()
        return
    elif args.command == "import":
        parse_import(args.path, args.id)
    elif args.command == "create":
        parse_create()
    elif args.command == "change-name":
        parse_change_name(args.pre_config_id, args.new_name)


def main():
    """Entry point for the application script"""

    signal.signal(signal.SIGINT, sigint_handler)

    try:
        setup()
    except KeyboardInterrupt:
        print("\nYou pressed Ctrl + C! No pre conf created.")
