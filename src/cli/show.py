import inquirer
from inquirer.themes import GreenPassion
from flask import request
from flask_restful import Resource
import requests
import mongoengine as me
from src.cli.cliRunner import BASE_URL
import argparse

pre_configs_id = requests.get(
    BASE_URL + "/pre-configs/<string:pre_config_id>",
    headers={"Accept": "application/json"},
).json()

pre_configs = requests.get()

list = argparse.ArgumentParser()
list.add_argument("list", help="list all pre configurations presents.", type=dict)
args = list.parse_args()
# my_list = [int(pre_configs_id) for pre_configs_id in args.list.split(',')]

show = argparse.ArgumentParser()
show.add_argument("show", help="select the desired preset", type=str)
args2 = show.parse_args()
