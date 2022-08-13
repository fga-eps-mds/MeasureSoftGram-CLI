import pytest
import src.cli.commands as create
from src.cli.exceptions import exceptions
from tests.test_helpers import read_json


def test_pre_config_file_reader():
    available_pre_config = read_json("tests/unit/data/measuresoftgramCoreFormat.json")

    create.pre_config_file_reader(
        "tests/unit/data/measuresoftgramPreConfig.json", available_pre_config
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
    file_pre_config = read_json("tests/unit/data/measuresoftgramPreConfig.json")
    characteristics = create.read_file_characteristics(file_pre_config)

    assert characteristics == {
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
    }


def test_valid_validate_file_characteristics():
    file_pre_config = read_json("tests/unit/data/measuresoftgramPreConfig.json")
    characteristics = create.validate_file_characteristics(file_pre_config)

    assert characteristics


def test_invalid_validate_file_characteristics():

    file_characteristics_without_weights = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_characteristics_without_weights["characteristics"][0].pop("weight")

    with pytest.raises(exceptions.InvalidWeight):
        create.validate_file_characteristics(file_characteristics_without_weights)

    file_characteristics_without_name = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_characteristics_without_name["characteristics"][0].pop("name")

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_file_characteristics(file_characteristics_without_name)

    file_characteristics_without_subc = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_characteristics_without_subc["characteristics"][0].pop("subcharacteristics")

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_file_characteristics(file_characteristics_without_subc)


def test_valid_read_file_sub_characteristics():
    file_subcharacteristics = read_json("tests/unit/data/measuresoftgramPreConfig.json")
    subcharacteristics = create.read_file_sub_characteristics(file_subcharacteristics)

    assert subcharacteristics == {
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
    }


def test_valid_validate_file_sub_characteristics():
    file_subcharacteristics = read_json("tests/unit/data/measuresoftgramPreConfig.json")
    subcharacteristics = create.validate_file_sub_characteristics(
        file_subcharacteristics
    )

    assert subcharacteristics


def test_invalid_validate_file_sub_characteristics():

    file_without_name_subcharacteristics = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_without_name_subcharacteristics["characteristics"][0]["subcharacteristics"][
        0
    ].pop("name")

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_file_sub_characteristics(file_without_name_subcharacteristics)

    file_without_weight_subcharacteristics = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_without_weight_subcharacteristics["characteristics"][0]["subcharacteristics"][
        0
    ].pop("weight")

    with pytest.raises(exceptions.InvalidWeight):
        create.validate_file_sub_characteristics(file_without_weight_subcharacteristics)

    file_without_measures_subcharacteristics = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_without_measures_subcharacteristics["characteristics"][0][
        "subcharacteristics"
    ][0].pop("measures")

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_file_sub_characteristics(
            file_without_measures_subcharacteristics
        )

    file_empty_measures_subcharacteristics = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_empty_measures_subcharacteristics["characteristics"][0]["subcharacteristics"][
        0
    ]["measures"] = []

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_file_sub_characteristics(file_empty_measures_subcharacteristics)


def test_valid_read_file_measures():
    file_pre_config = read_json("tests/unit/data/measuresoftgramPreConfig.json")

    measures = create.read_file_measures(file_pre_config)

    assert measures == [
        "passed_tests",
        "test_builds",
        "test_coverage",
        "non_complex_file_density",
        "commented_file_density",
        "duplication_absense",
    ]


def test_valid_validate_file_measures():
    file_pre_config = read_json("tests/unit/data/measuresoftgramPreConfig.json")

    measures = create.validate_file_measures(file_pre_config)

    assert measures


def test_invalid_validate_file_measures():

    file_without_name_measures = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_without_name_measures["characteristics"][0]["subcharacteristics"][0][
        "measures"
    ][0].pop("name")

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_file_measures(file_without_name_measures)

    file_without_weight_measures = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_without_weight_measures["characteristics"][0]["subcharacteristics"][0][
        "measures"
    ][0].pop("weight")

    with pytest.raises(exceptions.InvalidWeight):
        create.validate_file_measures(file_without_weight_measures)

    file_invalid_weight_measures = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_invalid_weight_measures["characteristics"][0]["subcharacteristics"][0][
        "measures"
    ][0]["weight"] = 120

    with pytest.raises(exceptions.InvalidWeight):
        create.validate_file_measures(file_invalid_weight_measures)

    file_invalid_weight_sum_measures = read_json(
        "tests/unit/data/measuresoftgramPreConfig.json"
    )
    file_invalid_weight_sum_measures["characteristics"][0]["subcharacteristics"][0][
        "measures"
    ][0]["weight"] = 10

    with pytest.raises(exceptions.InvalidWeight):
        create.validate_file_measures(file_invalid_weight_sum_measures)


def test_valid_validate_core_available():
    file_pre_config = read_json("tests/unit/data/measuresoftgramPreConfig.json")

    available_pre_configs = read_json("tests/unit/data/measuresoftgramCoreFormat.json")
    file_characteristics = create.read_file_characteristics(file_pre_config)
    file_subcharacteristics = create.read_file_sub_characteristics(file_pre_config)

    assert create.validate_core_available(
        available_pre_configs, file_characteristics, file_subcharacteristics
    )


def test_invalid_validate_core_available():

    available_pre_configs = read_json("tests/unit/data/measuresoftgramCoreFormat.json")
    file_wrong_characteristics = {
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
        file_wrong_characteristics.keys()
    )

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_core_available(
            available_pre_configs, file_wrong_characteristics, file_subcharacteristics
        )

    file_characteristics_wrong_subcharacteristics = {
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

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_core_available(
            available_pre_configs,
            file_characteristics_wrong_subcharacteristics,
            file_subcharacteristics,
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
    file_subcharacteristics_wrong_measures = {
        "testing_status": {
            "weights": {"passed_tests": 100.0},
            "measures": ["non_complex_file_density"],
        },
        "modifiability": {
            "weights": {"non_complex_file_density": 100.0},
            "measures": ["passed_tests"],
        },
    }

    with pytest.raises(exceptions.UnableToReadFile):
        create.validate_core_available(
            available_pre_configs,
            file_characteristics,
            file_subcharacteristics_wrong_measures,
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


def test_check_in_keys():
    key_for_check = "name"
    keys = ["weight", "subcharacteristics"]
    exception = exceptions.UnableToReadFile
    exception_description = "teste"

    with pytest.raises(exceptions.UnableToReadFile):
        create.check_in_keys(key_for_check, keys, exception, exception_description)

    keys = ["name", "weight", "subcharacteristics"]

    assert create.check_in_keys(key_for_check, keys, exception, exception_description)


def test_validate_weight_parameter():
    weight = 120
    exception = exceptions.InvalidWeight
    exception_description = "teste"

    with pytest.raises(exceptions.InvalidWeight):
        create.validate_weight_parameter(weight, exception, exception_description)

    weight = 90

    assert create.validate_weight_parameter


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
    assert validate is True

    sum_weights = 99

    validate = create.validate_sum_of_weights(sum_weights)
    assert validate is False
