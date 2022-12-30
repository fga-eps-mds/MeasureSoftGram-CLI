import os
from dotenv import load_dotenv
import logging
from src.cli.parsers import create_parser


def run_cli():
    parser = create_parser()
    raw_args = parser.parse_args()
    command = getattr(raw_args, "command", "help")

    if not command:
        parser.print_help()
        return

    cmd_func, args = parse_args(raw_args)

    cmd_func(args)  # type: ignore


def parse_args(raw_args):
    func = getattr(raw_args, "func", "help")

    args = vars(raw_args)
    del args["command"]
    del args["func"]

    return func, args


def main():
    """Main entry point for MSGram CLI."""

    load_dotenv()
    run_cli()
