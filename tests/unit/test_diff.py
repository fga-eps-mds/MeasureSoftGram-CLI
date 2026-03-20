import copy

import json
import shutil
import sys
from io import StringIO
from pathlib import Path
import tempfile

import pytest

from src.cli.commands.cmd_diff import command_diff

CALCULATE_ARGS = {
    "output_format": "json",
    "rp_path": Path(""),
    "rd_path": Path(""),
}


@pytest.mark.parametrize("diff_arg", ["output_format", "rp_path", "rd_path"])
def test_diff_invalid_args(diff_arg):
    captured_output = StringIO()
    sys.stdout = captured_output

    args = copy.deepcopy(CALCULATE_ARGS)
    del args[diff_arg]

    with pytest.raises(SystemExit):
        command_diff(args)

    sys.stdout = sys.__stdout__
    assert (
        f"KeyError: args['{diff_arg}'] - non-existent parameters"
        in captured_output.getvalue()
    )


def test_diff_file():
    config_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram_diff.json", f"{config_dirpath}/msgram_diff.json"
    )
    shutil.copy(
        "tests/unit/data/calc_msgram_diff.json",
        f"{config_dirpath}/calc_msgram_diff.json",
    )
    shutil.copy(
        "tests/unit/data/calc_exptc_diff_msgram.json",
        f"{config_dirpath}/calc_exptc_diff_msgram.json",
    )

    args = {
        "output_format": "json",
        "rp_path": Path(config_dirpath + "/msgram_diff.json"),
        "rd_path": Path(config_dirpath + "/calc_msgram_diff.json"),
    }

    command_diff(args)

    with open(config_dirpath + "/calc_diff_msgram.json", "r") as f:
        output_data = json.load(f)

    with open(config_dirpath + "/calc_exptc_diff_msgram.json", "r") as f:
        expected_data = json.load(f)

    assert output_data == expected_data

    shutil.rmtree(config_dirpath)


def test_diff_invalid_config_file():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/invalid_json.json", f"{config_dirpath}/invalid_json.json"
    )

    args = {
        "output_format": "csv",
        "rp_path": Path(config_dirpath + "/msgram_diff.json"),
        "rd_path": Path(config_dirpath + "/calc_msgram_diff.json"),
    }

    with pytest.raises(SystemExit):
        command_diff(args)

    sys.stdout = sys.__stdout__
    assert (
        f"Error reading config file in {config_dirpath}" in captured_output.getvalue()
    )

    shutil.rmtree(config_dirpath)


def test_diff_invalid_config_value():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram_diff_error.json",
        f"{config_dirpath}/msgram_diff_error.json",
    )
    shutil.copy(
        "tests/unit/data/calc_msgram_diff.json",
        f"{config_dirpath}/calc_msgram_diff.json",
    )

    args = {
        "output_format": "json",
        "rp_path": Path(config_dirpath + "/msgram_diff_error.json"),
        "rd_path": Path(config_dirpath + "/calc_msgram_diff.json"),
    }

    with pytest.raises(SystemExit):
        command_diff(args)

    sys.stdout = sys.__stdout__
    assert (
        "Failed to decode the JSON file: The values informed in the"
        in captured_output.getvalue()
    )

    shutil.rmtree(config_dirpath)


def test_diff_invalid_calculated_file():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram_diff.json", f"{config_dirpath}/msgram_diff.json"
    )

    args = {
        "output_format": "csv",
        "rp_path": Path(config_dirpath + "/msgram_diff.json"),
        "rd_path": Path(config_dirpath + "/calc_msgram_error.json"),
    }

    with pytest.raises(SystemExit):
        command_diff(args)

    sys.stdout = sys.__stdout__
    assert (
        f"Error reading calculated file in {config_dirpath}"
        in captured_output.getvalue()
    )

    shutil.rmtree(config_dirpath)


def test_diff_invalid_vectors_size():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram_diff_extra.json",
        f"{config_dirpath}/msgram_diff.json",
    )
    shutil.copy(
        "tests/unit/data/calc_msgram_diff.json",
        f"{config_dirpath}/calc_msgram_diff.json",
    )

    args = {
        "output_format": "csv",
        "rp_path": Path(config_dirpath + "/msgram_diff.json"),
        "rd_path": Path(config_dirpath + "/calc_msgram_diff.json"),
    }

    with pytest.raises(SystemExit):
        command_diff(args)

    sys.stdout = sys.__stdout__
    assert (
        "Error calculating: The size between planned and developed release vectors is not equal."
        in captured_output.getvalue()
    )

    shutil.rmtree(config_dirpath)


def test_diff_differents_characteristics():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram_diff_different.json",
        f"{config_dirpath}/msgram_diff.json",
    )
    shutil.copy(
        "tests/unit/data/calc_msgram_diff.json",
        f"{config_dirpath}/calc_msgram_diff.json",
    )

    args = {
        "output_format": "csv",
        "rp_path": Path(config_dirpath + "/msgram_diff.json"),
        "rd_path": Path(config_dirpath + "/calc_msgram_diff.json"),
    }

    with pytest.raises(SystemExit):
        command_diff(args)

    sys.stdout = sys.__stdout__
    assert (
        "Planned and calculated files have differents characteristics"
        in captured_output.getvalue()
    )

    shutil.rmtree(config_dirpath)
