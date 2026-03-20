from pathlib import Path

FILE_CONFIG = "msgram.json"
DEFAULT_CONFIG_PATH = Path.cwd() / ".msgram"
DEFAULT_RAW_DATA_PATH = Path.cwd() / "analytics-raw-data"
DEFAULT_CONFIG_FILE_PATH = DEFAULT_CONFIG_PATH / FILE_CONFIG
DIFF_FILE_CONFIG = "msgram_diff.json"

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
    {
        "team_throughput": {
            "metrics": [
                "total_issues",
                "resolved_issues",
            ],
        }
    },
    {
        "ci_feedback_time": {
            "metrics": [
                "sum_ci_feedback_times",
                "total_builds",
            ],
        }
    },
]
