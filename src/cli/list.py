import requests
import pytz
from datetime import datetime

BASE_URL = "http://localhost:5000/"


def parse_list():
    response = requests.get(
        BASE_URL + "/pre-configs",
        headers={"Accept": "application/json"},
    )

    pre_configs = response.json()

    if not 200 <= response.status_code <= 299:
        print("Error: an error occurred while fetching your pre configurations")
        return

    print(
        "{:<30} {:<35} {:<30} {:<10}".format("ID", "Name", "Created at", "Metrics file")
    )

    for pre_config in pre_configs:
        pre_config_name = pre_config["name"] if pre_config["name"] else "-"

        created_at = datetime.fromisoformat(pre_config["created_at"]).astimezone(
            pytz.timezone("Brazil/East")
        )

        created_at = created_at.strftime("%m/%d/%Y %H:%M:%S")

        print(
            "{:<30} {:<35} {:<30} {:<10}".format(
                pre_config["_id"], pre_config_name, created_at, "-"
            )
        )
