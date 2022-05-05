def to_zero_one_decimal(value):
    if value > 1:
        return value / 100


def print_results(results):
    print("\nThe analysis was completed with Success!\n\nHere are the Results:\n")
    result_values = results["analysis"]

    print(f"SQC: {result_values['sqc']['sqc']}")

    print("\nCharacteristics before weighting:\n")
    for key_c, value_c in result_values["weighted_characteristics"]["sqc"].items():
        print("\t", key_c, "=", f"{to_zero_one_decimal(value_c)}")

    print("\nCharacteristics:\n")
    for key_c, value_c in result_values["characteristics"].items():
        print("\t", key_c, "=", f"{value_c}\n")
        print("\t Subcharacteristics after weighting:")
        for key_sc, value_sc in result_values["weighted_subcharacteristics"][
            key_c
        ].items():
            print("\t\t", key_sc, "=", f"{to_zero_one_decimal(value_sc)}")
        print("\n")

    print("\nSubcharacteristics:\n")
    for key_sc, value_sc in result_values["subcharacteristics"].items():
        print("\t", key_sc, "=", f"{value_sc}\n")
        print("\t Measures after weighting:")
        for key_m, value_m in result_values["weighted_measures"][key_sc].items():
            print("\t\t", key_m, "=", f"{to_zero_one_decimal(value_m)}")
        print("\n")


def validade_analysis_response(status_code, response_json):
    if status_code == 201 or status_code == 200:
        print_results(response_json)
    else:
        if response_json is not None and "error" in response_json.keys():
            print("Error: ", response_json["error"])
        else:
            print("Error while making analysis")
