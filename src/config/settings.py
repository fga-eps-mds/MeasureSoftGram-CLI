from pathlib import Path

FILE_CONFIG = "msgram.json"
DEFAULT_CONFIG_PATH = Path.cwd() / ".msgram"
DEFAULT_RAW_DATA_PATH = Path.cwd() / "analytics-raw-data"
DEFAULT_CONFIG_FILE_PATH = DEFAULT_CONFIG_PATH / FILE_CONFIG

AVAILABLE_ENTITIES = [
    "metrics",
    "measures",
    "subcharacteristics",
    "characteristics",
    "tsqmi",
]

SUPPORTED_FORMATS = [
    "json",
    "tabular",
]

AVAILABLE_IMPORTS = ["sonarqube", "github"]

AVAILABLE_GEN_FORMATS = ["csv", "json"]

SUPPORTED_MEASURES = [
    {
        "passed_tests": {
            "metrics": [
                "tests",
                "test_failures",
                "test_errors",
            ],
        }
    },
    {
        "test_builds": {
            "metrics": [
                "test_execution_time",
                "tests",
            ],
        }
    },
    {
        "test_coverage": {
            "metrics": [
                "coverage",
            ],
        }
    },
    {
        "non_complex_file_density": {
            "metrics": [
                "functions",
                "complexity",
            ],
        }
    },
    {
        "commented_file_density": {
            "metrics": [
                "comment_lines_density",
            ],
        }
    },
    {
        "duplication_absense": {
            "metrics": [
                "duplicated_lines_density",
            ],
        }
    },
    # {
    #     "ci_feedback_time": {
    #         "metrics": [
    #             "number_of_build_pipelines_in_the_last_x_days",
    #             "runtime_sum_of_build_pipelines_in_the_last_x_days",
    #         ],
    #     }
    # },
    # {
    #     "team_throughput": {
    #         "metrics": [
    #             "number_of_resolved_issues_with_US_label_in_the_last_x_days",
    #             "total_number_of_issues_with_US_label_in_the_last_x_days",
    #         ],
    #     }
    # },
]
