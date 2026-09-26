import logging
import os
import re
import sys
import subprocess
from datetime import datetime

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from src.cli.exceptions import exceptions

logger = logging.getLogger("msgram")
console = Console(highlight=False, soft_wrap=False)

DATE_PATTERN = r"^\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4}$"
THEME_CHOICES = ("auto", "dark", "light")
_selected_theme = "auto"

_THEME_STYLES = {
    "dark": {
        "main": "bright_white",
        "muted": "white",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
        "accent": "bright_cyan",
        "border": "white",
    },
    "light": {
        "main": "black",
        "muted": "bright_black",
        "success": "#0B6B2B",
        "warning": "#8A5A00",
        "error": "#8B0000",
        "accent": "blue",
        "border": "bright_black",
    },
}

MODERN_BOX = getattr(box, "ROUNDED", box.MINIMAL)


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


def _detect_mac_theme():
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        if result.returncode == 0 and "Dark" in result.stdout:
            return "dark"
        return "light"
    except Exception:
        pass
    return None


def _detect_linux_theme():
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        if result.returncode == 0:
            if "prefer-dark" in result.stdout:
                return "dark"
            elif "prefer-light" in result.stdout or "default" in result.stdout:
                return "light"
    except Exception:
        pass
    return None


def _detect_os_theme():
    if sys.platform == "darwin":
        return _detect_mac_theme()
    elif sys.platform.startswith("linux"):
        return _detect_linux_theme()
    return None


def _detect_terminal_theme():
    colorfgbg = os.getenv("COLORFGBG")
    if not colorfgbg:
        return _detect_os_theme()

    try:
        background = int(colorfgbg.split(";")[-1])
    except ValueError:
        return _detect_os_theme()

    if background in {0, 1, 2, 3, 4, 5, 6, 8}:
        return "dark"
    if background in {7, 9, 10, 11, 12, 13, 14, 15}:
        return "light"

    return _detect_os_theme()


def _active_theme():
    if _selected_theme in {"dark", "light"}:
        return _selected_theme

    detected_theme = _detect_terminal_theme()
    if detected_theme in {"dark", "light"}:
        return detected_theme

    return "dark"


def _style(name: str):
    theme = _active_theme()
    return _THEME_STYLES.get(theme, _THEME_STYLES["dark"]).get(
        name,
        _THEME_STYLES["dark"]["main"],
    )


def _bold_style(name: str):
    return f"bold {_style(name)}"


def color_tag(name: str):
    return f"[{_style(name)}]"


def clear_console():
    console.clear()


def progress_styles():
    return {
        "style": _style("muted"),
        "complete_style": _style("success"),
        "finished_style": _style("success"),
        "pulse_style": _style("accent"),
    }


def _prompt_theme():
    styles = {
        "prompt": _style("main"),
        "prompt.choices": _style("muted"),
        "prompt.default": _style("muted"),
        "prompt.invalid": _style("error"),
        "prompt.invalid.choice": _style("warning"),
    }

    return Theme(styles)


def ask_confirm(prompt: str) -> bool:
    prompt_text = Text(str(prompt), style=_style("main"))
    console.push_theme(_prompt_theme())
    try:
        return Confirm.ask(prompt_text, console=console)
    finally:
        console.pop_theme()


def print_help(help_text: str):
    text = Text()
    in_usage = False
    for line in help_text.splitlines(keepends=True):
        stripped = line.strip()
        style = _style("main")

        if stripped.startswith("usage:"):
            in_usage = True
            style = _bold_style("accent")
        elif in_usage:
            if stripped == "" or stripped.endswith(":"):
                in_usage = False
                if stripped.endswith(":"):
                    style = _bold_style("accent")
            else:
                style = _bold_style("accent")
        elif stripped.endswith(":"):
            style = _bold_style("accent")

        text.append(line, style=style)

    console.print(text, end="")


def print_output(text, style_name: str = "main"):
    console.print(text, style=_style(style_name))


def print_info(text):
    """Print a regular CLI message using the active contrast."""
    print_output(f"ℹ {text}", "main")


def print_success(text):
    """Print a success message."""
    print_output(f"✔ {text}", "success")


def print_warn(text: str):
    """Print a warning message."""
    print_output(f"⚠ {text}", "warning")


def print_error(text: str):
    """Print an error message."""
    print_output(f"✖ {text}", "error")


def print_status(label: str, value: str, status: str = "success"):
    text = Text()
    text.append(label, style=_style(status))
    text.append(" ")
    text.append(str(value), style=_style("main"))
    console.print(text)


def generate_table(the_dict: dict, table_name: str = "", field: str = "") -> Table:
    table = Table(
        title=table_name or None,
        title_style=_bold_style("main"),
        border_style=_style("border"),
        pad_edge=True,
        padding=(0, 1),
        box=MODERN_BOX,
        safe_box=True,
        expand=True,
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

    return table


def print_table(the_dict: dict, table_name: str = "", field: str = ""):
    table = generate_table(the_dict, table_name, field)
    console.print(table)


def make_progress_bar() -> Progress:
    progress_bar = Progress(
        TextColumn("[{task.description}]", style=_style("main")),
        BarColumn(
            bar_width=40,
            complete_style=_style("success"),
            finished_style=_style("success"),
            pulse_style=_style("accent"),
        ),
        TaskProgressColumn(style=_bold_style("accent")),
        TextColumn("[{task.completed}/{task.total}]", style=_style("muted")),
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
            border_style=_style("accent"),
            padding=(1, 2),
            box=MODERN_BOX,
            width=min(console.width, 140) if console.width else 140,
        ),
    )


def print_diff_table(the_dict: dict, table_name: str = "", field: str = ""):
    table = Table(
        title=table_name or None,
        title_style=_bold_style("main"),
        border_style=_style("border"),
        pad_edge=True,
        padding=(0, 1),
        box=MODERN_BOX,
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
