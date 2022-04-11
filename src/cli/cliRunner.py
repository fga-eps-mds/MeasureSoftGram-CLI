import argparse
import requests
import sys
from src.cli.jsonReader import file_reader
from src.cli.create import (
    define_characteristic,
    define_subcharacteristics,
    define_measures,
    validate_pre_config_metrics_post,
)

BASE_URL = "http://localhost:5000/"


def sigint_handler(*_):
    print("\n\nExiting MeasureSoftGram...")
    sys.exit(0)


def parse_import(file_path, id):
    components = file_reader(r"{}".format(file_path))

    payload = {
        "pre_config_id": id,
        "components": components
    }

    response_pre_config_metrics = requests.post(
        BASE_URL + "pre-config-metrics", data=payload
    )
    validate_pre_config_metrics_post(response_pre_config_metrics.status_code)


def parse_create():
    print("Creating a new pre conf")

    available_pre_config = requests.get(
        BASE_URL + "available-pre-configs", headers={"Accept": "application/json"}
    ).json()

    [user_characteristics, caracteristics_weights] = define_characteristic(
        available_pre_config
    )

    [user_sub_characteristic, sub_characteristic_weights] = define_subcharacteristics(
        user_characteristics, available_pre_config
    )

    [user_measures, measures_weights] = define_measures(
        user_sub_characteristic, available_pre_config
    )

    pass


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
    parser_create = subparsers.add_parser(
        "create", help="Create a new model pre configuration"
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


def main():
    """Entry point for the application script"""

    signal.signal(signal.SIGINT, sigint_handler)

    try:
        setup()
    except KeyboardInterrupt:
        print("\nYou pressed Ctrl + C! No pre conf created.")
