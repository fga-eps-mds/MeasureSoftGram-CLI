import pytest
from src.cli import create, exceptions
from tests.test_helpers import read_json


def test_pre_config_file_reader():
    available_preconfig = read_json("tests/unit/data/measuresoftgramFormat.json")

    create.preconfig_file_reader(
        "tests/unit/data/measuresoftgramPreconfig.json", available_preconfig
    )

    assert {
        "characteristics": {
            "reliability": {
                "weight": 50.0,
                "subcharacteristics": ["testing_status"],
                "weights": {"testing_status": 100.0},
            },
            "maintainability": {
                "weight": 50.0,
                "subcharacteristics": ["modifiability"],
                "weights": {"modifiability": 100.0},
            },
        },
        "subcharacteristics": {
            "testing_status": {
                "weights": {
                    "passed_tests": 33.33,
                    "test_builds": 33.33,
                    "test_coverage": 33.33,
                },
                "measures": ["passed_tests", "test_builds", "test_coverage"],
            },
            "modifiability": {
                "weights": {
                    "non_complex_file_density": 50.0,
                    "commented_file_density": 30.0,
                    "duplication_absense": 20.0,
                },
                "measures": [
                    "non_complex_file_density",
                    "commented_file_density",
                    "duplication_absense",
                ],
            },
        },
        "measures": [
            "passed_tests",
            "test_builds",
            "test_coverage",
            "non_complex_file_density",
            "commented_file_density",
            "duplication_absense",
        ],
    }


def test_valid_read_file_characteristics():
    file_characteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 100.0},
                            {"name": "test_builds", "weight": 100.0},
                            {"name": "test_coverage", "weight": 100.0},
                        ],
                    }
                ],
            }
        ]
    }
    characteristics = create.read_file_characteristics(file_characteristics)

    assert characteristics == {
        "Reliability": {
            "weight": 100.0,
            "subcharacteristics": ["Testing_status"],
            "weights": {"Testing_status": 100.0},
        }
    }


def test_valid_validate_file_characteristics():
    file_characteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 100.0},
                            {"name": "test_builds", "weight": 100.0},
                            {"name": "test_coverage", "weight": 100.0},
                        ],
                    }
                ],
            }
        ]
    }
    characteristics = create.validate_file_characteristics(file_characteristics)

    assert characteristics


def test_invalid_validate_file_characteristics():

    file_characteristics_without_weights = {
        "characteristics": [
            {
                "name": "Reliability",
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 100.0},
                            {"name": "test_builds", "weight": 100.0},
                            {"name": "test_coverage", "weight": 100.0},
                        ],
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidCharacteristic):
        create.validate_file_characteristics(file_characteristics_without_weights)

    file_characteristics_without_name = {
        "characteristics": [
            {
                "weight": 50,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 100.0},
                            {"name": "test_builds", "weight": 100.0},
                            {"name": "test_coverage", "weight": 100.0},
                        ],
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidCharacteristic):
        create.validate_file_characteristics(file_characteristics_without_name)

    file_characteristics_without_subc = {
        "characteristics": [
            {"name": "Reliability", "weight": 50, "subcharacteristics": []}
        ]
    }

    with pytest.raises(exceptions.InvalidCharacteristic):
        create.validate_file_characteristics(file_characteristics_without_subc)


def test_valid_read_file_sub_characteristics():
    file_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 40.0},
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }
    subcharacteristics = create.read_file_sub_characteristics(file_subcharacteristics)

    assert subcharacteristics == {
        "Testing_status": {
            "weights": {
                "passed_tests": 40.0,
                "test_builds": 30.0,
                "test_coverage": 30.0,
            },
            "measures": ["passed_tests", "test_builds", "test_coverage"],
        }
    }


def test_valid_validate_file_sub_characteristics():
    file_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 40.0},
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }
    subcharacteristics = create.validate_file_sub_characteristics(
        file_subcharacteristics
    )

    assert subcharacteristics


def test_invalid_validate_file_sub_characteristics():
    file_without_name_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "weight": 30.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 40.0},
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        create.validate_file_sub_characteristics(file_without_name_subcharacteristics)

    file_without_weight_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "measures": [
                            {"name": "passed_tests", "weight": 40.0},
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        create.validate_file_sub_characteristics(file_without_weight_subcharacteristics)

    file_without_measures_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        create.validate_file_sub_characteristics(
            file_without_measures_subcharacteristics
        )

    file_empty_measures_subcharacteristics = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {"name": "Testing_status", "weight": 30.0, "measures": []}
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        create.validate_file_sub_characteristics(file_empty_measures_subcharacteristics)


def test_valid_read_file_measures():
    file_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 100.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 100.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 40.0},
                            {"name": "test_builds", "weight": 20.0},
                            {"name": "test_coverage", "weight": 40.0},
                        ],
                    }
                ],
            }
        ]
    }

    measures = create.read_file_measures(file_measures)

    assert measures == ["passed_tests", "test_builds", "test_coverage"]


def test_valid_validate_file_measures():
    file_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 40.0},
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }

    measures = create.validate_file_measures(file_measures)

    assert measures


