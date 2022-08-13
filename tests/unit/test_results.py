from src.cli.commands import print_results, validade_analysis_response
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
        "weighted_characteristics": {
            "sqc": {
                "maintainability": 0.5,
                "reliability": 0.7142857142857143,
            }
        },
        "weighted_subcharacteristics": {
            "maintainability": {
                "modifiability": 0.5,
            },
            "reliability": {
                "testing_status": 0.7142857142857143,
            },
        },
        "weighted_measures": {
            "modifiability": {
                "m1": 0.5,
            },
            "testing_status": {
                "m1": 0.7142857142857143,
            },
        },
    }
}

ERROR_MESSAGE = {"error": "Pre-Config is not a valid ID"}


def test_print_results(mocker):

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        print_results(RESULTS)

        out = fake_out.getvalue()

        assert "The analysis was completed with Success!" in out
        assert "SQC: 0.6165241607725739" in out
        assert "maintainability = 0.5"
        assert "reliability = 0.7142857142857143" in out
        assert "modifiability = 0.5" in out
        assert "testing_status = 0.7142857142857143" in out


def test_validate_analysis_response_success(mocker):

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        validade_analysis_response(201, RESULTS)

        out = fake_out.getvalue()

        assert "The analysis was completed with Success!" in out
        assert "SQC: 0.6165241607725739" in out
        assert "maintainability = 0.5"
        assert "reliability = 0.7142857142857143" in out
        assert "modifiability = 0.5" in out
        assert "testing_status = 0.7142857142857143" in out


def test_validate_analysis_response_error(mocker):
    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        validade_analysis_response(404, ERROR_MESSAGE)

        assert "Pre-Config is not a valid ID" in fake_out.getvalue()
