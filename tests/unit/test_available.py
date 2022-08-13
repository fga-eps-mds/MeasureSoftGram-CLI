from src.cli.commands import parse_available
from io import StringIO


mocked_available = {
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
        "passed_tests": {
            "name": "Passed Tests",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
            "metrics": ["test_success_density"],
        },
        "test_builds": {
            "name": "Test Builds",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
            "metrics": ["tests", "test_execution_time"],
        },
        "test_coverage": {
            "name": "Test Coverage",
            "subcharacteristics": ["testing_status"],
            "characteristics": ["reliability"],
            "metrics": ["coverage"],
        },
        "non_complex_file_density": {
            "name": "Non complex file density",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["complexity", "functions"],
        },
        "commented_file_density": {
            "name": "Commented file density",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["comment_lines_density"],
        },
        "duplication_absense": {
            "name": "Duplication abscense",
            "subcharacteristics": ["modifiability"],
            "characteristics": ["maintainability"],
            "metrics": ["duplicated_lines_density"],
        },
    },
}


class DummyResponse:
    def __init__(self, status_code, mocked_data):
        self.status_code = status_code
        self.res = mocked_data

    def json(self):
        return self.res


# @mock.patch('requests.get', return_value=DummyResponse(200, mocked_available))
def test_parse_available(mocker):

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        mocker.patch(
            "requests.get",
            return_value=DummyResponse(200, mocked_available)
        )
        parse_available()

        expected_lines = [
            "These are all items available in the MeasureSoftGram database in the following order:",
            "Characteristics -> Subcharacteristics -> Measures -> Necessary Metrics",
            "You can use these items to create a pre configuration",
            "Maintainability:",
            "Modifiability:",
            "Commented file density:",
            "comment_lines_density",
            "Duplication abscense:",
            "duplicated_lines_density",
            "Non complex file density:",
            "complexity, functions",
            "Reliability:",
            "Testing Status:",
            "Passed Tests:",
            "test_success_density",
            "Test Builds:",
            "tests, test_execution_time",
            "Test Coverage:",
            "coverage",
        ]

        for line in expected_lines:
            assert line in fake_out.getvalue()
