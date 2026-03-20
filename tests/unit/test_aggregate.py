import pytest
import json
import os
import tempfile

from src.cli.aggregate_metrics import (
    should_process_metrics,
)
from src.cli.aggregate_metrics import read_msgram, save_metrics
from src.cli.aggregate_metrics import (
    process_metrics,
    aggregate_metrics,
)


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(TEST_DATA_DIR, "msgram.json"), "r") as file:
    config = json.load(file)

with open(os.path.join(TEST_DATA_DIR, "onlysonarmsgram.json"), "r") as file:
    only_sonar_msgram = json.load(file)

with open(os.path.join(TEST_DATA_DIR, "onlygithubmsgram.json"), "r") as file:
    only_github_msgram = json.load(file)


@pytest.mark.parametrize(
    "config, expected_result",
    [
        (config, True),
        (only_sonar_msgram, True),
        (only_github_msgram, True),
    ],
)
def test_should_process_metrics(config, expected_result):
    result = should_process_metrics(config)
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


@pytest.mark.parametrize(
    "input_format, expected_result",
    [("github", True), ("sonar", True)],
)
def test_process_metrics(input_format, expected_result):
    with tempfile.TemporaryDirectory() as temp_dir:
        if input_format == "github":
            file_name = "github_nlohmann-json-19-11-2023-12-53-58-extracted.msgram"
            file_path = os.path.join(temp_dir, file_name)
            data = {"github_metrics": [{"metric": "resolved_issues", "value": 25}]}
        else:
            file_name = "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram"
            file_path = os.path.join(temp_dir, file_name)
            data = {"sonar_metric": 42}

        with open(file_path, "w") as sonar_file:
            json.dump(data, sonar_file)

        result = process_metrics(temp_dir, [file_name])
        expected_result = [(file_name, data)]

        assert result == expected_result

        assert os.path.exists(file_path)


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


@pytest.mark.parametrize(
    "input_format, expected_result",
    [
        (
            "github",
            {
                "github_metrics": [
                    {"metric": "resolved_issues", "value": 6.0},
                    {"metric": "total_issues", "value": 1.0},
                    {"metric": "sum_ci_feedback_times", "value": 925.0},
                    {"metric": "total_builds", "value": 30.0},
                ]
            },
        ),
        ("sonar", {"some_metric": 42}),
    ],
)
def test_aggregate_metrics(input_format, expected_result):
    with tempfile.TemporaryDirectory() as temp_dir:
        folder_path = temp_dir

        if input_format == "github":
            msgram_file = os.path.join(
                folder_path,
                "github_fga-eps-mds-2024.1-MeasureSoftGram-DOC-28-07-2024-00-00-22-extracted.msgram",
            )
            with open(msgram_file, "w") as file:
                json.dump(
                    {
                        "github_metrics": [
                            {"metric": "resolved_issues", "value": 6.0},
                            {"metric": "total_issues", "value": 1.0},
                            {"metric": "sum_ci_feedback_times", "value": 925.0},
                            {"metric": "total_builds", "value": 30.0},
                        ]
                    },
                    file,
                )
        else:
            msgram_file = os.path.join(
                folder_path,
                "fga-eps-mds-2023-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram",
            )
            with open(msgram_file, "w") as file:
                json.dump({"some_metric": 42}, file)

        result = aggregate_metrics(input_format, folder_path, config)

        assert result is True

        output_file_path = os.path.join(
            folder_path,
            (
                "github_fga-eps-mds-2024.1-MeasureSoftGram-DOC-28-07-2024-00-00-22-extracted.metrics"
                if input_format == "github"
                else "fga-eps-mds-2023-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.metrics"
            ),
        )

        assert os.path.exists(output_file_path)

        with open(output_file_path, "r") as output_file:
            saved_metrics = json.load(output_file)

        assert saved_metrics == expected_result
