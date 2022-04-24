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

    for characteristic in available_pre_configs["characteristics"]:
        print(
            "\n    {}:".format(
                available_pre_configs["characteristics"][characteristic]["name"]
            )
        )

        for subcharacteristic in available_pre_configs["subcharacteristics"]:
            if (
                available_pre_configs["characteristics"][characteristic]["name"]
                .lower()
                .replace(" ", "_")
                in available_pre_configs["subcharacteristics"][subcharacteristic][
                    "characteristics"
                ]
            ):
                print(
                    "        {}:".format(
                        available_pre_configs["subcharacteristics"][subcharacteristic][
                            "name"
                        ]
                    )
                )

                for measure in available_pre_configs["measures"]:
                    if (
                        available_pre_configs["subcharacteristics"][subcharacteristic][
                            "name"
                        ]
                        .lower()
                        .replace(" ", "_")
                        in available_pre_configs["measures"][measure][
                            "subcharacteristics"
                        ]
                    ):
                        print(
                            "            {}:".format(
                                available_pre_configs["measures"][measure]["name"]
                            )
                        )
                        print(
                            "                {}".format(
                                ", ".join(
                                    available_pre_configs["measures"][measure][
                                        "metrics"
                                    ]
                                )
                            )
                        )
