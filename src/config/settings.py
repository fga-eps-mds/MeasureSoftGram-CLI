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
    "sqc"
]

SUPPORTED_FORMATS = [
    "json",
    "tabular",
]

AVAILABLE_IMPORTS = ["sonarqube"]

AVAILABLE_GEN_FORMATS = ["csv", "json"]
