import pytest
import json
import os

from src.cli.aggregate_metrics import should_process_github_metrics, should_process_sonar_metrics
from src.cli.aggregate_metrics import list_msgram_files, read_msgram
from src.cli.aggregate_metrics import process_github_metrics


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

with open(os.path.join(TEST_DATA_DIR, 'msgram.json'), 'r') as file:
    config = json.load(file)

with open(os.path.join(TEST_DATA_DIR, 'allmsgram.json'), 'r') as file:
    all_config = json.load(file)

with open(os.path.join(TEST_DATA_DIR, 'onlygithubmsgram.json'), 'r') as file:
    only_github_msgram = json.load(file)

@pytest.mark.parametrize("config, expected_result", [
    (config, True),
    (all_config, True),
    (only_github_msgram, False),
    ({}, False),
    ({"characteristics": []}, False),
    ({"characteristics": [{"subcharacteristics": []}]}, False),
    ({"characteristics": [{"subcharacteristics": [{"measures": []}]}]}, False),
])
def test_should_process_sonar_metrics(config, expected_result):
    result = should_process_sonar_metrics(config)
    assert result == expected_result

@pytest.mark.parametrize("config, expected_result", [
    (config, False),
    (all_config, True),
    (only_github_msgram, True),
    ({}, False),
    ({"characteristics": []}, False),
    ({"characteristics": [{"subcharacteristics": []}]}, False),
    ({"characteristics": [{"subcharacteristics": [{"measures": []}]}]}, False),
])
def test_should_process_github_metrics(config, expected_result):
    result = should_process_github_metrics(config)
    assert result == expected_result

def test_list_msgram_files():

    expected_result = ['github_nlohmann-json-19-11-2023-12-53-58-extracted.msgram','fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram']
    assert list_msgram_files(TEST_DATA_DIR) == expected_result

    folder_path = 'path/to/invalid/file.txt'
    assert list_msgram_files(folder_path) == False

    folder_path = 'nonexistent/folder'
    assert list_msgram_files(folder_path) == False

def test_read_msgram():

    file_path = TEST_DATA_DIR + '/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram'
    expected_result = {'key': 'value'}
    
    with open(file_path, 'w') as file:
        json.dump(expected_result, file)
    
    assert read_msgram(file_path) == expected_result

    directory_path = TEST_DATA_DIR
    os.makedirs(directory_path, exist_ok=True)
    assert read_msgram(directory_path) == False

    nonexistent_file_path = 'nonexistent/file.msgram'
    assert read_msgram(nonexistent_file_path) == False

def test_process_github_metrics():
    folder_path = TEST_DATA_DIR
    github_file_name = 'github_nlohmann-json-19-11-2023-12-53-58-extracted.msgram'
    github_file_path = os.path.join(folder_path, github_file_name)

    metrics = {
        "sonar": ["some_metric"],
        "github": ["resolved_issues", "total_issues"]
    }

    result = process_github_metrics(folder_path, [github_file_name], metrics)

    # Validate the result
    expected_result = (
        github_file_name,
        [
            {"metric": "resolved_issues", "value": 25},
            {"metric": "total_issues", "value": 30}
        ]
    )
    assert result == expected_result