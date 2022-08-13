import json
import requests

from src.cli.exceptions.exceptions import MeasureSoftGramCLIException
from src.cli.commands.parse_create.utils import (
    validate_pre_config_post,
    pre_config_file_reader
)
from src.config.settings import BASE_URL


def parse_create(file_path):
    available_pre_config = requests.get(
        BASE_URL + "available-pre-configs",
        headers={"Accept": "application/json"}
    ).json()

    try:
        pre_config = pre_config_file_reader(
            r"{}".format(file_path),
            available_pre_config,
        )
    except MeasureSoftGramCLIException as error:
        print("Error: ", error)
        return

    response = requests.post(BASE_URL + "pre-configs", json=pre_config)

    saved_pre_config = json.loads(response.text)

    validate_pre_config_post(response.status_code, saved_pre_config)
