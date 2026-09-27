from pathlib import Path
from unittest.mock import patch

import pytest
from staticfiles import DEFAULT_PRE_CONFIG as pre_config

from src.cli.jsonReader import open_json_file
from src.cli.resources.measure import calculate_measures


def test_calculate_measures():
    json_data = open_json_file(
        Path(
            "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram"
        )
    )

    infos, headers = calculate_measures(json_data)
    assert headers == ["Id", "Name", "Description", "Value", "Created at"]
    assert "measures" in infos

    measure_result = infos.get("measures")
    measure_expected = [
        {"key": "passed_tests", "value": 1.0},
        {"key": "test_builds", "value": 0.9996066627522133},
        {"key": "test_coverage", "value": 0.40234848484848484},
        {"key": "non_complex_file_density", "value": 0.44347274991556906},
        {"key": "commented_file_density", "value": 0.04318181818181818},
        {"key": "duplication_absense", "value": 1.0},
    ]
    for measure_result, measure_expected in zip(measure_result, measure_expected):
        assert measure_result.get("key") == measure_expected.get("key")
        assert pytest.approx(measure_result.get("value")) == measure_expected.get(
            "value"
        )


def test_calculate_technical_debt_ratio():
    json_data = {
        "src/a.py": [{"metric": "sqale_debt_ratio", "value": "0.0"}],
        "src/b.py": [{"metric": "sqale_debt_ratio", "value": "8.3"}],
        "src/c.py": [{"metric": "sqale_debt_ratio", "value": "4.0"}],
        "src/d.py": [{"metric": "sqale_debt_ratio", "value": "32.5"}],
    }

    infos, _ = calculate_measures(json_data, pre_config)

    measure_result = infos.get("measures")
    assert len(measure_result) == 1
    assert measure_result[0].get("key") == "technical_debt_ratio"
    assert pytest.approx(measure_result[0].get("value")) == 0.59625


@patch("src.cli.resources.measure.print_warn")
def test_calculate_measures_warns_missing_metric(mock_print_warn):
    json_data = open_json_file(
        Path(
            "tests/unit/data/fga-eps-mds-2023-2-MeasureSoftGram-Service-12-11-2023-02-57-52-develop-extracted.metrics"
        )
    )

    infos, _ = calculate_measures(json_data, pre_config)

    measure_keys = [measure.get("key") for measure in infos.get("measures")]
    assert "technical_debt_ratio" not in measure_keys
    assert "duplication_absense" in measure_keys
    mock_print_warn.assert_called_once_with(
        "Measure 'technical_debt_ratio' could not be calculated. "
        "Missing metrics: sqale_debt_ratio"
    )


@patch("src.cli.resources.measure.print_warn")
def test_calculate_measures_does_not_warn_measures_from_other_source(
    mock_print_warn,
):
    json_data = open_json_file(
        Path(
            "tests/unit/data/github_fga-eps-mds-2024.1-MeasureSoftGram-DOC-28-07-2024-00-00-22-extracted.metrics"
        )
    )

    calculate_measures(json_data, pre_config)

    mock_print_warn.assert_not_called()


@patch("src.cli.resources.measure.print_warn")
def test_calculate_measures_does_not_warn_measures_not_configured(mock_print_warn):
    json_data = {
        "src/a.py": [{"metric": "sqale_debt_ratio", "value": "8.3"}],
        "src/b.py": [{"metric": "sqale_debt_ratio", "value": "4.0"}],
    }

    calculate_measures(json_data)

    mock_print_warn.assert_not_called()
