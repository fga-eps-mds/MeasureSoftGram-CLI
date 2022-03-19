import argparse
import sys
from urllib import request
import requests
from measuresoftgram.create import (
    define_characteristic,
    define_subcharacteristics,
    define_measures,
)
from measuresoftgram.jsonReader import file_reader


def parse_import():
    print("Importing metrics")
    user_path = input("Please provide sonar json absolute file path: ")
    file_reader(r'{}'.format(user_path)) 


BASE_URL = "http://localhost:5000/"


def parse_create():
    headers = {"Content-type": "application/json"}
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
    subparsers = parser.add_subparsers(help="sub-command help")
    parser_import = subparsers.add_parser("import", help="Import a metrics file")
    parser_create = subparsers.add_parser(
        "create", help="Create a new model pre configuration"
    )

    parser_import.set_defaults(func=parse_import)
    parser_create.set_defaults(func=parse_create)

    args = parser.parse_args()
    # if args is empty show help
    if not sys.argv[1:]:
        parser.print_help()
        return
    args.func()


def main():
    """Entry point for the application script"""

    setup()

   
if __name__=="__main__":
    main()