def test_invalid_validate_file_measures():
    file_without_name_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {"weight": 40.0},
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidMeasure):
        create.validate_file_measures(file_without_name_measures)

    file_without_weigth_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {
                                "name": "passed_tests",
                            },
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidMeasure):
        create.validate_file_measures(file_without_weigth_measures)

    file_invalid_weight_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 120.0},
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidMeasure):
        create.validate_file_measures(file_invalid_weight_measures)

    file_invalid_weight_sum_measures = {
        "characteristics": [
            {
                "name": "Reliability",
                "weight": 25.0,
                "subcharacteristics": [
                    {
                        "name": "Testing_status",
                        "weight": 30.0,
                        "measures": [
                            {"name": "passed_tests", "weight": 10.0},
                            {"name": "test_builds", "weight": 30.0},
                            {"name": "test_coverage", "weight": 30.0},
                        ],
                    }
                ],
            }
        ]
    }

    with pytest.raises(exceptions.InvalidMeasure):
        create.validate_file_measures(file_invalid_weight_sum_measures)


def test_valid_validate_core_available():

    available_pre_configs = read_json("tests/unit/data/measuresoftgramFormat.json")
    file_characteristics = {
        "reliability": {
            "name": "Reliability",
            "subcharacteristics": ["testing_status"],
        },
        "maintainability": {
            "name": "Maintainability",
            "subcharacteristics": ["modifiability"],
        },
    }
    file_subcharacteristics = {
        "testing_status": {
            "name": "Testing Status",
            "measures": ["passed_tests", "test_builds", "test_coverage"],
            "characteristics": ["reliability"],
        },
    }

    assert create.validate_core_available(
        available_pre_configs, file_characteristics, file_subcharacteristics
    )


def test_invalid_validate_core_available():

    available_pre_configs = read_json("tests/unit/data/measuresoftgramFormat.json")
    file_characteristics = {
        "usability": {
            "weight": 50,
            "subcharacteristics": ["testing_status"],
            "weights": {"testing_status": 100.0},
        },
        "maintainability": {
            "weight": 50,
            "subcharacteristics": ["modifiability"],
            "weights": {"modifiability": 100.0},
        },
    }
    file_subcharacteristics = (
        {
            "testing_status": {
                "weights": {"passed_tests": 100.0},
                "measures": ["passed_tests"],
            },
            "modifiability": {
                "weights": {"non_complex_file_density": 100.0},
                "measures": ["non_complex_file_density"],
            },
        },
    )

    assert list(available_pre_configs["characteristics"].keys()) != list(
        file_characteristics.keys()
    )

    with pytest.raises(exceptions.InvalidCharacteristic):
        create.validate_core_available(
            available_pre_configs, file_characteristics, file_subcharacteristics
        )

    file_characteristics = {
        "reliability": {
            "weight": 50,
            "subcharacteristics": ["modifiability"],
            "weights": {"testing_status": 100.0},
        },
        "maintainability": {
            "weight": 50,
            "subcharacteristics": ["modifiability"],
            "weights": {"modifiability": 100.0},
        },
    }
    file_subcharacteristics = {
        "testing_status": {
            "weights": {"passed_tests": 100.0},
            "measures": ["passed_tests"],
        },
        "modifiability": {
            "weights": {"non_complex_file_density": 100.0},
            "measures": ["non_complex_file_density"],
        },
    }

    with pytest.raises(exceptions.InvalidSubcharacteristic):
        create.validate_core_available(
            available_pre_configs, file_characteristics, file_subcharacteristics
        )

    file_characteristics = {
        "reliability": {
            "weight": 50,
            "subcharacteristics": ["testing_status"],
            "weights": {"testing_status": 100.0},
        },
        "maintainability": {
            "weight": 50,
            "subcharacteristics": ["modifiability"],
            "weights": {"modifiability": 100.0},
        },
    }
    file_subcharacteristics = {
        "testing_status": {
            "weights": {"passed_tests": 100.0},
            "measures": ["non_complex_file_density"],
        },
        "modifiability": {
            "weights": {"non_complex_file_density": 100.0},
            "measures": ["passed_tests"],
        },
    }

    with pytest.raises(exceptions.InvalidMeasure):
        create.validate_core_available(
            available_pre_configs, file_characteristics, file_subcharacteristics
        )


def test_validate_weight_value():
    """
    Test for validate_weight_value function
    """
    assert create.validate_weight_value(0) is False
    assert create.validate_weight_value(50)
    assert create.validate_weight_value(100)
    assert create.validate_weight_value(-30) is False
    assert create.validate_weight_value(120) is False


def test_round_of_sum_weights():
    sum_weights = 99.99

    sum_weights = create.round_sum_of_weights(sum_weights)
    assert sum_weights == 100


def test_validate_sum_of_weights():
    sum_weights = 100

    validate = create.validate_sum_of_weights(sum_weights)
    assert validate is True

    sum_weights = 99.99

    validate = create.validate_sum_of_weights(sum_weights)
    assert validate is False
