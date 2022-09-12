import json
from urllib.error import HTTPError
import requests

from tabulate import tabulate

from src.cli.utils import check_host_url
from src.clients.service_client import ServiceClient


def parse_calculate_entity(
    host_url,
    organization_id,
    repository_id,
    product_id,
):

    payload = {
        "characteristics": [
            {"key": "reliability"},
            {"key": "maintainability"}
        ],
    }

    host_url = check_host_url(host_url)

    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'products/{product_id}/'
        f'repositories/{repository_id}/'
        f'calculate/'
        f'characteristics/'
    )

    print(host_url)

    try:
        response = ServiceClient.calculate_entity(host_url, payload)

        print(response.json())

    except:
        requests.RequestException,
        ConnectionError,
        HTTPError,
        json.decoder.JSONDecodeError
