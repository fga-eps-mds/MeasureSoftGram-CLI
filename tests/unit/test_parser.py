from pathlib import Path
from src.cli.commands.cmd_init import command_init
from src.cli.commands.cmd_extract import command_extract
from src.cli.commands.cmd_calculate import command_calculate
from src.cli.commands.cmd_list import command_list

from src.cli.parsers import create_parser


def mock_command_init(args):
    return f"Mocked command_init with args: {args}"


def mock_command_extract(args):
    return f"Mocked command_extract with args: {args}"


def mock_command_calculate(args):
    return f"Mocked command_calculate with args: {args}"


def mock_command_list(args):
    return f"Mocked command_list with args: {args}"


def test_parser_init():
    parser = create_parser()
    args = parser.parse_args(["init", "-cp", "/path/to/config"])
    assert args.func == command_init
    assert args.config_path == Path("/path/to/config")


def test_parser_list():
    parser = create_parser()
    args = parser.parse_args(["list", "-cp", "/path/to/config"])
    assert args.func == command_list
    assert args.config_path == Path("/path/to/config")


def test_parser_extract():
    parser = create_parser()

    args = parser.parse_args(
        [
            "extract",
            "-sp",
            "/path/to/data",
            "-ep",
            "/path/to/extracted",
            "-gr",
            "/path/to/repo",
        ]
    )
    assert args.func == command_extract
    assert args.sonar_path == Path("/path/to/data")
    assert args.extracted_path == Path("/path/to/extracted")
    assert args.gh_repository == "/path/to/repo"


def test_parser_calculate():
    parser = create_parser()
    args = parser.parse_args(
        [
            "calculate",
            "-ep",
            "/path/to/extracted",
            "-cp",
            "/path/to/config",
            "-o",
            "csv",
        ]
    )
    assert args.func == command_calculate
    assert args.extracted_path == Path("/path/to/extracted")
    assert args.config_path == Path("/path/to/config")
    assert args.output_format == "csv"
