import argparse
import os
import signal
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.cli.commands import command_init, command_extract, parse_get_entity, parse_import, parse_init
from src.cli.commands.parse_calculate.parse_calculate import parse_calculate
from src.cli.commands.parse_generate.parse_generate import parse_generate

from src.config.settings import (
    AVAILABLE_ENTITIES,
    AVAILABLE_GEN_FORMATS,
    AVAILABLE_IMPORTS,
    SUPPORTED_FORMATS,
)


def sigint_handler(*_):
    print("\n\nExiting MeasureSoftGram...")
    sys.exit(0)


def setup():
    parser = argparse.ArgumentParser(
        description="Command line interface for measuresoftgram"
    )
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    # =====================================< COMMAND init >=====================================
    parser_initialize = subparsers.add_parser(
        "initialize",
        help="Create a init file `.measuresoftgram` with your default organization, product and repositories",
    )

    parser_initialize.add_argument(
        "--dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent.parent.parent / ".msgram",
        help="Path to the directory",
    )

    parser_init = subparsers.add_parser(
        "init",
        help="Create a init file `.measuresoftgram` with your default organization, product and repositories",
    )

    parser_init.add_argument(
        "file_path",
        type=lambda p: Path(p).absolute(),
        help="Path to your configured JSON file with the organization, product and repositories names",
    )

    parser_init.add_argument(
        "--host",
        type=str,
        nargs="?",
        default=os.getenv("MSG_SERVICE_HOST"),
        help=("The host of the service."),
    )

    parser_extract = subparsers.add_parser(
        "extract",
        help="Extract supported metrics"
    )

    parser_extract.add_argument(
        "output_origin",
        type=str,
        choices=(AVAILABLE_IMPORTS),
        help=(
            "Import a metrics files from some origin. Valid values are: "
            + ", ".join(AVAILABLE_IMPORTS)
        ),
    )

    parser_extract.add_argument(
        "config_dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent.parent.parent / ".msgram",
        help="Path to the directory",
    )

    parser_extract.add_argument(
        "dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the directory",
    )

    parser_extract.add_argument(
        "language_extension",
        type=str,
        help="The source code language extension",
    )

    # =============================< IMPORT PARSER CODE >=============================

    parser_import = subparsers.add_parser(
        "import",
        help="Import a folder with metrics",
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
        nargs="?",
        default=os.getenv("MSG_SERVICE_HOST"),
        help="The host of the service",
    )

    parser_get_entity = subparsers.add_parser(
        "get",
        help="Gets the last record of a specific entity",
    )

    parser_get_entity.add_argument(
        "entity",
        type=str,
        choices=(AVAILABLE_ENTITIES),
        help=("The entity to get. Valid values are: " + ", ".join(AVAILABLE_ENTITIES)),
    )

    parser_get_entity.add_argument(
        "entity_id",
        type=int,
        nargs="?",
        help=(
            "The ID of the entity to get. If not provided, a list with the last record of all available entities will "
            "be returned."
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
        nargs="?",
        default=os.getenv("MSG_SERVICE_HOST"),
        help="The host of the service",
    )

    parser_get_entity.add_argument(
        "--output_format",
        type=str,
        nargs="?",
        default="tabular",
        help=(
            "The format of the output. "
            + "Valid values are: "
            + ", ".join(SUPPORTED_FORMATS)
        ),
    )

    parser_get_entity.add_argument(
        "--organization_id",
        type=str,
        nargs="?",
        default=os.getenv("MSG_ORGANIZATION_ID"),
        help="The ID of the organization that the repository belongs to",
    )

    parser_get_entity.add_argument(
        "--repository_id",
        type=str,
        nargs="?",
        default=os.getenv("MSG_REPOSITORY_ID"),
        help="The ID of the repository",
    )

    parser_get_entity.add_argument(
        "--product_id",
        type=str,
        nargs="?",
        default=os.getenv("MSG_PRODUCT_ID"),
        help="The ID of the product",
    )

    # =============================< GENERATE PARSER CODE >=============================

    parser_generate = subparsers.add_parser(
        "generate",
        help="Generate an output file, according to the specified type, for the historical values for a given product",
    )

    parser_generate.add_argument(
        "format",
        type=str,
        choices=AVAILABLE_GEN_FORMATS,
        help=(
            "The possible formats to generate an output file. Valid values are: "
            + ", ".join(AVAILABLE_GEN_FORMATS)
        ),
    )

    parser_generate.add_argument(
        "--host",
        type=str,
        nargs="?",
        default=os.getenv("MSG_SERVICE_HOST"),
        help="The host of the service",
    )

    parser_calculate_entity = subparsers.add_parser(
        "calculate", help="Calculates all entities"
    )

    parser_calculate_entity.add_argument(
        "all",
        type=str,
        nargs="?",
        help=(
            "Returns the calculated value of the entities: measures, subcharacteristics, characteristics, sqc"
        ),
    )
    parser_calculate_entity.add_argument(
        "--host",
        type=str,
        nargs="?",
        default=os.getenv("MSG_SERVICE_HOST"),
        help="The service host",
    )

    parser_calculate_entity.add_argument(
        "--organization_id",
        type=str,
        nargs="?",
        default=os.getenv("MSG_ORGANIZATION_ID"),
        help="The specific ID of the organization to which the repository belongs",
    )

    parser_calculate_entity.add_argument(
        "--repository_id",
        type=str,
        nargs="?",
        default=os.getenv("MSG_REPOSITORY_ID"),
        help="The repository ID",
    )

    parser_calculate_entity.add_argument(
        "--product_id",
        type=str,
        nargs="?",
        default=os.getenv("MSG_PRODUCT_ID"),
        help="The product ID",
    )

    parser_calculate_entity.add_argument(
        "--output_format",
        type=str,
        nargs="?",
        default="tabular",
        help=("The format of the output values are: ".join(SUPPORTED_FORMATS)),
    )

    # =============================< Arguments parsing methods >=============================

    args = parser.parse_args()

    # if args is empty show help
    if not sys.argv[1:]:
        parser.print_help()
        return

    elif args.command == "initialize":
        command_init(vars(args))

    elif args.command == "extract":
        command_extract(vars(args))

    elif args.command == "import":
        parse_import(
            args.output_origin,
            args.dir_path,
            args.language_extension,
            args.host,
        )

    elif args.command == "init":
        parse_init(
            args.file_path,
            args.host,
        )

    elif args.command == "get":
        parse_get_entity(
            args.entity,
            args.entity_id,
            args.host,
            args.organization_id,
            args.repository_id,
            args.product_id,
            args.output_format,
            args.history,
        )

    elif args.command == "generate":
        parse_generate(args.format, args.host)

    elif args.command == "calculate":
        parse_calculate(
            args.host,
            args.organization_id,
            args.repository_id,
            args.product_id,
            args.output_format,
        )


def main():
    """Entry point for the application script"""

    load_dotenv()
    signal.signal(signal.SIGINT, sigint_handler)

    setup()
