import pytest
from io import StringIO
from src.cli import create
from src.cli.create import (
    validate_check_box_input,
    validate_weight_sum,
    validate_weight_value,
    define_weight,
    select_characteristics,
    sublevel_cli,
    input_weights,
    print_error_message,
    print_no_need_define_weights_msg,
    generic_valid_input,
    define_characteristic,
    has_one_sublevel,
    define_sublevel,
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

    assert validate_weight_sum(
        [
            {"maintanability": "33.33"},
            {"testability": "33.33"},
            {"reliability": "33.33"},
        ]
    )

    assert (
        validate_weight_sum(
            [
                {"maintanability": "37.33"},
                {"testability": "53.93"},
                {"reliability": "63.19"},
            ]
        )
        is False
    )
    assert (
        validate_weight_sum(
            [
                {"maintanability": "37.337"},
                {"testability": "13.933"},
                {"reliability": "23.195"},
            ]
        )
        is False
    )


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


@pytest.mark.parametrize(
    "value,msg,expected",
    [
        (
            False,
            "Error message 1",
            "Error message 1\n",
        ),
        (True, "Error message 2", ""),
    ],
)
def test_print_error_message(value, msg, expected, mocker):
    """
    Test for print_error_message function
    """

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        print_error_message(msg, value)
        assert fake_out.getvalue() == expected


@pytest.mark.parametrize(
    "key,value,expected",
    [
        (
            "characteristics",
            "Usability",
            "\nOnly one characteristics Usability selected, no need to define weights\n\n",
        ),
        (
            "subcharacteristics",
            "Reliability",
            "\nOnly one subcharacteristics Reliability selected, no need to define weights\n\n",
        ),
        (
            "measures",
            "Commented File Density",
            "\nOnly one measures Commented File Density selected, no need to define weights\n\n",
        ),
    ],
)
def test_print_no_need_weights(key, value, expected, mocker):
    """
    Test for print_no_need_weights function
    """

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        print_no_need_define_weights_msg(key, value)
        assert fake_out.getvalue() == expected


def test_input_weights(mocker):
    """
    Test for input_weights function
    """
    mocker.patch("src.cli.create.define_weight", return_value={"mock": "50"})

    sublevel_conf = {
        "usability": {
            "name": "Usability",
        },
        "reliability": {
            "name": "Reliability",
        },
    }

    user_sublevels = ["usability", "reliability"]

    assert input_weights(sublevel_conf, user_sublevels) == [
        {"mock": "50"},
        {"mock": "50"},
    ]


def test_select_characteristics(mocker):
    """
    Test for select_characteristics function
    """
    mocker.patch(
        "inquirer.prompt",
        return_value={"characteristics": ["Usability", "Maintainability"]},
    )

    characteristics = {
        "usability": {
            "name": "Usability",
        },
        "maintainability": {
            "name": "Maintainability",
        },
    }

    assert select_characteristics(characteristics) == ["usability", "maintainability"]


class TestGenericValidInput:
    def test_perfect_flux(self):
        """
        Test for generic_valid_select function
        """

        def validation_func(values):
            return len(values) > 0

        def body_func():
            return ["option", "option2"]

        assert generic_valid_input(validation_func, body_func, "Error message 1") == [
            "option",
            "option2",
        ]

    def test_error_flux(self):
        """
        Test for generic_valid_select function
        """

        flag = False

        def validation_func(values):
            nonlocal flag
            if not flag:
                flag = True
                return False
            return len(values) > 0

        def body_func():
            return ["option", "option2"]

        assert generic_valid_input(validation_func, body_func, "Error message 1") == [
            "option",
            "option2",
        ]


class TestHasOneSublevel:
    def test_has_one(self):
        available_conf = {
            "subcharacteristics": {
                "testability": {"name": "Testability", "measures": ["em1"]}
            }
        }

        assert (
            has_one_sublevel(
                available_conf, "subcharacteristics", "measures", "testability"
            )
            is True
        )

    def test_has_none(self):
        available_conf = {
            "subcharacteristics": {
                "testability": {"name": "Testability", "measures": []}
            }
        }

        assert (
            has_one_sublevel(
                available_conf, "subcharacteristics", "measures", "testability"
            )
            is False
        )

    def test_has_many(self):
        available_conf = {
            "subcharacteristics": {
                "testability": {"name": "Testability", "measures": ["em1", "em2"]}
            }
        }

        assert (
            has_one_sublevel(
                available_conf, "subcharacteristics", "measures", "testability"
            )
            is False
        )


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

    def test_select_only_one(self, mocker):
        """
        test for define_characteristics
        """
        mocker.patch("inquirer.prompt", return_value={"characteristics": ["Usability"]})

        available_conf = {
            "characteristics": {
                "usability": {"name": "Usability"},
                "reliability": {"name": "Reliability"},
            }
        }

        resp_user_characteristics, resp_characteristics_weights = define_characteristic(
            available_conf
        )

        assert len(resp_user_characteristics) == 1
        assert len(resp_characteristics_weights) == 1
        assert resp_user_characteristics == ["usability"]
        assert int(resp_characteristics_weights[0]["usability"]) == 100


class TestDefineSublevels:
    AVAILABLE_PRE_CONF = {
        "characteristics": {
            "reliability": {
                "name": "Reliability",
                "subcharacteristics": ["testing_status"],
            },
            "maintainability": {
                "name": "Maintainability",
                "subcharacteristics": ["modifiability"],
            },
        },
        "subcharacteristics": {
            "testing_status": {
                "name": "Testing Status",
                "measures": ["passed_tests", "test_builds", "test_coverage"],
                "characteristics": ["reliability"],
            },
            "modifiability": {
                "name": "Modifiability",
                "measures": [
                    "non_complex_file_density",
                    "commented_file_density",
                    "duplication_absense",
                ],
                "characteristics": ["maintainability"],
            },
        },
        "measures": {
            "test_builds": {
                "name": "Test Builds",
                "subcharacteristics": ["testing_status"],
                "characteristics": ["reliability"],
            },
            "test_coverage": {
                "name": "Test Coverage",
                "subcharacteristics": ["testing_status"],
                "characteristics": ["reliability"],
            },
            "non_complex_file_density": {
                "name": "Non complex file density",
                "subcharacteristics": ["modifiability"],
                "characteristics": ["maintainability"],
            },
        },
    }

    def test_one_sub_level(self):
        available_conf = {
            "subcharacteristics": {
                "testability": {
                    "name": "Testability",
                }
            }
        }

        u_characteristics = ["reliability"]

        resp_sub_chars, resp_sub_chars_weights = define_sublevel(
            u_characteristics, available_conf, "characteristics", "subcharacteristics"
        )

        assert len(resp_sub_chars) == 1
        assert len(resp_sub_chars_weights) == 1
        assert resp_sub_chars == ["testability"]
        assert int(resp_sub_chars_weights[0]["testability"]) == 100

    def test_has_one_sub_level(self, mocker):
        with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
            u_characteristics = ["maintainability", "reliability"]

            resp_sub_chars, resp_sub_chars_weights = define_sublevel(
                u_characteristics,
                self.AVAILABLE_PRE_CONF,
                "characteristics",
                "subcharacteristics",
            )

            testing_status_msg = "Only one subcharacteristics Testing Status selected, no need to define weights"
            modifiability_msg = "Only one subcharacteristics Modifiability selected, no need to define weights"

            assert modifiability_msg in fake_out.getvalue()
            assert testing_status_msg in fake_out.getvalue()
            assert resp_sub_chars == ["modifiability", "testing_status"]
            assert resp_sub_chars_weights == [
                {"modifiability": 100},
                {"testing_status": 100},
            ]

    def test_has_one_sub_sub_level(self, mocker):
        u_subcharacteristics = ["modifiability"]

        mocker.patch.object(
            create, "select_sublevels", return_value=["non_complex_file_density"]
        )

        with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
            resp_measures, resp_measures_weights = define_sublevel(
                u_subcharacteristics,
                self.AVAILABLE_PRE_CONF,
                "subcharacteristics",
                "measures",
            )

            warning_msg = "Only one measures Non complex file density selected, no need to define weights"

            assert warning_msg in fake_out.getvalue()
            assert resp_measures == ["non_complex_file_density"]
            assert resp_measures_weights == [{"non_complex_file_density": 100}]

    def test_has_more_than_one_sub_sub_level(self, mocker):
        u_subcharacteristics = ["testing_status"]

        mocker.patch.object(
            create, "select_sublevels", return_value=["test_builds", "test_coverage"]
        )
        mocker.patch.object(
            create,
            "input_weights",
            return_value=[{"test_builds": 33.5}, {"test_coverage": 66.5}],
        )

        resp_measures, resp_measures_weights = define_sublevel(
            u_subcharacteristics,
            self.AVAILABLE_PRE_CONF,
            "subcharacteristics",
            "measures",
        )

        assert resp_measures == ["test_builds", "test_coverage"]
        assert resp_measures_weights == [{"test_builds": 33.5}, {"test_coverage": 66.5}]
