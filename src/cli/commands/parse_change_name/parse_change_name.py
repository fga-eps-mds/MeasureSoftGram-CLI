import requests

from src.config.settings import BASE_URL


def parse_change_name(pre_config_id, new_name):
    response = requests.patch(
        BASE_URL + f"pre-configs/{pre_config_id}", json={"name": new_name}
    )

    response_data = response.json()

    if 200 <= response.status_code <= 299:
        print(
            f'Your Pre Configuration name was succesfully changed to "{response_data["name"]}"'
        )
    else:
        print(
            f"There was an ERROR while changing your Pre Configuration name:  {response_data['error']}"
        )
