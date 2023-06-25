from pathlib import Path

from src.cli.resources.tsqmi import calculate_tsqmi
from src.cli.jsonReader import open_json_file


def test_calculate_tsqmi():
    config = open_json_file(Path("tests/unit/data/msgram.json"))
    characteristics = [
        {"key": "reliability", "value": 0.8633460569923477},
        {"key": "maintainability", "value": 0.650528195701257},
    ]

    infos, headers = calculate_tsqmi(config, characteristics)

    assert headers == ["Id", "Value", "Created at"]
    assert infos == {"tsqmi": [{"key": "tsqmi", "value": 0.7643799276297641}]}
