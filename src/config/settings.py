from pathlib import Path

FILE_CONFIG = "msgram.json"
DEFAULT_CONFIG_PATH = Path.cwd() / ".msgram"
DEFAULT_CONFIG_FILE_PATH = DEFAULT_CONFIG_PATH / FILE_CONFIG

AVAILABLE_GEN_FORMATS = ["csv", "json", "tabular", "raw", "tree"]

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
        "technical_debt_ratio": {
            "metrics": [
                "sqale_debt_ratio",
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
