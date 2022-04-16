import inquirer
from inquirer.themes import GreenPassion
from flask import request
from flask_restful import Resource
import requests
import mongoengine as me
from src.util.constants import CORE_URL

# available_entries = requests.get(
#     CORE_URL + "/available-pre-configs",
#     headers={"Accept": "application/json"},
# ).json()

pre_configs_id = requests.get(
    CORE_URL + "/pre-configs/<string:pre_config_id>",
    headers={"Accept": "application/json"},
).json()

pre_config_goals = requests.get(
    CORE_URL + "/pre-configs/<string:pre_config2>",
    headers={"Accept": "application/json"},
).json()


def search_id (pre_configs_id):
    pass
