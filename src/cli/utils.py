import logging
import re
from datetime import datetime

from rich import box, print
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.table import Table
from rich.text import Text

from src.cli.exceptions import exceptions

logger = logging.getLogger("msgram")
console = Console(highlight=False, soft_wrap=False, width=140)

DATE_PATTERN = r"^\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4}$"


def is_valid_date_range(date):
    match = re.match(DATE_PATTERN, date)
    if not match:
        return False

    d1, m1, y1, d2, m2, y2 = [int(time) for time in re.split(r"[/\-]", date)]

    try:
        since = datetime(y1, m1, d1)
        until = datetime(y2, m2, d2)
    except ValueError:
        return False

    return since <= until


def print_info(text: str):
    """Print an info message."""
    console.print(text, style="green")


def print_warn(text: str):
    """Print a warning message."""
    console.print(text, style="yellow")


def print_error(text: str):
    """Print a error message."""
    console.print(text, style="red")


def print_table(the_dict: dict, table_name: str = "", field: str = ""):
    table = Table(
        title=table_name,
        title_style="bold",
        row_styles=["none", "dim"],
        border_style="bright_yellow",
        pad_edge=False,
        box=box.MINIMAL,
    )

    table.add_column(
        field,
        no_wrap=True,
        header_style="bold cyan",
        footer_style="bright_cian",
        style="cyan",
    )

    table.add_column(
        "values",
        no_wrap=True,
        header_style="bold red",
        footer_style="bright_red",
        style="red",
    )

    for field, value in the_dict.items():
        table.add_row(str(field), str(value))

    console.print(table)


def make_progress_bar() -> Progress:
    progress_bar = Progress(
        TextColumn("{task.description}"),
        TextColumn("[bold bright_red]Waiting  "),
        BarColumn(complete_style="red"),
        TaskProgressColumn(),
        refresh_per_second=10,
        transient=True,
    )
    return progress_bar


def print_rule(title: str = "", text: str = "", style: str = "#4682B4"):
    if title:
        console.rule(f"{title}", style=style)
    else:
        console.rule(style=style)
    if text:
        console.print(text, style="grey58")

    console.line()


def print_panel(menssage: str, title: str = "Next steps"):
    console.line(2)
    print(
        Panel(
            menssage,
            title=title,
            title_align="center",
            style="#4F4F4F",
            border_style="#A9A9A9",
            padding=(1, 2),
            width=140,
        ),
    )


def print_diff_table(the_dict: dict, table_name: str = "", field: str = ""):
    table = Table(
        title=table_name,
        title_style="bold",
        row_styles=["none"],
        border_style="bright_yellow",
        pad_edge=False,
        box=box.MINIMAL,
    )

    table.add_column(
        field,
        no_wrap=True,
        header_style="bold cyan",
        footer_style="bright_cian",
    )

    table.add_column(
        "Planned",
        no_wrap=True,
        header_style="bold cyan",
        footer_style="bright_cian",
    )

    table.add_column(
        "Developed",
        no_wrap=True,
        header_style="bold cyan",
        footer_style="bright_cian",
    )

    table.add_column(
        "Diff",
        no_wrap=True,
        header_style="bold cyan",
        footer_style="bright_cian",
    )

    for field, value in the_dict.items():
        row_style = format_diff_color(value)
        table.add_row(
            Text(str(field), style=row_style),
            Text(str(value["planned"]), style=row_style),
            Text(str(value["developed"]), style=row_style),
            Text(str(value["diff"]), style=row_style),
        )

    console.print(table)


def format_diff_color(value):
    if value["planned"] - value["developed"] < 0:
        return "green"
    elif value["planned"] - value["developed"] > 0:
        return "red"
    else:
        return "white"


def validate_json_values(file, file_path):
    for value in file:
        try:
            if value > 1 or value < 0:
                raise exceptions.MeasureSoftGramCLIException(
                    f"[red]The values informed in the .json file {file_path} must be between 0 and 1.\n"
                )
        except exceptions.MeasureSoftGramCLIException as e:
            print_error(f"[red]Failed to decode the JSON file: {e}\n")
            print_rule()
            exit(1)
        except TypeError:
            print_error(
                f"[red]Failed to decode the JSON file: The values informed in the .json"
                f"file {file_path} must be between 0 and 1.\n"
            )
            print_rule()
            exit(1)
