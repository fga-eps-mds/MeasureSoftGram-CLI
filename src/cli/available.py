import requests

BASE_URL = "http://localhost:5000/"


def parse_available():
    available_pre_configs = requests.get(
        BASE_URL + "available-pre-configs", headers={"Accept": "application/json"}
    ).json()

    print(
        "\nThese are all items available in the MeasureSoftGram database in the following order:\
            \nCharacteristics -> Subcharacteristics -> Measures -> Necessary Metrics\
            \n\n You can use these items to create a pre configuration"
    )

    characteristics = available_pre_configs["characteristics"]
    subcharacteristics = available_pre_configs["subcharacteristics"]
    measures = available_pre_configs["measures"]

    for characteristic in characteristics:
        print_line = characteristics[characteristic]["name"]
        print(f"\n\t{print_line}:")

        for subcharacteristic in subcharacteristics:
            if (
                characteristics[characteristic]["name"].lower().replace(" ", "_")
                in subcharacteristics[subcharacteristic]["characteristics"]
            ):
                print_line = subcharacteristics[subcharacteristic]["name"]
                print(f"\t\t{print_line}:")

                for measure in measures:
                    if (
                        subcharacteristics[subcharacteristic]["name"]
                        .lower()
                        .replace(" ", "_")
                        in measures[measure]["subcharacteristics"]
                    ):
                        print_line = measures[measure]["name"]
                        print(f"\t\t\t{print_line}:")
                        print_line = ", ".join(measures[measure]["metrics"])
                        print(f"\t\t\t\t{print_line}")
