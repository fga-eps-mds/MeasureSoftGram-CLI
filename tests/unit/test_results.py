from src.cli.results import truncate, print_results, validade_analysis_response
import pytest
from io import StringIO


class TestResponseCreated:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json():
        return {
            "analysis": {
                "sqc": {"sqc": 0.6165241607725739},
                "subcharacteristics": {
                    "modifiability": 0.5,
                    "testing_status": 0.7142857142857143,
                },
                "characteristics": {
                    "maintainability": 0.5,
                    "reliability": 0.7142857142857143,
                },
            }
        }


class TestResponseError:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json():
        return {}


def test_truncate():
    assert truncate(1237.1283919, 2) == 1237.12


def test_print_results(mocker):

    test_response = TestResponseCreated

    test_analysis_values = test_response.json()

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        print_results(test_analysis_values)

        assert (
            "\nThe analysis was completed with Success!"
            + "\n\nHere are the Results:\n\nSQC:\n61.65%\n\nCharacteristics"
            + ":\nmaintainability = 50.0%\nreliability = 71.42%\n"
            + "\nSubcharacteristics:\nmodifiability = 50.0%"
            + "\ntesting_status = 71.42%\n"
            in fake_out.getvalue()
        )
