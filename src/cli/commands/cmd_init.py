import logging
import sys
import json
from pathlib import Path
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Confirm

from staticfiles import DEFAULT_PRE_CONFIG
from src.config.settings import FILE_CONFIG

logger = logging.getLogger("msgram")


def command_init(args):
    try:
        config_path: Path = args["config_path"]

    except Exception as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        sys.exit(1)

    logger.debug(config_path)
    console = Console()
    file_path = config_path / FILE_CONFIG

    console.clear()
    console.rule(title="MSGram", style="#4682B4")
    print("[#708090]Init to set config file[/]:")
    console.line(1)

    if not config_path.exists():
        print(f"create dir: {config_path}")
        config_path.mkdir()

    replace = True

    if file_path.exists():
        print(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")
        replace = Confirm.ask(f"> Do you want to replace [bold blue]'{FILE_CONFIG}'[/]?")

    if replace:
        try:
            with file_path.open("w") as f:
                f.write(json.dumps(DEFAULT_PRE_CONFIG, indent=4))

        except OSError:
            console.line(2)
            print("[bold red]Error opening or writing to file[/]")

        console.print(
            f"The file config: '{config_path.name}/msgram.json' was created successfully.",
            style="green",
        )

    else:
        console.print(
            f"The file config: '{config_path.name}/msgram.json' not changed...",
            style="green",
        )

    console.line(2)
    print(
        Panel(
            "> [#008080]Run msgram extract -o sonarqube -dp data_path[/], to extract suported metrics!",
            title="Next steps",
            title_align="center",
            style="#4F4F4F",
            border_style="#A9A9A9",
            padding=(1, 2),
        ),
    )
