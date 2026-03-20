import copy
import os
import shutil
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch
import filecmp

import pytest

from src.cli.commands.cmd_calculate import calculate_all, command_calculate, show_tree
from src.cli.jsonReader import open_json_file
from staticfiles import DEFAULT_PRE_CONFIG as pre_config

CALCULATE_ARGS = {
    "output_format": "csv",
    "config_path": Path(""),
    "extracted_path": Path(""),
}


def test_show_tree(capfd):

    data_calculated = {
        "repository": [
            {"key": "repository", "value": "fga-eps-mds-2022-2-MeasureSoftGram-CLI"}
        ],
        "version": [{"key": "version", "value": "01-05-2023-21-40"}],
        "measures": [
            {"key": "passed_tests", "value": 1.0},
            {"key": "test_builds", "value": 0.9996066627522133},
            {"key": "test_coverage", "value": 0.40234848484848484},
            {"key": "non_complex_file_density", "value": 0.44347274991556906},
            {"key": "commented_file_density", "value": 0.04318181818181818},
            {"key": "duplication_absence", "value": 1.0},
            {"key": "team_throughput", "value": 0.6969696969696971},
            {"key": "ci_feedback_time", "value": 0.06117908787541713},
        ],
        "subcharacteristics": [
            {"key": "testing_status", "value": 0.8421061048464034},
            {"key": "maturity", "value": 0.06117908787541713},
            {"key": "modifiability", "value": 0.6415437113263573},
            {"key": "functional_completeness", "value": 0.6969696969696971},
        ],
        "characteristics": [
            {"key": "reliability", "value": 0.5970282960684735},
            {"key": "maintainability", "value": 0.6415437113263573},
            {"key": "functional_suitability", "value": 0.6969696969696971},
        ],
        "tsqmi": [{"key": "tsqmi", "value": 0.6455181338484177}],
    }

    expected_output = (
        "Overview - tree:\n\n"
        "\n"
        "tsqmi: 0.6455181338484177\n"
        "├── reliability: 0.5970282960684735\n"
        "│   ├── testing_status 0.8421061048464034\n"
        "│   │   ├── passed_tests 1.0\n"
        "│   │   ├── test_builds 0.9996066627522133\n"
        "│   │   └── test_coverage 0.40234848484848484\n"
        "│   └── maturity 0.06117908787541713\n"
        "│       └── ci_feedback_time 0.06117908787541713\n"
        "├── maintainability: 0.6415437113263573\n"
        "│   └── modifiability 0.6415437113263573\n"
        "│       ├── non_complex_file_density 0.44347274991556906\n"
        "│       └── commented_file_density 0.04318181818181818\n"
        "└── functional_suitability: 0.6969696969696971\n"
        "    └── functional_completeness 0.6969696969696971\n"
        "        └── team_throughput 0.6969696969696971"
    )

    show_tree(data_calculated, pre_config)

    captured = capfd.readouterr()

    assert captured.out.strip() == expected_output.strip()


@pytest.mark.parametrize(
    "calculate_arg", ["output_format", "config_path", "extracted_path"]
)
def test_calculate_invalid_args(calculate_arg):
    captured_output = StringIO()
    sys.stdout = captured_output

    args = copy.deepcopy(CALCULATE_ARGS)
    del args[calculate_arg]

    with pytest.raises(SystemExit):
        command_calculate(args)

    sys.stdout = sys.__stdout__
    assert (
        f"KeyError: args['{calculate_arg}'] - non-existent parameters"
        in captured_output.getvalue()
    )


@pytest.mark.parametrize(
    "output_format,multiple_files",
    [
        ("tabular", False),
        ("tree", False),
        ("raw", False),
        ("csv", True),
        ("json", True),
    ],
)
def test_calculate_file(output_format, multiple_files):
    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy("tests/unit/data/msgram.json", f"{config_dirpath}/msgram.json")

    extracted_file_name = "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.metrics"
    shutil.copy(
        f"tests/unit/data/{extracted_file_name}",
        f"{extract_dirpath}/{extracted_file_name}",
    )

    args = {
        "output_format": output_format,
        "config_path": Path(config_dirpath),
        "extracted_path": Path(extract_dirpath + (f"/{extracted_file_name}")),
    }
    if not multiple_files:
        calculate_patch = patch("builtins.input", return_value=output_format)
        calculate_patch.start()

    command_calculate(args)

    if multiple_files is False:
        assert len(os.listdir(config_dirpath)) == 1
        assert len(os.listdir(extract_dirpath)) == 1

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


