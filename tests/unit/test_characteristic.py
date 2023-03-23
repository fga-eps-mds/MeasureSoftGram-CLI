from pathlib import Path

from src.cli.resources.characteristic import calculate_characteristics
from src.cli.jsonReader import open_json_file


def test_calculate_characteristics():
    config = open_json_file(Path('tests/unit/data/msgram.json'))
    subcharacteristics = [
        {'key': 'testing_status', 'value': 0.8633460569923477},
        {'key': 'modifiability', 'value': 0.650528195701257}
    ]

    infos, headers = calculate_characteristics(config, subcharacteristics)

    assert headers == ["Id", "Name", "Description", "Value", "Created at"]
    assert infos == {'characteristics': [
        {'key': 'reliability', 'value': 0.8633460569923477},
        {'key': 'maintainability', 'value': 0.650528195701257}
    ]}
