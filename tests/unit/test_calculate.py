import os
import sys
import copy
import pytest
import tempfile
import shutil

from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.cli.commands.cmd_calculate import command_calculate, calculate_all
from src.cli.jsonReader import open_json_file

CALCULATE_ARGS = {
    "output_format": "csv",
    "config_path": Path(""),
    "extracted_path": Path(""),
}


@pytest.mark.parametrize(
    "calculate_arg",
    ['output_format', 'config_path', 'extracted_path']
)
def test_calculate_invalid_args(calculate_arg):
    captured_output = StringIO()
    sys.stdout = captured_output

    args = copy.deepcopy(CALCULATE_ARGS)
    del args[calculate_arg]

    with pytest.raises(SystemExit):
        command_calculate(args)

    sys.stdout = sys.__stdout__
    assert f"KeyError: args['{calculate_arg}'] - non-existent parameters" in captured_output.getvalue()


@pytest.mark.parametrize(
    "output_format,mult_file",
    [
        ("tabular", False), ("tree", False), ("raw", False),
        ("csv", True), ("json", True)
    ]
)
def test_calculate_file(output_format, mult_file):
    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram.json",
        f"{config_dirpath}/msgram.json"
    )

    extracted_file_name = "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram"
    shutil.copy(
        f"tests/unit/data/{extracted_file_name}",
        f"{extract_dirpath}/{extracted_file_name}"
    )

    args = {
        "output_format": output_format,
        "config_path": Path(config_dirpath),
        "extracted_path": Path(
            extract_dirpath + (f"/{extracted_file_name}" if not mult_file else "")
        ),
    }

    if not mult_file:
        calculate_patch = patch('builtins.input', return_value=output_format)
        calculate_patch.start()

    command_calculate(args)

    assert len(os.listdir(config_dirpath)) == 2 if mult_file else 1
    assert len(os.listdir(extract_dirpath)) == 1

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


def test_calculate_all_dict():
    file_name = "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram"
    json_data = open_json_file(Path(f"tests/unit/data/{file_name}"))
    config = open_json_file(Path('tests/unit/data/msgram.json'))

    calculated = calculate_all(json_data, file_name, config)

    assert calculated == {
        'repository': [{'key': 'repository', 'value': 'fga-eps-mds-2022-2-MeasureSoftGram-CLI'}],
        'version': [{'key': 'version', 'value': '01-05-2023-21-40'}],
        'measures': [
            {'key': 'passed_tests', 'value': 1.0},
            {'key': 'test_builds', 'value': 0.9999969696180555},
            {'key': 'test_coverage', 'value': 0.5153846153846154},
            {'key': 'non_complex_file_density', 'value': 0.4829268292682926},
            {'key': 'commented_file_density', 'value': 0.029230769230769227},
            {'key': 'duplication_absense', 'value': 1.0}
        ],
        'subcharacteristics': [
            {'key': 'testing_status', 'value': 0.8633460569923477},
            {'key': 'modifiability', 'value': 0.650528195701257}
        ],
        'characteristics': [
            {'key': 'reliability', 'value': 0.8633460569923477},
            {'key': 'maintainability', 'value': 0.650528195701257}
        ],
        'sqc': [{'key': 'sqc', 'value': 0.7643799276297641}]
    }


def test_calculate_invalid_config_file():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/invalid_json.json",
        f"{config_dirpath}/msgram.json"
    )

    args = {
        "output_format": 'csv',
        "config_path": Path(config_dirpath),
        "extracted_path": Path("."),
    }

    with pytest.raises(SystemExit):
        command_calculate(args)

    sys.stdout = sys.__stdout__
    assert f"Error reading msgram.json config file in {config_dirpath}" in captured_output.getvalue()

    shutil.rmtree(config_dirpath)


def test_calculate_invalid_extracted_file():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram.json",
        f"{config_dirpath}/msgram.json"
    )

    extracted_file_name = "invalid_json.json"
    shutil.copy(
        f"tests/unit/data/{extracted_file_name}",
        f"{extract_dirpath}/{extracted_file_name}"
    )

    args = {
        "output_format": "csv",
        "config_path": Path(config_dirpath),
        "extracted_path": Path(
            extract_dirpath + f"/{extracted_file_name}"),
    }

    command_calculate(args)

    sys.stdout = sys.__stdout__
    assert f"Error calculating {extract_dirpath}/{extracted_file_name}" in captured_output.getvalue()
    assert "All calculations performed" not in captured_output.getvalue()

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


def test_calculate_warn_zero_calculated_files():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()

    shutil.copy(
        "tests/unit/data/msgram.json",
        f"{config_dirpath}/msgram.json"
    )

    args = {
        "output_format": "csv",
        "config_path": Path(config_dirpath),
        "extracted_path": Path("."),
    }

    command_calculate(args)

    sys.stdout = sys.__stdout__
    assert "WARNING: No extracted file readed so no csv was generated!" in captured_output.getvalue()
    assert "All calculations performed" not in captured_output.getvalue()

    shutil.rmtree(config_dirpath)
