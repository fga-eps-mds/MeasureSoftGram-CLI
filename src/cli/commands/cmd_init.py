import json
import logging
import sys
from pathlib import Path

from rich.prompt import Confirm
from staticfiles import DEFAULT_PRE_CONFIG

from src.cli.utils import (
    clear_console,
    console,
    print_error,
    print_panel,
    print_rule,
    print_success,
    print_warn,
)
from src.config.settings import FILE_CONFIG

logger = logging.getLogger("msgram")


def command_init(args):
    try:
        config_path: Path = args["config_path"]

    except Exception as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        sys.exit(1)

    logger.debug(config_path)
    file_path = config_path / FILE_CONFIG

    clear_console()
    print_rule("MSGram", "Init to set config file:")

    if not config_path.exists():
        print_success(f"Created dir: {config_path}")
        config_path.mkdir()

    replace = True

    if file_path.exists():
        print_warn(f"MSGram config file '{FILE_CONFIG}' exists already!")
        replace = Confirm.ask(
            f"> Do you want to replace '{FILE_CONFIG}'?",
            console=console,
        )

    if replace:
        try:
            with file_path.open("w") as f:
                f.write(json.dumps(DEFAULT_PRE_CONFIG, indent=4))
        except OSError:
            console.line(2)
            print_error("Error opening or writing to file")
        print_success(
            f"The file config: '{config_path.name}/msgram.json' was created successfully."
        )

    else:
        print_warn(f"The file config: '{config_path.name}/msgram.json' not changed...")

    print_panel(
        "> Run msgram extract -o <source of information> -dp data_path -ep extract_path,\n"
        "  to extract supported metrics!"
    )
