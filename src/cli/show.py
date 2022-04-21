import requests

BASE_URL = "http://localhost:5000/"


def parse_show(id):
    response = requests.get(
        BASE_URL + f"/pre-configs/{id}",
        headers={"Accept": "application/json"},
    )

    response_data = response.json()

    if 200 <= response.status_code <= 299:
        print(response_data)
    else:
        print("Error: ", response_data["Error"])
