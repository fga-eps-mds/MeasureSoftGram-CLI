from email import header
import json

from tabulate import tabulate

from src.cli.utils import check_host_url
from src.clients.service_client import ServiceClient
from src.cli.commands.parse_calculate_entity.utils import calculate_measures, calculate_characteristics, calculate_subcharacteristics, calculate_sqc


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

    data_measures, headers_measures = calculate_measures(host_url)
    data_characteristics, headers_characteristics = calculate_characteristics(host_url)
    data_subcharacteristics, headers_subcharacteristics = calculate_subcharacteristics(host_url)
    data_sqc, headers_sqc = calculate_sqc(host_url)

    if output_format == 'tabular':
        print('Calculated Measures: \n')
        print(tabulate(data_measures, headers=headers_measures))
        print('\n')

        print('Calculated Characteristics: \n')
        print(tabulate(data_characteristics, headers=headers_characteristics))
        print('\n')

        print('Calculated Subcharacteristics: \n')
        print(tabulate(data_subcharacteristics, headers=headers_subcharacteristics))
        print('\n')

        print('Calculated SQC: \n')
        print(tabulate(data_sqc, headers=headers_sqc))

    elif output_format == 'json':
        print(json.dumps(data_measures))
        print(json.dumps(calculate_characteristics))
        print(json.dumps(calculate_subcharacteristics))
