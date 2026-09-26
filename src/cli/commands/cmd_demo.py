import logging
import sys
from pathlib import Path

from src.cli.commands.cmd_init import command_init
from src.cli.commands.cmd_extract import command_extract
from src.cli.commands.cmd_calculate import command_calculate
from src.cli.utils import (
    clear_console,
    print_error,
    print_info,
    print_panel,
    print_rule,
    print_success,
)

logger = logging.getLogger("msgram")

# Directory name of the embedded sample dataset shipped with the repository.
EXAMPLES_DIRNAME = "examples"
RAW_DATA_DIRNAME = "analytics-raw-data"
DEFAULT_DEMO_OUTPUT = Path.cwd() / "msgram-demo"


def find_raw_data_dir() -> Path:
    """Locate the embedded sample dataset.

    The lookup is done relative to this module (not the current working
    directory) so the demo keeps working when the CLI is installed and run
    from outside the repository. We walk up the parents of this file looking
    for `examples/analytics-raw-data`.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / EXAMPLES_DIRNAME / RAW_DATA_DIRNAME
        if candidate.is_dir() and any(candidate.glob("*.json")):
            return candidate

    raise FileNotFoundError(
        f"Could not find the embedded sample dataset '{EXAMPLES_DIRNAME}/"
        f"{RAW_DATA_DIRNAME}' with a Sonar JSON file."
    )


def command_demo(args):
    try:
        output_path: Path = args.get("output_path") or DEFAULT_DEMO_OUTPUT
        output_format: str = args.get("output_format") or "csv"

    except Exception as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        sys.exit(1)

    output_path = Path(output_path).absolute()

    try:
        raw_data_path = find_raw_data_dir()
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)

    clear_console()
    print_rule("MSGram demo", "Running an end-to-end pipeline on a sample dataset:")
    print_info(f"> Working directory: {output_path}")
    print_info(f"> Sample dataset:    {raw_data_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    # Remove a previous config so `init` never prompts for a replacement,
    # keeping the demo fully non-interactive when re-run.
    config_file = output_path / "msgram.json"
    if config_file.exists():
        config_file.unlink()

    # Step 1: init - generate msgram.json from the default pre config.
    command_init({"config_path": output_path})

    # Step 2: extract - read the embedded Sonar JSON into a .metrics file.
    command_extract(
        {
            "extracted_path": output_path,
            "sonar_path": raw_data_path,
        }
    )

    # Step 3: calculate - compute the four quality layers and export.
    command_calculate(
        {
            "extracted_path": output_path,
            "config_path": output_path,
            "output_format": output_format,
        }
    )

    result_name = "calc_msgram.json" if output_format == "json" else "calc_msgram.csv"
    result_file = output_path / result_name

    print_success("\nDemo finished successfully!")
    print_panel(
        title="Demo done",
        menssage=(
            "> The end-to-end pipeline (init -> extract -> calculate) ran on the "
            "embedded sample dataset.\n"
            f"> Config file:  {config_file}\n"
            f"> Result file:  {result_file}\n"
            "> Inspect the result or re-run with your own data following the README."
        ),
    )
