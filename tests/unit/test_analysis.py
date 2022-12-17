from io import StringIO

from src.cli.commands.parse_analysis import parse_analysis, results


class DummyResponse:
    def __init__(self, status_code, mocked_data):
        self.status_code = status_code
        self.res = mocked_data

    def json(self):
        return self.res


def test_parse_analysis(mocker):
    mocked_analysis = {
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

    mocker.patch("requests.post", return_value=DummyResponse(200, mocked_analysis))

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_analysis.parse_analysis("abcd")

        expected_lines = [
            "The analysis was completed with Success!",
            "Here are the Results:",
            "SQC: 0.6165241607725739",
            "Characteristics before weighting:",
            "maintainability = 0.5",
            "reliability = 0.7142857142857143",
            "modifiability = 0.5",
            "testing_status = 0.7142857142857143",
        ]

        out = fake_out.getvalue()
        print(out)

        for line in expected_lines:
            assert line in out


def test_to_zero_one_decimal():
    assert results.to_zero_one_decimal(0.0) is None
    assert results.to_zero_one_decimal(1) is None
    assert results.to_zero_one_decimal(2) == 0.02


def test_validade_analysis_response_error(mocker):
    mocker.patch("requests.post", return_value=DummyResponse(400, {}))

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        parse_analysis.parse_analysis("abcd")

        out = fake_out.getvalue()
        print(out)

        assert "Error while making analysis" in out
