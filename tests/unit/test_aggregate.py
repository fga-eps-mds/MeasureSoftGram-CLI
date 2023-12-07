import pytest
import json
import os
import tempfile

from src.cli.aggregate_metrics import (
    should_process_github_metrics,
    should_process_sonar_metrics,
)
from src.cli.aggregate_metrics import read_msgram, save_metrics
from src.cli.aggregate_metrics import (
    process_github_metrics,
    process_sonar_metrics,
    aggregate_metrics,
)


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(TEST_DATA_DIR, "msgram.json"), "r") as file:
    config = json.load(file)

with open(os.path.join(TEST_DATA_DIR, "allmsgram.json"), "r") as file:
    all_config = json.load(file)

with open(os.path.join(TEST_DATA_DIR, "onlygithubmsgram.json"), "r") as file:
    only_github_msgram = json.load(file)


@pytest.mark.parametrize(
    "config, expected_result",
    [
        (config, True),
        (all_config, True),
        (only_github_msgram, False),
        ({}, False),
        ({"characteristics": []}, False),
        ({"characteristics": [{"subcharacteristics": []}]}, False),
        ({"characteristics": [{"subcharacteristics": [{"measures": []}]}]}, False),
    ],
)
def test_should_process_sonar_metrics(config, expected_result):
    result = should_process_sonar_metrics(config)
    assert result == expected_result


@pytest.mark.parametrize(
    "config, expected_result",
    [
        (config, False),
        (all_config, True),
        (only_github_msgram, True),
        ({}, False),
        ({"characteristics": []}, False),
        ({"characteristics": [{"subcharacteristics": []}]}, False),
        ({"characteristics": [{"subcharacteristics": [{"measures": []}]}]}, False),
    ],
)
def test_should_process_github_metrics(config, expected_result):
    result = should_process_github_metrics(config)
    assert result == expected_result


def test_read_msgram():
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "test_file.msgram")
        expected_result = {"key": "value"}

        # Write the expected content to the temporary file
        with open(file_path, "w") as file:
            json.dump(expected_result, file)

        # Test reading from the temporary file
        assert read_msgram(file_path) == expected_result

        # Test reading from a directory (should return False)
        assert read_msgram(temp_dir) is False

        # Test reading from a nonexistent file (should return False)
        nonexistent_file_path = os.path.join(temp_dir, "nonexistent_file.msgram")
        assert read_msgram(nonexistent_file_path) is False


def test_process_github_metrics():
    result = process_github_metrics(TEST_DATA_DIR, [], {"sonar": [], "github": []})
    assert result is False

    folder_path = TEST_DATA_DIR
    github_file_name = "github_nlohmann-json-19-11-2023-12-53-58-extracted.msgram"

    metrics = {"sonar": ["some_metric"], "github": ["resolved_issues", "total_issues"]}

    result = process_github_metrics(folder_path, [github_file_name], metrics)

    # Validate the result
    expected_result = (
        github_file_name,
        [
            {"metric": "resolved_issues", "value": 25},
            {"metric": "total_issues", "value": 30},
        ],
    )
    assert result == expected_result


def test_process_sonar_metrics():
    with tempfile.TemporaryDirectory() as temp_dir:
        sonar_file_name = "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram"
        sonar_file_path = os.path.join(temp_dir, sonar_file_name)

        github_file_name = "github_nlohmann-json-19-11-2023-12-53-58-extracted.msgram"
        github_file_path = os.path.join(temp_dir, github_file_name)

        sonar_data = {"sonar_metric": 42}
        github_data = {"github_metrics": [{"metric": "resolved_issues", "value": 25}]}

        with open(sonar_file_path, "w") as sonar_file:
            json.dump(sonar_data, sonar_file)

        with open(github_file_path, "w") as github_file:
            json.dump(github_data, github_file)

        result = process_sonar_metrics(temp_dir, [sonar_file_name], [github_file_name])
        expected_result = [(sonar_file_name, sonar_data)]
        assert result == expected_result

        assert os.path.exists(sonar_file_path)
        assert os.path.exists(github_file_path)


def test_save_metrics():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = os.path.join(temp_dir, "test_file.msgram")
        metrics = {"metric1": 10, "metric2": 20}

        save_metrics(file_name, metrics)

        output_file_path = os.path.join(temp_dir, "test_file.metrics")
        assert os.path.exists(output_file_path)

        with open(output_file_path, "r") as output_file:
            saved_metrics = json.load(output_file)

        assert saved_metrics == metrics


def test_aggregate_metrics():
    with tempfile.TemporaryDirectory() as temp_dir:
        folder_path = temp_dir

        msgram_file1 = os.path.join(folder_path, "file1.msgram")
        msgram_file2 = os.path.join(folder_path, "github_file.msgram")

        with open(msgram_file1, "w") as file:
            json.dump({"some_metric": 42}, file)

        with open(msgram_file2, "w") as file:
            json.dump(
                {
                    "github_metrics": [
                        {"metric": "resolved_issues", "value": 25},
                        {"metric": "total_issues", "value": None},
                    ]
                },
                file,
            )

        result = aggregate_metrics(folder_path, all_config)

        assert result is True

        output_file_path = os.path.join(folder_path, "file1.metrics")
        assert os.path.exists(output_file_path)

        with open(output_file_path, "r") as output_file:
            saved_metrics = json.load(output_file)

        expected_metrics = {
            "some_metric": 42,
            "github_metrics": [
                {"metric": "resolved_issues", "value": 25},
                {"metric": "total_issues", "value": None},
                {"metric": "sum_ci_feedback_times", "value": None},
                {"metric": "total_builds", "value": None},
            ],
        }
        assert saved_metrics == expected_metrics
