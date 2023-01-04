import os
from dotenv import load_dotenv
import logging

from src.cli.parsers import create_parser

from src.config.setup_log import config_logger

logger = logging.getLogger("msgram")


def run_cli():
    parser = create_parser()
    raw_args = parser.parse_args()
    command = getattr(raw_args, "command", "help")

    logger.debug(f"cmd  : {command}")
    logger.debug(f"rargs: {raw_args}")

    if not command:
        logger.critical(f"cmd < {command} > not implemented!")
        parser.print_help()
        return

    cmd_func, args = parse_args(raw_args)

    cmd_func(args)  # type: ignore


def parse_args(raw_args):
    func = getattr(raw_args, "func", "help")

    args = vars(raw_args)
    del args["command"]
    del args["func"]

    logger.debug(f"args : {args}")
    logger.debug(f"func : {func}")
    return func, args


def main():
    """Main entry point for MSGram CLI."""

    load_dotenv()
    log_mod = os.getenv("LOG")
    config_logger(log_mod)

    logger.info("Starting MSGram CLI app")
    run_cli()
    logger.info("Done MSGram CLI app")
