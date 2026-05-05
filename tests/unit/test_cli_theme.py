from argparse import Namespace
from io import StringIO

import pytest
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import src.cli.cli as cli
import src.cli.parsers as parsers
import src.cli.utils as cli_utils


class DummyConsole:
    width = 80

    def __init__(self):
        self.calls = []
        self.lines = []
        self.pushed_themes = []
        self.popped = 0

    def print(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    def rule(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    def line(self, count=1):
        self.lines.append(count)

    def push_theme(self, theme):
        self.pushed_themes.append(theme)

    def pop_theme(self):
        self.popped += 1


def test_auto_theme_detects_terminal_background(monkeypatch):
    cli_utils.configure_theme("auto")

    monkeypatch.setenv("COLORFGBG", "15;0")
    assert cli_utils._active_theme() == "dark"
    assert cli_utils._style("main") == "bright_white"

    monkeypatch.setenv("COLORFGBG", "0;15")
    assert cli_utils._active_theme() == "light"
    assert cli_utils._style("main") == "black"


def test_auto_theme_fallback_is_safe_when_colorfgbg_is_missing(monkeypatch):
    monkeypatch.delenv("COLORFGBG", raising=False)
    monkeypatch.setenv("MSGRAM_COLOR_THEME", "dark")

    cli_utils.configure_theme("auto")

    assert cli_utils._active_theme() == "dark"
    assert cli_utils._style("main") == "bright_white"
    assert cli_utils._style("success") == "bright_green"


def test_light_and_dark_theme_main_styles_are_distinct():
    cli_utils.configure_theme("light")
    assert cli_utils._style("main") == "black"
    assert cli_utils.color_tag("main") == "[black]"

    cli_utils.configure_theme("dark")
    assert cli_utils._style("main") == "bright_white"
    assert cli_utils.color_tag("main") == "[bright_white]"


def test_status_styles_are_distinct_for_light_and_dark():
    cli_utils.configure_theme("light")
    light_styles = {
        cli_utils._style("success"),
        cli_utils._style("warning"),
        cli_utils._style("error"),
    }

    cli_utils.configure_theme("dark")
    dark_styles = {
        cli_utils._style("success"),
        cli_utils._style("warning"),
        cli_utils._style("error"),
    }

    assert light_styles == {"#0B6B2B", "#8A5A00", "#8B0000"}
    assert dark_styles == {"bright_green", "bright_yellow", "bright_red"}
    assert len(light_styles) == 3
    assert len(dark_styles) == 3


def test_progress_styles_follow_active_theme():
    cli_utils.configure_theme("light")

    assert cli_utils.progress_styles() == {
        "style": "bright_black",
        "complete_style": "#0B6B2B",
        "finished_style": "#0B6B2B",
        "pulse_style": "blue",
    }


def test_invalid_theme_falls_back_to_safe_theme(monkeypatch):
    monkeypatch.delenv("COLORFGBG", raising=False)

    cli_utils.configure_theme("sepia")

    assert cli_utils._active_theme() == "dark"
    assert cli_utils._style("warning") == "bright_yellow"


@pytest.mark.parametrize(
    "printer,expected_style",
    [
        (cli_utils.print_info, "black"),
        (cli_utils.print_success, "#0B6B2B"),
        (cli_utils.print_warn, "#8A5A00"),
        (cli_utils.print_error, "#8B0000"),
    ],
)
def test_output_functions_use_active_theme(monkeypatch, printer, expected_style):
    dummy_console = DummyConsole()
    monkeypatch.setattr(cli_utils, "console", dummy_console)
    cli_utils.configure_theme("light")

    printer("message")

    assert dummy_console.calls[-1][0] == ("message",)
    assert dummy_console.calls[-1][1]["style"] == expected_style


def test_print_status_uses_status_and_main_styles(monkeypatch):
    dummy_console = DummyConsole()
    monkeypatch.setattr(cli_utils, "console", dummy_console)
    cli_utils.configure_theme("dark")

    cli_utils.print_status("Reading:", "file.metrics", "success")

    printed_text = dummy_console.calls[-1][0][0]
    assert isinstance(printed_text, Text)
    assert printed_text.plain == "Reading: file.metrics"
    assert str(printed_text.spans[0].style) == "bright_green"
    assert str(printed_text.spans[-1].style) == "bright_white"


def test_print_table_renders_headers_and_data(monkeypatch):
    output = StringIO()
    monkeypatch.setattr(
        cli_utils,
        "console",
        Console(file=output, force_terminal=False, color_system=None, width=80),
    )
    cli_utils.configure_theme("light")

    cli_utils.print_table({"coverage": "0.95"}, "metrics", "metric")

    rendered = output.getvalue()
    assert "metric" in rendered
    assert "values" in rendered
    assert "coverage" in rendered
    assert "0.95" in rendered


def test_print_diff_table_builds_rich_table(monkeypatch):
    dummy_console = DummyConsole()
    monkeypatch.setattr(cli_utils, "console", dummy_console)
    cli_utils.configure_theme("dark")

    cli_utils.print_diff_table(
        {"reliability": {"planned": 0.5, "developed": 0.8, "diff": -0.3}},
        "diff",
        "Characteristics",
    )

    printed_table = dummy_console.calls[-1][0][0]
    assert isinstance(printed_table, Table)
    assert [column.header for column in printed_table.columns] == [
        "Characteristics",
        "Planned",
        "Developed",
        "Diff",
    ]


def test_format_diff_color_uses_status_styles():
    cli_utils.configure_theme("light")

    assert cli_utils.format_diff_color({"planned": 0.5, "developed": 0.8}) == "#0B6B2B"
    assert cli_utils.format_diff_color({"planned": 0.8, "developed": 0.5}) == "#8B0000"
    assert cli_utils.format_diff_color({"planned": 0.5, "developed": 0.5}) == "black"


def test_rule_and_panel_use_theme_styles(monkeypatch):
    dummy_console = DummyConsole()
    monkeypatch.setattr(cli_utils, "console", dummy_console)
    cli_utils.configure_theme("light")

    cli_utils.print_rule("Title", "details")
    cli_utils.print_panel("message", title="Done")

    assert dummy_console.calls[0][0] == ("Title",)
    assert dummy_console.calls[0][1]["style"] == "blue"
    assert dummy_console.calls[1][0] == ("details",)
    assert dummy_console.calls[1][1]["style"] == "bright_black"
    assert dummy_console.lines == [1, 2]
    assert isinstance(dummy_console.calls[-1][0][0], Panel)


def test_make_progress_bar_uses_themed_error_style():
    cli_utils.configure_theme("dark")

    progress = cli_utils.make_progress_bar()

    assert progress is not None


def test_confirm_wrapper_uses_themed_text_and_returns_boolean(monkeypatch):
    dummy_console = DummyConsole()
    monkeypatch.setattr(cli_utils, "console", dummy_console)
    cli_utils.configure_theme("light")
    seen = {}

    def fake_confirm(prompt, console):
        seen["prompt"] = prompt
        seen["console"] = console
        return True

    monkeypatch.setattr(cli_utils.Confirm, "ask", fake_confirm)

    assert cli_utils.ask_confirm("> Continue?") is True
    assert seen["console"] is dummy_console
    assert seen["prompt"].plain == "> Continue?"
    assert str(seen["prompt"].style) == "black"
    assert dummy_console.pushed_themes
    assert dummy_console.popped == 1


def test_print_help_uses_themed_text(monkeypatch):
    dummy_console = DummyConsole()
    monkeypatch.setattr(cli_utils, "console", dummy_console)
    cli_utils.configure_theme("dark")

    cli_utils.print_help("usage: msgram [-h]\n\noptions:\n  -h, --help\n")

    printed_help = dummy_console.calls[-1][0][0]
    assert isinstance(printed_help, Text)
    assert "usage: msgram [-h]" in printed_help.plain
    assert "options:" in printed_help.plain
    assert "bold" in str(printed_help.spans[0].style)
    assert "bright_cyan" in str(printed_help.spans[0].style)


def test_parser_accepts_theme_values_and_rejects_invalid_theme():
    parser = parsers.create_parser()

    assert parser.parse_args(["--theme", "auto"]).theme == "auto"
    assert parser.parse_args(["--theme", "dark"]).theme == "dark"
    assert parser.parse_args(["--theme", "light"]).theme == "light"
    assert parser.parse_args(["init", "--theme", "light"]).command_theme == "light"

    with pytest.raises(SystemExit):
        parser.parse_args(["--theme", "sepia"])


def test_themed_parser_prints_help_with_centralized_output(monkeypatch):
    printed = {}

    def fake_print_help(help_text):
        printed["help"] = help_text

    monkeypatch.setattr(parsers, "print_help", fake_print_help)
    parser = parsers.create_parser()

    parser.print_help()

    assert "usage: msgram [-h]" in printed["help"]


def test_subcommand_help_uses_themed_parser(monkeypatch):
    printed = {}

    def fake_print_help(help_text):
        printed["help"] = help_text

    monkeypatch.setattr(parsers, "print_help", fake_print_help)
    parser = parsers.create_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["init", "--theme", "dark", "-h"])

    assert "usage: msgram init" in printed["help"]


def test_cli_theme_helpers_and_parse_args():
    assert cli.get_theme_from_argv(["msgram"]) == "auto"
    assert cli.get_theme_from_argv(["msgram", "--theme", "dark", "init"]) == "dark"
    assert cli.get_theme_from_argv(["msgram", "init", "--theme=light"]) == "light"

    raw_args = Namespace(command="init", func=lambda args: args, theme="dark")
    assert cli.get_theme_from_namespace(raw_args) == "dark"

    command_args = Namespace(
        command="init",
        func=lambda args: args,
        theme="auto",
        command_theme="light",
        config_path="/tmp/config",
    )

    assert cli.get_theme_from_namespace(command_args) == "light"

    func, args = cli.parse_args(command_args)
    assert callable(func)
    assert args == {"config_path": "/tmp/config"}


def test_run_cli_configures_theme_before_executing_command(monkeypatch):
    configured_themes = []
    received_args = []

    def fake_configure_theme(theme):
        configured_themes.append(theme)

    def fake_command(args):
        received_args.append(args)

    class FakeParser:
        def parse_args(self):
            return Namespace(
                command="init",
                func=fake_command,
                theme="auto",
                command_theme="light",
                config_path="/tmp/config",
            )

    monkeypatch.setattr(cli, "configure_theme", fake_configure_theme)
    monkeypatch.setattr(cli, "create_parser", lambda: FakeParser())
    monkeypatch.setattr(cli.sys, "argv", ["msgram", "--theme", "dark", "init"])

    cli.run_cli()

    assert configured_themes == ["dark", "light"]
    assert received_args == [{"config_path": "/tmp/config"}]
