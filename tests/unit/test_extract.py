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
    "output_origin": "sonarqube",
    "extracted_path": Path(""),
    "data_path": Path(""),
    "language_extension": "py"
}


def test_get_file_infos():
    file_path = "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json"

    file_name = get_infos_from_name(file_path)
    assert "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop-extracted.msgram" in file_name


def test_not_get_file_infos_wrong_name():
    filename = "metrics/wrong-name.json"

    with pytest.raises(SystemExit) as e:
        _ = get_infos_from_name(filename)

    assert e.value.code == 1


def test_command_extract_should_succeed():
    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram.json",
        f"{config_dirpath}/msgram.json"
    )

    shutil.copy(
        "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json",
        f"{extract_dirpath}/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json"
    )

    args = {
        "output_origin": "sonarqube",
        "extracted_path": Path(config_dirpath),
        "data_path": Path(extract_dirpath),
        "language_extension": "py"
    }

    captured_output = StringIO()
    sys.stdout = captured_output

    command_extract(args)

    sys.stdout = sys.__stdout__

    assert "Metrics successfully extracted" in captured_output.getvalue()
    assert os.path.isfile(
        f"{config_dirpath}/fga-eps-mds-2022-2-MeasureSoftGram-"
        "CLI-01-11-2023-21-59-03-develop-extracted.msgram"
    )

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


@pytest.mark.parametrize(
    "extract_arg",
    ['output_origin', 'extracted_path', 'data_path', 'language_extension']
)
def test_extract_invalid_args(extract_arg):
    captured_output = StringIO()
    sys.stdout = captured_output

    args = copy.deepcopy(EXTRACT_ARGS)
    del args[extract_arg]

    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__
    assert f"KeyError: args['{extract_arg}'] - non-existent parameters" in captured_output.getvalue()


def test_command_extract_extracted_path_is_not_a_dir():
    captured_output = StringIO()
    sys.stdout = captured_output

    args = copy.deepcopy(EXTRACT_ARGS)
    args['extracted_path'] = Path('inexistent')

    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__
    assert 'FileNotFoundError: extract directory' in captured_output.getvalue()
