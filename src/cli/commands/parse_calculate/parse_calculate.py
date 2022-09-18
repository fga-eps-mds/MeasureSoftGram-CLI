import json

from tabulate import tabulate
from termcolor import colored

from src.cli.utils import check_host_url
from src.cli.commands.parse_calculate.utils import (
    calculate_measures,
    calculate_characteristics,
    calculate_subcharacteristics,
    calculate_sqc
)
from src.cli.exceptions import MeasureSoftGramCLIException


def parse_calculate(
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

    try:
        data_measures, headers_measures = calculate_measures(host_url)
        data_characteristics, headers_characteristics = calculate_characteristics(host_url)
        data_subcharacteristics, headers_subcharacteristics = calculate_subcharacteristics(host_url)
        data_sqc, headers_sqc = calculate_sqc(host_url)

        if output_format == 'tabular':
            print(colored('\nCalculated Measures: \n', "green"))
            print(tabulate(data_measures, headers=headers_measures))

            print(colored('\nCalculated Characteristics: \n', "green"))
            print(tabulate(data_characteristics, headers=headers_characteristics))

            print(colored('\nCalculated Subcharacteristics: \n', "green"))
            print(tabulate(data_subcharacteristics, headers=headers_subcharacteristics))

            print(colored('\nCalculated SQC: \n', "green"))
            print(tabulate(data_sqc, headers=headers_sqc))

        elif output_format == 'json':
            print(colored('\nCalculated Measures: \n', "green"))
            print(json.dumps(data_measures))

            print(colored('\nCalculated Characteristics: \n', "green"))
            print(json.dumps(data_characteristics))

            print(colored('\nCalculated Subcharacteristics: \n', "green"))
            print(json.dumps(data_subcharacteristics))

            print(colored('\nCalculated SQC: \n', "green"))
            print(json.dumps(data_sqc))
    except MeasureSoftGramCLIException as error:
        print(colored(f"Error: {error}", "red"))
        return 1
