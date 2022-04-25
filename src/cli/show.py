import requests
from src.cli.utils import pretty_date_str

BASE_URL = "http://localhost:5000/"


def parse_show(id):
    response = requests.get(
        BASE_URL + f"/pre-configs/{id}",
        headers={"Accept": "application/json"},
    )

    response_data = response.json()

    if 200 <= response.status_code <= 299:
        print(f"Name: {response_data['name']}")
        print(f"ID: {response_data['_id']}")
        print(f"Created at: {pretty_date_str(response_data['created_at'])}")

        print(
            "\nSelected levels. Ordered as characteristics -> subcharacteristics -> measures\n"
        )

        for key, char_data in response_data["characteristics"].items():
            print(f"{key} (weigth: {char_data['weight']})")

            for subchar in char_data["subcharacteristics"]:
                subchar_data = response_data["subcharacteristics"][subchar]

                print(f"\t{subchar} (weigth: {char_data['weights'][subchar]})")

                for measure in subchar_data["measures"]:
                    print(f"\t\t{measure} (weigth: {subchar_data['weights'][measure]})")

            print("\n")
    else:
        print("Error: ", response_data["error"])
