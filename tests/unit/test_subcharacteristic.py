from pathlib import Path

from src.cli.resources.subcharacteristic import calculate_subcharacteristics
from src.cli.jsonReader import open_json_file


def test_calculate_subcharacteristics():
    config = open_json_file(Path('tests/unit/data/msgram.json'))
    measures = [
        {'key': 'passed_tests', 'value': 1.0},
        {'key': 'test_builds', 'value': 0.9999969696180555},
        {'key': 'test_coverage', 'value': 0.5153846153846154},
        {'key': 'non_complex_file_density', 'value': 0.4829268292682926},
        {'key': 'commented_file_density', 'value': 0.029230769230769227},
        {'key': 'duplication_absense', 'value': 1.0}
    ]

    infos, headers = calculate_subcharacteristics(config, measures)

    assert headers == ["Id", "Name", "Description", "Value", "Created at"]
    assert infos == {'subcharacteristics': [
        {'key': 'testing_status', 'value': 0.8633460569923477},
        {'key': 'modifiability', 'value': 0.650528195701257}
    ]}
