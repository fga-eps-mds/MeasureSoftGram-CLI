import argparse

from pathlib import Path

from src.cli.commands.cmd_diff import command_diff
from src.cli.commands.cmd_init import command_init
from src.cli.commands.cmd_extract import command_extract
from src.cli.commands.cmd_calculate import command_calculate
from src.cli.commands.cmd_list import command_list
from src.cli.commands.cmd_norm_diff import command_norm_diff

from src.config.settings import (
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
        help="Path to the directory with the model configuration file (msgram.json).",
    )
    parser_init.set_defaults(func=command_init)  # function command init

    # =====================================< COMMAND list >=====================================
    parser_list_config = subparsers.add_parser(
        "list",
        help="Listing configurations parameters.",
    )

    parser_list_config.add_argument(
        "-cp",
        "--config_path",
        type=lambda p: Path(p).absolute(),
        default=DEFAULT_CONFIG_PATH,
        help="Path to the directory with the model configuration file (msgram.json).",
    )

    parser_list_config.add_argument(
        "all",
        nargs="?",
        help="Show configuration file.",
    )

    parser_list_config.set_defaults(func=command_list)  # function command list config

    # =====================================< COMMAND extract >=====================================
    parser_extract = subparsers.add_parser("extract", help="Extract supported metrics")

    parser_extract.add_argument(
        "-sp",
        "--sonar_path",
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
        "-gl",
        "--gh_label",
        type=str,
        help=(
            "Selected label name to be considered in the Story Issues extraction."
            + ' Format "XX YY", including quotation marks.'
            + ' Default, not case sensitive: "US", "User Story" or "User Stories".'
        ),
    )

    parser_extract.add_argument(
        "-gw",
        "--gh_workflows",
        type=str,
        help="Selected workflow name to be considered in the CI Feedback Time extraction."
        + ' Format "XX YY", including quotation marks.'
        + ' Default, not case sensitive: "build".',
    )

    parser_extract.add_argument(
        "-gd",
        "--gh_date_range",
        type=str,
        help=(
            'Filter range of dates considered on extraction, with format "dd/mm/yyyy-dd/mm/yyyy"'
            + ", including quotation marks."
        ),
    )

    parser_extract.add_argument(
        "-gr",
        "--gh_repository",
        type=str,
        help="Path to analysis git repository",
    )

    parser_extract.add_argument(
        "-p1",
        "--pe_release_1",
        type=lambda p: Path(p).absolute(),
        help="Path to the .csv file of the first release, used for extracting performance efficiency data",
    )

    parser_extract.add_argument(
        "-p2",
        "--pe_release_2",
        type=lambda p: Path(p).absolute(),
        help="Path to the .csv file of the second release, used for extracting performance efficiency data",
    )

    parser_extract.add_argument(
        "-pn",
        "--pe_repository_name",
        type=str,
        help="Name of the repository associated with the extracted performance efficiency data",
    )

    parser_extract.set_defaults(func=command_extract)  # function command extract

    # =====================================< COMMAND calculate >=====================================
    parser_calculate = subparsers.add_parser(
        "calculate",
        help="Calculates all entities",
    )

    # parser_calculate.add_argument(
    #     "all",
    #     type=str,
    #     nargs="?",
    #     help=(
    #         "Returns the calculated value of the entities: measures, subcharacteristics, characteristics, tsqmi"
    #     ),
    # )

    parser_calculate.add_argument(
        "-ep",
        "--extracted_path",
        type=lambda p: Path(p).absolute(),
        default=DEFAULT_CONFIG_PATH,
        help="Path to the extracted directory",
    )

    parser_calculate.add_argument(
        "-cp",
        "--config_path",
        type=lambda p: Path(p).absolute(),
        default=DEFAULT_CONFIG_PATH,
        help="Path to the directory with the model configuration file (msgram.json).",
    )

    parser_calculate.add_argument(
        "-o",
        "--output_format",
        type=str,
        choices=AVAILABLE_GEN_FORMATS,
        default="csv",
        help=(
            "The format of the output (export) values are: "
            + ", ".join(SUPPORTED_FORMATS)
        ),
    )
    parser_calculate.set_defaults(func=command_calculate)  # function command calculate

    # =====================================< COMMAND norm_diff >=====================================
    parser_norm_diff = subparsers.add_parser(
        "norm_diff",
        help="Calculates the Frobenius norm of the difference between tensors RP and RD, which means the quantitative "
        "perception of the discrepancy between the planned and developed quality requirements in a release.",
    )

    parser_norm_diff.add_argument(
        "-rp",
        "--rp_path",
        type=lambda p: Path(p).absolute(),
        help="path to the .json file with the planned/wished values ​​for the quality "
        "characteristics of a release. quality requirements goals for a release.",
    )

    parser_norm_diff.add_argument(
        "-rd",
        "--rd_path",
        type=lambda p: Path(p).absolute(),
        help="path to the .json file with the model-calculated values ​​for a release's "
        "quality characteristics observed/developed.",
    )

    parser_norm_diff.set_defaults(
        func=command_norm_diff
    )  # function command list config

    # =====================================< COMMAND diff >=====================================
    parser_calculate = subparsers.add_parser(
        "diff",
        help="Calculates and interprets the difference between the planned and developed quantitative perceptions "
        "of each quality characteristic, represented by the RP and RD tensors.",
    )

    parser_calculate.add_argument(
        "-rd",
        "--rd_path",
        type=lambda p: Path(p).absolute(),
        help="Path to the .json file with the model-calculated values for a release's quality"
        "characteristics observed/developed.",
    )

    parser_calculate.add_argument(
        "-rp",
        "--rp_path",
        type=lambda p: Path(p).absolute(),
        help="Path to the .json file with the planned/wished values for the quality characteristics"
        "of a release. Quality requirements goals for a release.",
    )

    parser_calculate.add_argument(
        "-of",
        "--output_format",
        type=str,
        choices=AVAILABLE_GEN_FORMATS,
        help=("The format of the output (export) values is tabular"),
    )
    parser_calculate.set_defaults(func=command_diff)

    return parser
