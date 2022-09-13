import os
import argparse
import sys
import signal
from pathlib import Path

from src.cli.commands import parse_import, parse_get_entity

from src.config.settings import AVAILABLE_ENTITIES, AVAILABLE_IMPORTS, SUPPORTED_FORMATS


def sigint_handler(*_):
    print("\n\nExiting MeasureSoftGram...")
    sys.exit(0)


def setup():
    parser = argparse.ArgumentParser(
        description="Command line interface for measuresoftgram"
    )

    argparse.ArgumentTypeError('invalid value!!!')

    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    parser_import = subparsers.add_parser(
        "import",
        help="Import a folder with metrics"
    )

    parser_import.add_argument(
        "output_origin",
        type=str,
        choices=(AVAILABLE_IMPORTS),
        help=(
            "Import a metrics files from some origin. Valid values are: "
            + ", ".join(AVAILABLE_IMPORTS)
        ),
    )

    parser_import.add_argument(
        "dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the directory",
    )

    parser_import.add_argument(
        "language_extension",
        type=str,
        help="The source code language extension",
    )

    parser_import.add_argument(
        "--host",
        type=str,
        nargs='?',
        default=os.getenv(
            "MSG_SERVICE_HOST",
            "https://measuresoftgram-service.herokuapp.com/"
        ),
        help="The host of the service",
    )

    parser_import.add_argument(
        "--organization_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_ORGANIZATION_ID", "1"),
        help="The ID of the organization that the repository belongs to",
    )

    parser_import.add_argument(
        "--repository_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_REPOSITORY_ID", "6"),
        help="The ID of the repository",
    )

    parser_import.add_argument(
        "--product_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_PRODUCT_ID", "3"),
        help="The ID of the product",
    )

    parser_get_entity = subparsers.add_parser(
        "get",
        help="Gets the last record of a specific entity",
    )

    parser_get_entity.add_argument(
        "entity",
        type=str,
        choices=(AVAILABLE_ENTITIES),
        help=(
            "The entity to get. Valid values are: "
            + ", ".join(AVAILABLE_ENTITIES)
        ),
    )

    parser_get_entity.add_argument(
        "entity_id",
        type=int,
        nargs='?',
        help=(
            "The ID of the entity to get. If not provided, a list with the "
            "last record of all available entities will be returned."
        ),
    )

    parser_get_entity.add_argument(
        "--history",
        action="store_true",
        default=False,
        help="The history of the repository",
    )

    parser_get_entity.add_argument(
        "--host",
        type=str,
        nargs='?',
        default="https://measuresoftgram-service.herokuapp.com/",
        help="The host of the service",
    )

    parser_get_entity.add_argument(
        "--output_format",
        type=str,
        nargs='?',
        default="tabular",
        help=(
            "The format of the output. "
            "Valid values are: " + ", ".join(SUPPORTED_FORMATS)
        ),
    )

    parser_get_entity.add_argument(
        "--organization_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_ORGANIZATION_ID", "1"),
        help="The ID of the organization that the repository belongs to",
    )

    parser_get_entity.add_argument(
        "--repository_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_REPOSITORY_ID", "6"),
        help="The ID of the repository",
    )

    parser_get_entity.add_argument(
        "--product_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_PRODUCT_ID", "3"),
        help="The ID of the product",
    )

    # parser_create = subparsers.add_parser(
    #     "create",
    #     help="Create a new model pre configuration from a JSON file",
    # )

    # subparsers.add_parser(
    #     "available",
    #     help="Shows all characteristics, sub-characteristics and measures available in measuresoftgram",
    # )

    # parser_create.add_argument(
    #     "path",
    #     type=lambda p: Path(p).absolute(),
    #     default=Path(__file__).absolute().parent / "data",
    #     help="Path to the JSON file",
    # )

    # parser_analysis = subparsers.add_parser("analysis", help="Get analysis result")
    # parser_analysis.add_argument(
    #     "id",
    # )
    # subparsers.add_parser("list", help="List all pre configurations")

    # parser_show = subparsers.add_parser(
    #     "show", help="Show all information of a pre configuration"
    # )

    # parser_show.add_argument(
    #     "pre_config_id",
    #     type=str,
    #     help="Pre config ID",
    # )

    # change_name = subparsers.add_parser(
    #     "change-name", help="Change pre configuration name"
    # )

    # change_name.add_argument(
    #     "pre_config_id",
    #     type=str,
    #     help="Pre config ID",
    # )

    # change_name.add_argument(
    #     "new_name",
    #     type=str,
    #     help="New pre configuration name",
    # )

    args = parser.parse_args()

    # if args is empty show help
    if not sys.argv[1:]:
        parser.print_help()
        return

    elif args.command == "import":
        parse_import(
            args.output_origin,
            args.dir_path,
            args.language_extension,
            args.host,
            args.organization_id,
            args.repository_id,
            args.product_id,
        )

    # elif args.command == "create":
    #     parse_create(args.path)

    # elif args.command == "analysis":
    #     parse_analysis(args.id)

    # elif args.command == "available":
    #     parse_available()

    # elif args.command == "list":
    #     parse_list()

    # elif args.command == "show":
    #     parse_show(args.pre_config_id)

    # elif args.command == "change-name":
    #     parse_change_name(args.pre_config_id, args.new_name)

    elif args.command == 'get':
        parse_get_entity(
            args.entity,
            args.entity_id,
            args.host,
            args.organization_id,
            args.repository_id,
            args.product_id,
            args.output_format,
            args.history
        )


def main():
    """Entry point for the application script"""

    signal.signal(signal.SIGINT, sigint_handler)

    setup()
