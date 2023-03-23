from pathlib import Path

from src.cli.resources.measure import calculate_measures
from src.cli.jsonReader import open_json_file


def test_calculate_measures():
    json_data = open_json_file(Path(
        'tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.msgram'))

    infos, headers = calculate_measures(json_data)

    assert headers == ["Id", "Name", "Description", "Value", "Created at"]
    assert infos == {'measures': [
        {'key': 'passed_tests', 'value': 1.0},
        {'key': 'test_builds', 'value': 0.9999969696180555},
        {'key': 'test_coverage', 'value': 0.5153846153846154},
        {'key': 'non_complex_file_density', 'value': 0.4829268292682926},
        {'key': 'commented_file_density', 'value': 0.029230769230769227},
        {'key': 'duplication_absense', 'value': 1.0}
    ]}