def test_calculate_sonar():
    file_name = "fga-eps-mds-2023-2-MeasureSoftGram-Service-12-11-2023-02-57-52-develop-extracted.metrics"
    json_data = open_json_file(Path(f"tests/unit/data/{file_name}"))
    config = open_json_file(Path("tests/unit/data/msgram.json"))

    calculated_result = calculate_all(json_data, file_name, config)
    calculate_expected = {
        "repository": [
            {"key": "repository", "value": "fga-eps-mds-2023-2-MeasureSoftGram-Service"}
        ],
        "version": [{"key": "version", "value": "12-11-2023-02-57"}],
        "measures": [
            {"key": "passed_tests", "value": 1.0},
            {"key": "test_builds", "value": 0.9994736632118764},
            {"key": "test_coverage", "value": 0.799465811965812},
            {"key": "non_complex_file_density", "value": 0.29985992940690925},
            {"key": "commented_file_density", "value": 0.12777777777777777},
            {"key": "duplication_absense", "value": 1.0},
        ],
        "subcharacteristics": [
            {"key": "testing_status", "value": 0.9351668104467522},
            {"key": "modifiability", "value": 0.617602903519865},
        ],
        "characteristics": [
            {"key": "reliability", "value": 0.9351668104467522},
            {"key": "maintainability", "value": 0.617602903519865},
        ],
        "tsqmi": [{"key": "tsqmi", "value": 0.7970842309514055}],
    }
    assert calculated_result.get("repository") == calculate_expected.get("repository")
    assert calculated_result.get("version") == calculate_expected.get("version")
    measures_result = calculated_result.get("measures")
    measures_expected = calculate_expected.get("measures")
    for measure_result, measure_expected in zip(measures_result, measures_expected):
        assert measure_result.get("key") == measure_expected.get("key")
        assert pytest.approx(measure_result.get("value")) == measure_expected.get(
            "value"
        )

    subcharacteristics_result = calculated_result.get("subcharacteristics")
    subcharacteristics_expected = calculate_expected.get("subcharacteristics")
    for subcharacteristic_result, subcharacteristic_expected in zip(
        subcharacteristics_result, subcharacteristics_expected
    ):
        assert subcharacteristic_result.get("key") == subcharacteristic_expected.get(
            "key"
        )
        assert pytest.approx(
            subcharacteristic_result.get("value")
        ) == subcharacteristic_expected.get("value")

    characteristics_result = calculated_result.get("characteristics")
    characteristics_expected = calculate_expected.get("characteristics")
    for characteristic_result, characteristic_expected in zip(
        characteristics_result, characteristics_expected
    ):
        assert characteristic_result.get("key") == characteristic_expected.get("key")
        assert pytest.approx(
            characteristic_result.get("value")
        ) == characteristic_expected.get("value")

    tsqmi_result = calculated_result.get("tsqmi")[0]
    tsqmi_expected = calculate_expected.get("tsqmi")[0]
    assert tsqmi_result.get("key") == tsqmi_expected.get("key")
    assert pytest.approx(tsqmi_result.get("value")) == tsqmi_expected.get("value")


def test_calculate_github():
    file_name = "github_fga-eps-mds-2024.1-MeasureSoftGram-DOC-28-07-2024-00-00-22-extracted.metrics"
    json_data = open_json_file(Path(f"tests/unit/data/{file_name}"))
    config = open_json_file(Path("tests/unit/data/msgram.json"))

    calculated_result = calculate_all(json_data, file_name[len("github_") :], config)
    calculate_expected = {
        "repository": [
            {"key": "repository", "value": "fga-eps-mds-2024.1-MeasureSoftGram-DOC"}
        ],
        "version": [{"key": "version", "value": "28-07-2024-00-00"}],
        "measures": [
            {"key": "team_throughput", "value": 0.0},
            {"key": "ci_feedback_time", "value": 0.03225806451612903},
        ],
        "subcharacteristics": [
            {"key": "maturity", "value": 0.03225806451612903},
            {"key": "functional_completeness", "value": 0.0},
        ],
        "characteristics": [
            {"key": "reliability", "value": 0.03225806451612903},
            {"key": "functional_suitability", "value": 0.0},
        ],
        "tsqmi": [{"key": "tsqmi", "value": 0.023147764246074717}],
    }

    assert calculated_result.get("repository") == calculate_expected.get("repository")
    assert calculated_result.get("version") == calculate_expected.get("version")
    measures_result = calculated_result.get("measures")
    measures_expected = calculate_expected.get("measures")
    for measure_result, measure_expected in zip(measures_result, measures_expected):
        assert measure_result.get("key") == measure_expected.get("key")
        assert pytest.approx(measure_result.get("value")) == measure_expected.get(
            "value"
        )

    subcharacteristics_result = calculated_result.get("subcharacteristics")
    subcharacteristics_expected = calculate_expected.get("subcharacteristics")
    for subcharacteristic_result, subcharacteristic_expected in zip(
        subcharacteristics_result, subcharacteristics_expected
    ):
        assert subcharacteristic_result.get("key") == subcharacteristic_expected.get(
            "key"
        )
        assert pytest.approx(
            subcharacteristic_result.get("value")
        ) == subcharacteristic_expected.get("value")

    characteristics_result = calculated_result.get("characteristics")
    characteristics_expected = calculate_expected.get("characteristics")
    for characteristic_result, characteristic_expected in zip(
        characteristics_result, characteristics_expected
    ):
        assert characteristic_result.get("key") == characteristic_expected.get("key")
        assert pytest.approx(
            characteristic_result.get("value")
        ) == characteristic_expected.get("value")

    tsqmi_result = calculated_result.get("tsqmi")[0]
    tsqmi_expected = calculate_expected.get("tsqmi")[0]
    assert tsqmi_result.get("key") == tsqmi_expected.get("key")
    assert pytest.approx(tsqmi_result.get("value")) == tsqmi_expected.get("value")


