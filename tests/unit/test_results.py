from src.cli.results import truncate, print_results, validade_analysis_response
from io import StringIO


RESULTS = {
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

ERROR_MESSAGE = {"error": "Pre-Config is not a valid ID"}


def test_truncate():
    assert truncate(1237.1283919, 2) == 1237.12


def test_print_results(mocker):

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        print_results(RESULTS)

        assert (
            "\nThe analysis was completed with Success!"
            + "\n\nHere are the Results:\n\nSQC:\n61.65%\n\nCharacteristics"
            + ":\nmaintainability = 50.0%\nreliability = 71.42%\n"
            + "\nSubcharacteristics:\nmodifiability = 50.0%"
            + "\ntesting_status = 71.42%\n"
            in fake_out.getvalue()
        )


def test_validate_analysis_response_success(mocker):

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        validade_analysis_response(201, RESULTS)

        assert (
            "\nThe analysis was completed with Success!"
            + "\n\nHere are the Results:\n\nSQC:\n61.65%\n\nCharacteristics"
            + ":\nmaintainability = 50.0%\nreliability = 71.42%\n"
            + "\nSubcharacteristics:\nmodifiability = 50.0%"
            + "\ntesting_status = 71.42%\n"
            in fake_out.getvalue()
        )


def test_validate_analysis_response_error(mocker):
    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        validade_analysis_response(404, ERROR_MESSAGE)

        assert "Pre-Config is not a valid ID" in fake_out.getvalue()
