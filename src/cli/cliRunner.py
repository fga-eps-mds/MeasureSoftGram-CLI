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
    # user_path = input("Please provide sonar json absolute file path: ")
    print("Pre Config ID bellow: ")
    print(id)
    print("File path return: ")
    metrics = file_reader(r"{}".format(file_path))
    sorted_metrics = sorted(metrics, key=lambda d: d["metric"])

    payload = {
        "id_wanted": id,
        "comment_lines_density": sorted_metrics[0]["value"],
        "complexity": sorted_metrics[1]["value"],
        "coverage": sorted_metrics[2]["value"],
        "duplicated_lines_density": sorted_metrics[3]["value"],
        "files": sorted_metrics[4]["value"],
        "functions": sorted_metrics[5]["value"],
        "ncloc": sorted_metrics[6]["value"],
        "security_rating": sorted_metrics[7]["value"],
        "test_errors": sorted_metrics[8]["value"],
        "test_execution_time": sorted_metrics[9]["value"],
        "test_failures": sorted_metrics[10]["value"],
        "tests": sorted_metrics[11]["value"],
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
        "--file_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the data directory",
    )
    parser_import.add_argument(
        "--id",
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
        parse_import(args.file_path, args.id)
    elif args.command == "create":
        parse_create()


def main():
    """Entry point for the application script"""

    signal.signal(signal.SIGINT, sigint_handler)

    try:
        setup()
    except KeyboardInterrupt:
        print("\nYou pressed Ctrl + C! No pre conf created.")
