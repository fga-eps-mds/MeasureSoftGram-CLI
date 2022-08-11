import os

SERVICE_URL = os.getenv("SERVICE_URL", "https://measuresoftgram-service.herokuapp.com/")

BASE_URL = "http://172.20.0.2:5000/"

AVAILABLE_ENTITIES = [
    "metrics",
    "measures",
    "subcharacteristics",
    "characteristics",
    # "sqc",
]

SUPPORTED_FORMATS = [
    "json",
    "tabular",
]

AVAILABLE_IMPORTS = [
    "sonarqube"
]
