import json
import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm
from staticfiles import DEFAULT_PRE_CONFIG

from src.cli.utils import print_error, print_info, print_panel, print_rule
from src.config.settings import FILE_CONFIG

logger = logging.getLogger("msgram")


def command_print_config(args):
    # try:
    #     config_path: Path = args["config_path"]

    # except Exception as e:
    #     logger.error(f"KeyError: args[{e}] - non-existent parameters")
    #     print_error(f"KeyError: args[{e}] - non-existent parameters")
    #     sys.exit(1)

    console = Console()
    console.clear()
    print_rule("MSGram", "[#708090] TESTING [/]:")

    print_info(
            f"Command was called!"
        )
