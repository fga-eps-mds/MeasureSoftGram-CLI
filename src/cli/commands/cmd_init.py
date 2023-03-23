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


def command_init(args):
    try:
        config_path: Path = args["config_path"]

    except Exception as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        sys.exit(1)

    logger.debug(config_path)
    file_path = config_path / FILE_CONFIG

    console = Console()
    console.clear()
    print_rule("MSGram", "[#708090]Init to set config file[/]:")

    if not config_path.exists():
        print_info(f"Created dir: {config_path}")
        config_path.mkdir()

    replace = True

    if file_path.exists():
        print_info(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")
        replace = Confirm.ask(f"> Do you want to replace [bold blue]'{FILE_CONFIG}'[/]?")

    if replace:
        try:
            with file_path.open("w") as f:
                f.write(json.dumps(DEFAULT_PRE_CONFIG, indent=4))
        except OSError:
            console.line(2)
            print_error("Error opening or writing to file")
        print_info(f"The file config: '{config_path.name}/msgram.json' was created successfully.")

    else:
        print_info(f"The file config: '{config_path.name}/msgram.json' not changed...")

    print_panel(
        "> [#008080]Run msgram extract -o sonarqube -dp data_path -ep extract_path[/], to extract supported metrics!"
    )
