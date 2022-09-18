from termcolor import colored

from src.clients.service_client import ServiceClient
from src.cli.exceptions import MeasureSoftGramCLIException


def calculate_measures(host_url):
    payload_measures = {
        "measures": [
            {"key": "passed_tests"},
            {"key": "test_builds"},
            {"key": "test_coverage"},
            {"key": "non_complex_file_density"},
            {"key": "commented_file_density"},
            {"key": "duplication_absense"},
            {"key": "team_throughput"}
        ],
    }

    host_url += ('measures/')

    print(colored('\tCalculating Measures...', "blue"))
    data = ServiceClient.calculate_entity(host_url, payload_measures)
    if data.status_code == 201:
        extracted_data = []
        headers = ['Id', 'Name', 'Description', 'Value', 'Created at']
        for temp_data in data.json():
            extracted_data.append([
                temp_data['id'],
                temp_data['name'],
                temp_data['description'],
                temp_data['latest']['value'],
                temp_data['latest']['created_at'],
            ])
        return extracted_data, headers
    else:
        raise MeasureSoftGramCLIException(
            "Unable to calculate measures. Check the connection to the Service host."
        )


def calculate_characteristics(host_url):
    payload_characteristics = {
        "characteristics": [
            {"key": "reliability"},
            {"key": "maintainability"}
        ],
    }

    host_url += ('characteristics/')

    print(colored('\tCalculating Characteristics...', "blue"))
    data = ServiceClient.calculate_entity(host_url, payload_characteristics)
    if data.status_code == 201:
        extracted_data = []
        headers = ['Id', 'Name', 'Description', 'Value', 'Created at']
        for temp_data in data.json():
            extracted_data.append([
                temp_data['id'],
                temp_data['name'],
                temp_data['description'],
                temp_data['latest']['value'],
                temp_data['latest']['created_at'],
            ])
        return extracted_data, headers
    else:
        raise MeasureSoftGramCLIException(
            "Unable to calculate characteristics. Check the connection to the Service host."
        )


def calculate_subcharacteristics(host_url):
    payload_subcharacteristics = {
        "subcharacteristics": [
            {"key": "modifiability"},
            {"key": "testing_status"}
        ],
    }

    host_url += ('subcharacteristics/')

    print(colored('\tCalculating Subcharacteristics...', "blue"))
    data = ServiceClient.calculate_entity(host_url, payload_subcharacteristics)
    if data.status_code == 201:
        extracted_data = []
        headers = ['Id', 'Name', 'Description', 'Value', 'Created at']
        for temp_data in data.json():
            extracted_data.append([
                temp_data['id'],
                temp_data['name'],
                temp_data['description'],
                temp_data['latest']['value'],
                temp_data['latest']['created_at'],
            ])
        return extracted_data, headers
    else:
        raise MeasureSoftGramCLIException(
            "Unable to calculate subcharacteristics. Check the connection to the Service host."
        )


def calculate_sqc(host_url):

    payload_sqc = {}

    host_url += ('sqc/')

    print(colored('\tCalculating SQC...', "blue"))
    data = ServiceClient.calculate_entity(host_url, payload_sqc)
    if data.status_code == 201:
        extracted_data = [[data.json()['id'], data.json()['value'], data.json()['created_at']]]
        headers = ['Id', 'Value', 'Created at']

        return extracted_data, headers
    else:
        raise MeasureSoftGramCLIException(
            "Unable to calculate sqc. Check the connection to the Service host."
        )
