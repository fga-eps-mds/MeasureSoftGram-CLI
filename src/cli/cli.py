import os
import sys
from dotenv import load_dotenv
import logging

from src.cli.parsers import create_parser
from src.cli.utils import configure_theme

from src.config.setup_log import config_logger

logger = logging.getLogger("msgram")


def get_theme_from_namespace(raw_args):
    return getattr(raw_args, "command_theme", None) or getattr(
        raw_args, "theme", "auto"
    )


def get_theme_from_argv(argv):
    theme = "auto"
    for index, arg in enumerate(argv):
        if arg == "--theme" and index + 1 < len(argv):
            theme = argv[index + 1]
        elif arg.startswith("--theme="):
            theme = arg.split("=", 1)[1]
    return theme


def run_cli():
    configure_theme(get_theme_from_argv(sys.argv))
    parser = create_parser()
    raw_args = parser.parse_args()
    configure_theme(get_theme_from_namespace(raw_args))
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
    args.pop("theme", None)
    args.pop("command_theme", None)

    logger.debug(f"args : {args}")
    logger.debug(f"func : {func}")
    return func, args


def main():
    """Main entry point for MSGram CLI."""

    load_dotenv()
    log_mod = os.getenv("LOG")
    config_logger(log_mod)
    configure_theme(get_theme_from_argv(sys.argv))

    logger.info("Starting MSGram CLI app")
    run_cli()
    logger.info("Done MSGram CLI app")
