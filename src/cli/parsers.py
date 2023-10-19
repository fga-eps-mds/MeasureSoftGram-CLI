import argparse

from pathlib import Path

from src.cli.commands.cmd_init import command_init
from src.cli.commands.cmd_extract import  command_extract
from src.cli.commands.cmd_calculate import command_calculate
from src.cli.commands.cmd_print_config import command_print_config

from src.config.settings import (
    AVAILABLE_IMPORTS,
    SUPPORTED_FORMATS,
    DEFAULT_CONFIG_PATH,
    AVAILABLE_GEN_FORMATS,
)


def create_parser():
    parser = argparse.ArgumentParser(
        prog="msgram",
        description="Command line interface for measuresoftgram",
        epilog="Thanks for using %(prog)s!",
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="command",
        help="sub-command help",
    )

    # =====================================< COMMAND init >=====================================
    parser_init = subparsers.add_parser(
        "init",
        help="Create a init file `.measuresoftgram` with your default organization, product and repositories",
    )

    parser_init.add_argument(
        "-cp",
        "--config_path",
        type=lambda p: Path(p).absolute(),
        default=DEFAULT_CONFIG_PATH,
        help="Path to default config directory",
    )
    parser_init.set_defaults(func=command_init)  # function command init

    # =====================================< COMMAND print_config >=====================================
    parser_print_config = subparsers.add_parser(
        "print_config",
        help="THIS MESSAGE IS FROM PARSER",
    )

    parser_print_config.add_argument(
        "-hw",
        "--hello_world",
        type=lambda p: Path(p).absolute(),
        default=DEFAULT_CONFIG_PATH,
        help="HELP PARSER",
    )
    parser_print_config.set_defaults(func=command_print_config)  # function command print config

    # =====================================< COMMAND extract >=====================================
    parser_extract = subparsers.add_parser("extract", help="Extract supported metrics")

    parser_extract.add_argument(
        "-o",
        "--output_origin",
        required=True,
        type=str,
        choices=(AVAILABLE_IMPORTS),
        help=(
            "Import a metrics files/repository from some origin. Valid values are: "
            + ", ".join(AVAILABLE_IMPORTS)
        ),
    )

    parser_extract.add_argument(
        "-dp",
        "--data_path",
        type=lambda p: Path(p).absolute(),
        help="Path to analysis data directory",
    )

    parser_extract.add_argument(
        "-ep",
        "--extracted_path",
        type=lambda p: Path(p).absolute(),
        default=DEFAULT_CONFIG_PATH,
        help="Path to the extracted directory",
    )

    parser_extract.add_argument(
        "-le",
        "--language_extension",
        type=str,
        help="The source code language extension",
        default="py",
    )

    parser_extract.add_argument(
        "-rep",
        "--repository_path",
        type=str,
        help="Path to analysis git repository",
    )

    parser_extract.set_defaults(func=command_extract)  # function command extract

    # =====================================< COMMAND calculate >=====================================
    parser_calculate = subparsers.add_parser(
        "calculate",
        help="Calculates all entities",
    )

    parser_calculate.add_argument(
        "all",
        type=str,
        nargs="?",
        help=(
            "Returns the calculated value of the entities: measures, subcharacteristics, characteristics, tsqmi"
        ),
    )

    parser_calculate.add_argument(
        "-ep",
        "--extracted_path",
        type=lambda p: Path(p).absolute(),
        help="Path to the extracted directory",
    )

    parser_calculate.add_argument(
        "-cp",
        "--config_path",
        type=lambda p: Path(p).absolute(),
        default=DEFAULT_CONFIG_PATH,
        help="Path to the config directory",
    )

    parser_calculate.add_argument(
        "-o",
        "--output_format",
        type=str,
        choices=AVAILABLE_GEN_FORMATS,
        default="csv",
        help=("The format of the output (export) values are: ".join(SUPPORTED_FORMATS)),
    )
    parser_calculate.set_defaults(func=command_calculate)  # function command calculate

    return parser
