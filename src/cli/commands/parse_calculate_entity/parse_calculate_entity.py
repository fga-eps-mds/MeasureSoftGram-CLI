import json
from urllib.error import HTTPError
import requests

from tabulate import tabulate

from src.cli.utils import check_host_url
from src.clients.service_client import ServiceClient
from src.cli.commands.parse_calculate_entity.utils import calculate_measures, calculate_characteristics, calculate_subcharacteristics


def parse_calculate_entity(
    host_url,
    organization_id,
    repository_id,
    product_id,
):

    host_url = check_host_url(host_url)

    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'products/{product_id}/'
        f'repositories/{repository_id}/'
        f'calculate/'
    )

    res = calculate_subcharacteristics(host_url)

    print(res)