def test_calculate_invalid_config_file():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()

    shutil.copy("tests/unit/data/invalid_json.json", f"{config_dirpath}/msgram.json")

    args = {
        "output_format": "csv",
        "config_path": Path(config_dirpath),
        "extracted_path": Path("."),
    }

    with pytest.raises(SystemExit):
        command_calculate(args)

    sys.stdout = sys.__stdout__
    assert (
        f"Error reading msgram.json config file in {config_dirpath}"
        in captured_output.getvalue()
    )

    shutil.rmtree(config_dirpath)


def test_calculate_invalid_extracted_file():
    captured_output = StringIO()
    sys.stdout = captured_output

    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy("tests/unit/data/msgram.json", f"{config_dirpath}/msgram.json")

    extracted_file_name = "invalid_json.json"
    shutil.copy(
        f"tests/unit/data/{extracted_file_name}",
        f"{extract_dirpath}/{extracted_file_name}",
    )

    args = {
        "output_format": "csv",
        "config_path": Path(config_dirpath),
        "extracted_path": Path(extract_dirpath + f"/{extracted_file_name}"),
    }

    command_calculate(args)

    sys.stdout = sys.__stdout__
    assert (
        f"Error calculating {extract_dirpath}/{extracted_file_name}"
        in captured_output.getvalue()
    )
    assert "All calculations performed" not in captured_output.getvalue()

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


def test_calculate_csv_output():
    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy("tests/unit/data/msgram.json", f"{config_dirpath}/msgram.json")

    extracted_file_name = "github_fga-eps-mds-2024.1-MeasureSoftGram-DOC-28-07-2024-00-00-22-extracted.metrics"
    shutil.copy(
        f"tests/unit/data/{extracted_file_name}",
        f"{extract_dirpath}/{extracted_file_name}",
    )

    args = {
        "output_format": "csv",
        "config_path": Path(config_dirpath),
        "extracted_path": Path(extract_dirpath + f"/{extracted_file_name}"),
    }

    command_calculate(args)

    output_path = Path(f"{config_dirpath}/calc_msgram.csv")
    expected_output = Path("tests/unit/data/calc_msgram_exp_github_output.csv")
    assert output_path.stat().st_size > 0
    assert filecmp.cmp(output_path, expected_output, shallow=False)

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


def test_calculate_json_output():
    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy("tests/unit/data/msgram.json", f"{config_dirpath}/msgram.json")

    extracted_file_name = "github_fga-eps-mds-2024.1-MeasureSoftGram-DOC-28-07-2024-00-00-22-extracted.metrics"
    shutil.copy(
        f"tests/unit/data/{extracted_file_name}",
        f"{extract_dirpath}/{extracted_file_name}",
    )

    args = {
        "output_format": "json",
        "config_path": Path(config_dirpath),
        "extracted_path": Path(extract_dirpath + f"/{extracted_file_name}"),
    }

    command_calculate(args)

    output_path = Path(f"{config_dirpath}/calc_msgram.json")
    expected_output = Path("tests/unit/data/calc_msgram_exp_github_output.json")
    assert output_path.stat().st_size > 0
    assert filecmp.cmp(output_path, expected_output, shallow=False)

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)
