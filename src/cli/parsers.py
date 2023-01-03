import argparse
import os

from pathlib import Path

from src.cli.commands import command_import, command_init, command_extract
from src.config.settings import AVAILABLE_IMPORTS


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
        "--dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent.parent.parent / ".msgram",
        help="Path to the directory",
    )
    parser_init.set_defaults(func=command_init)  # function command init

    # =====================================< COMMAND extract >=====================================
    parser_extract = subparsers.add_parser("extract", help="Extract supported metrics")

    parser_extract.add_argument(
        "--output_origin",
        type=str,
        choices=(AVAILABLE_IMPORTS),
        help=(
            "Import a metrics files from some origin. Valid values are: "
            + ", ".join(AVAILABLE_IMPORTS)
        ),
    )

    parser_extract.add_argument(
        "--config_dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent.parent.parent / ".msgram",
        help="Path to the directory",
    )

    parser_extract.add_argument(
        "--dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the directory",
    )

    parser_extract.add_argument(
        "--language_extension",
        type=str,
        help="The source code language extension",
    )
    parser_extract.set_defaults(func=command_extract)  # function command extract

    # =====================================< COMMAND import >=====================================
    parser_import = subparsers.add_parser(
        "import",
        help="Import a folder with metrics",
    )

    parser_import.add_argument(
        "--output_origin",
        type=str,
        choices=(AVAILABLE_IMPORTS),
        help=(
            "Import a metrics files from some origin. Valid values are: "
            + ", ".join(AVAILABLE_IMPORTS)
        ),
    )

    parser_import.add_argument(
        "--dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the directory",
    )

    parser_import.add_argument(
        "--language_extension",
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
    parser_import.set_defaults(func=command_import)  # function command import

    return parser
