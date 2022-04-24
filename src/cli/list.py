import requests

BASE_URL = "http://localhost:5000/"


def parse_list():
    pre_configs = requests.get(
        BASE_URL + "/pre-configs",
        headers={"Accept": "application/json"},
    ).json()

    print(
        "{:<30} {:<35} {:<30} {:<10}".format("ID", "Name", "Created at", "Metrics file")
    )

    for pre_config in pre_configs:
        pre_config_name = pre_config["name"] if pre_config["name"] else "-"

        print(
            "{:<30} {:<35} {:<30} {:<10}".format(
                pre_config["_id"], pre_config_name, pre_config["created_at"], ""
            )
        )
