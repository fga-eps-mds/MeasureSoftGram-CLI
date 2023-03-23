import logging

from rich import box, print
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.table import Table

logger = logging.getLogger("msgram")
console = Console(highlight=False, soft_wrap=False, width=140)


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
