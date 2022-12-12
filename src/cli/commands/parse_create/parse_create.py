import json
import os

import requests

from src.cli.commands.parse_create.utils import (
    pre_config_file_reader,
    validate_pre_config_post,
)
from src.cli.exceptions.exceptions import MeasureSoftGramCLIException

BASE_URL = os.getenv("BASE_URL")


def parse_create(file_path):
    available_pre_config = requests.get(
        f"{BASE_URL}available-pre-configs", headers={"Accept": "application/json"}
    ).json()

    try:
        pre_config = pre_config_file_reader(file_path, available_pre_config)
    except MeasureSoftGramCLIException as error:
        print("Error: ", error)
        return

    response = requests.post(f"{BASE_URL}pre-configs", json=pre_config)

    saved_pre_config = json.loads(response.text)

    validate_pre_config_post(response.status_code, saved_pre_config)
