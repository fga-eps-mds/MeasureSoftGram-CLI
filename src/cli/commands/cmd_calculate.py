import json

from tabulate import tabulate
from termcolor import colored
import logging

from src.cli.utils import check_host_url
from src.cli.commands.parse_calculate.utils import (
    # calculate_measures,
    calculate_characteristics,
    calculate_subcharacteristics,
    calculate_sqc,
)
from src.cli.exceptions import MeasureSoftGramCLIException
from src.cli.resources.measure import calculate_measures

logger = logging.getLogger("msgram")


def command_calculate(args):
    try:
        output_format = args["output_format"]
        file_path = args["file_path"]
    except Exception as e:
        logger.error(f"KeyError: args['{e}'] - non-existent parameters")
        exit(1)

    try:
        data_measures, headers_measures = calculate_measures(file_path)
        # data_characteristics, headers_characteristics = calculate_characteristics(host_url)
        # data_subcharacteristics, headers_subcharacteristics = calculate_subcharacteristics(host_url)
        # data_sqc, headers_sqc = calculate_sqc(host_url)

        if output_format == "tabular":
            print(colored("\nCalculated Measures: \n", "green"))
            print(tabulate(data_measures, headers=headers_measures))

            # print(colored("\nCalculated Characteristics: \n", "green"))
            # print(tabulate(data_characteristics, headers=headers_characteristics))

            # print(colored("\nCalculated Subcharacteristics: \n", "green"))
            # print(tabulate(data_subcharacteristics, headers=headers_subcharacteristics))

            # print(colored("\nCalculated SQC: \n", "green"))
            # print(tabulate(data_sqc, headers=headers_sqc))

        elif output_format == "json":
            print(colored("\nCalculated Measures: \n", "green"))
            print(json.dumps(data_measures))

            # print(colored("\nCalculated Characteristics: \n", "green"))
            # print(json.dumps(data_characteristics))

            # print(colored("\nCalculated Subcharacteristics: \n", "green"))
            # print(json.dumps(data_subcharacteristics))

            # print(colored("\nCalculated SQC: \n", "green"))
            # print(json.dumps(data_sqc))
    
    except MeasureSoftGramCLIException as error:
        print(colored(f"Error: {error}", "red"))
        return 1
