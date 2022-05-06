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
        print(f"\n\t{characteristics[characteristic]['name']}:")
        for subcharacteristic in subcharacteristics:
            if (
                characteristic
                in subcharacteristics[subcharacteristic]["characteristics"]
            ):
                print(f"\t\t{subcharacteristics[subcharacteristic]['name']}:")
                for measure in measures:
                    if subcharacteristic in measures[measure]["subcharacteristics"]:
                        print(f"\t\t\t{measures[measure]['name']}:")
                        print(f"\t\t\t\t{', '.join(measures[measure]['metrics'])}")
