import argparse
import sys
from measuresoftgram.jsonReader import fileReader


def parse_import():
    print("Importing metrics")
    userPath = input("Please provide sonar json absolute file path: ")
    metrics = fileReader(r'{}'.format(userPath))   


def parse_create():
    print("Creating a new pre conf")
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


def parse_import():
    print("Importing metrics")
    pass


def parse_create():
    print("Creating a new pre conf")
    pass


def main():
    """Entry point for the application script"""

    setup()

   
if __name__=="__main__":
    main()
