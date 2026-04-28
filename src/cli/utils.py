import logging
import os
import re
from datetime import datetime

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.table import Table
from rich.text import Text

from src.cli.exceptions import exceptions

logger = logging.getLogger("msgram")
console = Console(highlight=False, soft_wrap=False)

DATE_PATTERN = r"^\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4}$"
THEME_CHOICES = ("auto", "dark", "light")
_selected_theme = "auto"

_THEME_STYLES = {
    "dark": {
        "main": "#E6E6E6",
        "muted": "#A9A9A9",
        "success": "#00C853",
        "warning": "#FFD54F",
        "error": "#FF5252",
        "accent": "#64B5F6",
        "border": "#90A4AE",
    },
    "light": {
        "main": "#202124",
        "muted": "#5F6368",
        "success": "#0B6B2B",
        "warning": "#8A5A00",
        "error": "#B00020",
        "accent": "#005F73",
        "border": "#5F6368",
    },
}

_AUTO_STYLES = {
    "main": None,
    "muted": None,
    "success": "green",
    "warning": "yellow",
    "error": "red",
    "accent": "cyan",
    "border": "bright_black",
}

ASCII_BOX = getattr(box, "ASCII", box.SIMPLE)


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


def configure_theme(theme: str = "auto"):
    """Configure CLI contrast for subsequent terminal output."""
    global _selected_theme
    _selected_theme = theme if theme in THEME_CHOICES else "auto"


def _detect_terminal_theme():
    colorfgbg = os.getenv("COLORFGBG")
    if not colorfgbg:
        return None

    try:
        background = int(colorfgbg.split(";")[-1])
    except ValueError:
        return None

    if background in {0, 1, 2, 3, 4, 5, 6, 8}:
        return "dark"
    if background in {7, 9, 10, 11, 12, 13, 14, 15}:
        return "light"

    return None


def _active_theme():
    if _selected_theme != "auto":
        return _selected_theme
    return _detect_terminal_theme() or "dark"


def _style(name: str):
    theme = _active_theme()
    if theme:
        return _THEME_STYLES[theme][name]
    return _AUTO_STYLES[name]


def _bold_style(name: str):
    color = _style(name)
    return f"bold {color}" if color else "bold"


def color_tag(name: str):
    color = _style(name)
    return f"[{color}]" if color and color.startswith("#") else ""


def clear_console():
    console.clear()


def print_output(text, style_name: str = "main"):
    console.print(text, style=_style(style_name))


def print_info(text):
    """Print a regular CLI message using the active contrast."""
    print_output(text, "main")


def print_success(text):
    """Print a success message."""
    print_output(text, "success")


def print_warn(text: str):
    """Print a warning message."""
    print_output(text, "warning")


def print_error(text: str):
    """Print an error message."""
    print_output(text, "error")


def print_status(label: str, value: str, status: str = "success"):
    text = Text()
    text.append(label, style=_style(status))
    text.append(" ")
    text.append(str(value), style=_style("main"))
    console.print(text)


def print_table(the_dict: dict, table_name: str = "", field: str = ""):
    table = Table(
        title=table_name or None,
        title_style=_bold_style("main"),
        border_style=_style("border"),
        pad_edge=True,
        padding=(0, 1),
        box=ASCII_BOX,
        safe_box=True,
    )

    table.add_column(
        field,
        no_wrap=False,
        overflow="fold",
        header_style=_bold_style("accent"),
        style=_style("main"),
    )

    table.add_column(
        "values",
        no_wrap=False,
        overflow="fold",
        header_style=_bold_style("accent"),
        style=_style("main"),
    )

    for field, value in the_dict.items():
        table.add_row(str(field), str(value))

    console.print(table)


def make_progress_bar() -> Progress:
    progress_bar = Progress(
        TextColumn("{task.description}"),
        TextColumn("Waiting  ", style=_bold_style("error")),
        BarColumn(complete_style=_style("error")),
        TaskProgressColumn(),
        refresh_per_second=10,
        transient=True,
    )
    return progress_bar


def print_rule(title: str = "", text: str = "", style: str = ""):
    rule_style = style or _style("accent")
    if title:
        console.rule(f"{title}", style=rule_style)
    else:
        console.rule(style=rule_style)
    if text:
        console.print(text, style=_style("muted"))

    console.line()


def print_panel(menssage: str, title: str = "Next steps"):
    console.line(2)
    console.print(
        Panel(
            menssage,
            title=title,
            title_align="center",
            style=_style("main"),
            border_style=_style("border"),
            padding=(1, 2),
            width=min(console.width, 140),
        ),
    )


def print_diff_table(the_dict: dict, table_name: str = "", field: str = ""):
    table = Table(
        title=table_name or None,
        title_style=_bold_style("main"),
        border_style=_style("border"),
        pad_edge=True,
        padding=(0, 1),
        box=ASCII_BOX,
        safe_box=True,
    )

    table.add_column(
        field,
        no_wrap=False,
        overflow="fold",
        header_style=_bold_style("accent"),
        style=_style("main"),
    )

    table.add_column(
        "Planned",
        no_wrap=False,
        overflow="fold",
        header_style=_bold_style("accent"),
        style=_style("main"),
    )

    table.add_column(
        "Developed",
        no_wrap=False,
        overflow="fold",
        header_style=_bold_style("accent"),
        style=_style("main"),
    )

    table.add_column(
        "Diff",
        no_wrap=False,
        overflow="fold",
        header_style=_bold_style("accent"),
        style=_style("main"),
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
        return _style("success")
    elif value["planned"] - value["developed"] > 0:
        return _style("error")
    else:
        return _style("main")


def validate_json_values(file, file_path):
    for value in file:
        try:
            if value > 1 or value < 0:
                raise exceptions.MeasureSoftGramCLIException(
                    f"The values informed in the .json file {file_path} must be between 0 and 1.\n"
                )
        except exceptions.MeasureSoftGramCLIException as e:
            print_error(f"Failed to decode the JSON file: {e}\n")
            print_rule()
            exit(1)
        except TypeError:
            print_error(
                f"Failed to decode the JSON file: The values informed in the .json"
                f"file {file_path} must be between 0 and 1.\n"
            )
            print_rule()
            exit(1)
