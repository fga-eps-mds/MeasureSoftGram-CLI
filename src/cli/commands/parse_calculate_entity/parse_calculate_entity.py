import json
from urllib.error import HTTPError
from wsgiref import headers
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
    output_format,
):

    host_url = check_host_url(host_url)

    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'products/{product_id}/'
        f'repositories/{repository_id}/'
        f'calculate/'
    )

    data_measures = calculate_measures(host_url)
    data_characteristics = calculate_characteristics(host_url)
    data_subcharacteristics = calculate_subcharacteristics(host_url)

    if output_format == 'tabular':
        print('Calculated Measures: \n')
        print(tabulate(data_measures, headers='keys'))
        print('\n')

        # print('Calculated Characteristics: \n')
        # print(tabulate(data_characteristics, headers='keys'))
        # print('\n')

        # print('Calculated Subcharacteristics: \n')
        # print(tabulate(data_subcharacteristics, headers='keys'))
        # print('\n')
    elif output_format == 'json':
        print(json.dumps(data_measures))
        # print(json.dumps(calculate_characteristics))
        # print(json.dumps(calculate_subcharacteristics))
