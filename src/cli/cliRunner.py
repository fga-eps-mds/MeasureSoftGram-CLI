import argparse
import json
import sys
import requests
import signal
from pathlib import Path
from src.cli.show import parse_show
from src.cli.list import parse_list
from src.cli.exceptions import MeasureSoftGramCLIException
from src.cli.jsonReader import file_reader, validate_metrics_post
from src.cli.results import validade_analysis_response
from src.cli.create import validate_pre_config_post, pre_config_file_reader
from src.cli.available import parse_available

BASE_URL = "http://localhost:5000/"


def sigint_handler(*_):
    print("\n\nExiting MeasureSoftGram...")
    sys.exit(0)


def parse_analysis(id):
    data = {"pre_config_id": id}
    response = requests.post(BASE_URL + "analysis", json=data)

    validade_analysis_response(response.status_code, response.json())


def parse_import(file_path, id, language_extension):
    try:
        components = file_reader(r"{}".format(file_path))
    except MeasureSoftGramCLIException as error:
        print("Error: ", error)
        return

    payload = {
        "pre_config_id": id,
        "components": components,
        "language_extension": language_extension,
    }

    response = requests.post(BASE_URL + "import-metrics", json=payload)

    validate_metrics_post(response.status_code, json.loads(response.text))


def parse_create(file_path):
    available_pre_config = requests.get(
        BASE_URL + "available-pre-configs", headers={"Accept": "application/json"}
    ).json()

    try:
        pre_config = pre_config_file_reader(
            r"{}".format(file_path), available_pre_config
        )
    except MeasureSoftGramCLIException as error:
        print("Error: ", error)
        return

    response = requests.post(BASE_URL + "/pre-configs", json=pre_config)

    saved_pre_config = json.loads(response.text)

    validate_pre_config_post(response.status_code, saved_pre_config)


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

    parser_import.add_argument(
        "language_extension",
        type=str,
        help="The source code language extension",
    )

    parser_create = subparsers.add_parser(
        "create",
        help="Create a new model pre configuration from a JSON file",
    )

    subparsers.add_parser(
        "available",
        help="Shows all characteristics, sub-characteristics and measures available in measuresoftgram",
    )

    parser_create.add_argument(
        "path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the JSON file",
    )

    parser_analysis = subparsers.add_parser("analysis", help="Get analysis result")
    parser_analysis.add_argument(
        "id",
    )
    subparsers.add_parser("list", help="List all pre configurations")

    parser_show = subparsers.add_parser(
        "show", help="Show all information of a pre configuration"
    )

    parser_show.add_argument(
        "pre_config_id",
        type=str,
        help="Pre config ID",
    )

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
        parse_import(args.path, args.id, args.language_extension)
    elif args.command == "create":
        parse_create(args.path)
    elif args.command == "analysis":
        parse_analysis(args.id)
    elif args.command == "available":
        parse_available()
    elif args.command == "list":
        parse_list()
    elif args.command == "show":
        parse_show(args.pre_config_id)
    elif args.command == "change-name":
        parse_change_name(args.pre_config_id, args.new_name)


def main():
    """Entry point for the application script"""

    signal.signal(signal.SIGINT, sigint_handler)

    setup()
