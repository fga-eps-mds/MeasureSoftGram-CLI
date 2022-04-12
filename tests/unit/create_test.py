from src.cli.create import (
    validate_weight_sum,
    validate_weight_value,
    validate_check_box_input,
    define_weight,
    define_characteristic,
    define_subcharacteristics,
    define_measures,
    sublevel_cli,
)


def test_validate_weight_value():
    """
    Test for validate_weight_value function
    """
    assert validate_weight_value(0) is False
    assert validate_weight_value(50)
    assert validate_weight_value(100)
    assert validate_weight_value(-30) is False
    assert validate_weight_value(120) is False


def test_validate_weight_sum():
    """
    Test for validate_weight_value function
    """

    assert validate_weight_sum([{"reliability": "50"}, {"testability": "10"}]) is False
    assert validate_weight_sum(
        [{"maintanability": "20"}, {"reliability": "70"}, {"testability": "10"}]
    )
    assert (
        validate_weight_sum([{"maintanability": "70"}, {"testability": "40"}]) is False
    )
    assert validate_weight_sum([]) is False


def test_validate_check_box_input():
    """
    Test for validate_check_box_input function
    """
    assert validate_check_box_input(0) is False
    assert validate_check_box_input(3)


def test_define_weight(mocker):
    """
    Test for define_weight function
    """
    mocker.patch("inquirer.prompt", return_value={"usability": "50"})

    assert define_weight("usability", "Usability") == {"usability": "50"}


def test_sublevel_cli(mocker):
    """
    Test for sublevel_cli function
    """
    mocker.patch(
        "inquirer.prompt",
        return_value={
            "sublevels": [
                "Non Complex File Density",
                "Commented File Density",
            ],
        },
    )

    available_conf = {
        "non_complex_file_density": {
            "name": "Non Complex File Density",
        },
        "commented_file_density": {
            "name": "Commented File Density",
        },
        "duplication": {
            "name": "Duplication",
        },
    }

    assert sublevel_cli(
        "Modifiability",
        "measures",
        ["non_complex_file_density", "commented_file_density", "duplication"],
        available_conf,
    ) == ["non_complex_file_density", "commented_file_density"]


class TestDefineCharacteristics:
    def test_one_characteristic(self, mocker):
        """
        test for define_characteristics
        """
        mocker.patch("inquirer.prompt", return_value={"usability": "50"})

        available_conf = {"characteristics": {"usability": {"name": "Usability"}}}

        resp_user_characteristics, resp_characteristics_weights = define_characteristic(
            available_conf
        )

        assert len(resp_user_characteristics) == 1
        assert len(resp_characteristics_weights) == 1
        assert resp_user_characteristics == ["usability"]
        assert int(resp_characteristics_weights[0]["usability"]) == 100


class TestDefineSubCharacteristics:
    def test_one_sub_char(self):
        available_conf = {
            "subcharacteristics": {
                "testability": {
                    "name": "Testability",
                }
            }
        }

        u_characteristics = ["reliability"]

        resp_sub_chars, resp_sub_chars_weights = define_subcharacteristics(
            u_characteristics, available_conf
        )

        assert len(resp_sub_chars) == 1
        assert len(resp_sub_chars_weights) == 1
        assert resp_sub_chars == ["testability"]
        assert int(resp_sub_chars_weights[0]["testability"]) == 100


class TestDefineMeasures:
    def test_one_measure(self):
        available_conf = {
            "measures": {
                "non_complex_functions": {
                    "name": "Non Complex Functions",
                }
            }
        }

        u_sub_chars = ["testability"]

        resp_measures, resp_measures_weights = define_measures(
            u_sub_chars, available_conf
        )

        assert len(resp_measures) == 1
        assert len(resp_measures_weights) == 1
        assert resp_measures == ["non_complex_functions"]
        assert int(resp_measures_weights[0]["non_complex_functions"]) == 100
