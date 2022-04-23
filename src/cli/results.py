import json


def print_results(results):
    print("\nThe analysis was completed with Success!" + "\n\nHere are the Results:\n")
    result_values = results["analysis"]

    for level in result_values:
        print(f"\n{level}:")
        for key, value in result_values[str(level)].items():
            print(key, "=", value)


def validade_analysis_response(response):
    if response.status_code == 201:
        print_results(response.json())
    elif response.status_code == 404 or response.status_code == 400:
        print(json.loads(response.text)["error"])
    else:
        print("Error while making analysis")
