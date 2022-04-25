import math


def truncate(number, digits) -> float:
    stepper = 10.0**digits
    return math.trunc(stepper * number) / stepper


def print_results(results):
    print("\nThe analysis was completed with Success!" + "\n\nHere are the Results:\n")
    result_values = results["analysis"]

    print("SQC:\n" + f"{truncate((result_values['sqc']['sqc'])*100,2)}%")

    print("\nCharacteristics:")
    for key_c, value_c in result_values["characteristics"].items():
        print(key_c, "=", f"{truncate((value_c * 100),2)}%")

    print("\nSubcharacteristics:")
    for key_sc, value_sc in result_values["subcharacteristics"].items():
        print(key_sc, "=", f"{truncate((value_sc * 100),2)}%")


def validade_analysis_response(status_code, response_json):
    if status_code == 201 or status_code == 200:
        print_results(response_json)
    elif status_code == 404:
        print(response_json["error"])
    else:
        print("Error while making analysis")
