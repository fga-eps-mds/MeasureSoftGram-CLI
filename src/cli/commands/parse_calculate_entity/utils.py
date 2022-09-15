from src.clients.service_client import ServiceClient
from urllib.error import HTTPError
import requests
import json


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
    print(host_url)

    try:
        response = ServiceClient.calculate_entity(host_url, payload_measures)
        print(response.json())
        return response.json()

    except:
        requests.RequestException,
        # ConnectionError,
        HTTPError,
        json.decoder.JSONDecodeError

    # payload_characteristics = {
    #     "characteristics": [
    #         {"key": "reliability"},
    #         {"key": "maintainability"}
    #     ],
    # }

    # payload_subcharacteristics = {
    #     "subcharacteristics": [
    #         {"key": "modifiability"},
    #         {"key": "testing_status"}
    #     ],
    # }
