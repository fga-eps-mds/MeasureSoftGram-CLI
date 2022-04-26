def print_results(results):
    print("\nThe analysis was completed with Success!\n\nHere are the Results:\n")
    result_values = results["analysis"]

    print(f"SQC: {result_values['sqc']['sqc']}")

    print("\nCharacteristics:")
    for key_c, value_c in result_values["characteristics"].items():
        print("\t", key_c, "=", f"{value_c}")

    print("\nSubcharacteristics:")
    for key_sc, value_sc in result_values["subcharacteristics"].items():
        print("\t", key_sc, "=", f"{value_sc}")


def validade_analysis_response(status_code, response_json):
    if status_code == 201 or status_code == 200:
        print_results(response_json)
    else:
        if response_json is not None and "error" in response_json.keys():
            print("Error: ", response_json["error"])
        else:
            print("Error while making analysis")
