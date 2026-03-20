import sys
import pytest
import tempfile
import shutil
import os
import copy

from io import StringIO
from pathlib import Path

from src.cli.commands.cmd_extract import get_infos_from_name, command_extract

EXTRACT_ARGS = {
    "extracted_path": Path(""),
    "sonar_path": Path(""),
}


def test_get_file_infos():
    file_path = "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json"

    file_name = get_infos_from_name(file_path)
    assert (
        "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop-extracted.metrics"
        in file_name
    )


def test_not_get_file_infos_wrong_name():
    filename = "metrics/wrong-name.json"

    with pytest.raises(SystemExit) as e:
        _ = get_infos_from_name(filename)

    assert e.value.code == 1


def test_command_extract_should_succeed():
    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy("tests/unit/data/msgram.json", f"{config_dirpath}/msgram.json")

    shutil.copy(
        "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json",
        f"{extract_dirpath}/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json",
    )

    args = {
        "extracted_path": Path(config_dirpath),
        "sonar_path": Path(extract_dirpath),
    }

    captured_output = StringIO()
    sys.stdout = captured_output

    command_extract(args)

    sys.stdout = sys.__stdout__

    assert "Metrics successfully extracted" in captured_output.getvalue()
    assert os.path.isfile(
        f"{config_dirpath}/fga-eps-mds-2022-2-MeasureSoftGram-"
        "CLI-01-11-2023-21-59-03-develop-extracted.metrics"
    )

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


@pytest.mark.parametrize(
    "extract_arg",
    ["extracted_path"],
)
def test_extract_invalid_args(extract_arg):
    captured_output = StringIO()
    sys.stdout = captured_output

    args = copy.deepcopy(EXTRACT_ARGS)
    del args[extract_arg]

    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__
    assert (
        f"KeyError: args['{extract_arg}'] - non-existent parameters"
        in captured_output.getvalue()
    )


def test_extract_fail_no_dp_or_rep():
    extract_dirpath = tempfile.mkdtemp()
    args = {
        "extracted_path": Path(extract_dirpath),
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert (
        "It is necessary to pass sonar_path, github_repository or the pe_ parameters"
        in captured_output.getvalue()
    )


def test_extract_fail_date_format():
    extract_dirpath = tempfile.mkdtemp()
    args = {
        "extracted_path": Path(extract_dirpath),
        "gh_repository": "fga-eps-mds/2023-1-MeasureSoftGram-DOC",
        "gh_date_range": "20/06/2023-15/07/2021",
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert (
        "Error: Range of dates for filter must be in format 'dd/mm/yyyy-dd/mm/yyyy'"
        in captured_output.getvalue()
    )


def test_extract_directory_not_exist():
    args = {
        "extracted_path": Path("tests/directory_not_exist"),
        "sonar_path": Path("tests/directory_not_exist"),
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert "FileNotFoundError: extract directory" in captured_output.getvalue()


def test_performance_efficiency_data_extraction():
    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy("tests/unit/data/msgram.json", f"{config_dirpath}/msgram.json")

    shutil.copy(
        "tests/unit/data/perf-eff-data-1.csv",
        f"{extract_dirpath}/perf-eff-data-1.csv",
    )

    shutil.copy(
        "tests/unit/data/perf-eff-data-2.csv",
        f"{extract_dirpath}/perf-eff-data-2.csv",
    )

    args = {
        "extracted_path": Path(extract_dirpath),
        "pe_release_1": Path(f"{extract_dirpath}/perf-eff-data-1.csv"),
        "pe_release_2": Path(f"{extract_dirpath}/perf-eff-data-2.csv"),
        "pe_repository_name": "perf-eff-csv",
    }

    captured_output = StringIO()
    sys.stdout = captured_output

    command_extract(args)

    sys.stdout = sys.__stdout__

    assert len(os.listdir(config_dirpath)) == 1
    assert len(os.listdir(extract_dirpath)) == 3

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)
