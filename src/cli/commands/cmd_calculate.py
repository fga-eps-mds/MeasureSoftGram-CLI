import json

from tabulate import tabulate
from termcolor import colored
import logging

from src.cli.jsonReader import open_json_file
from src.cli.exceptions import MeasureSoftGramCLIException
from src.cli.resources.measure import calculate_measures
from src.cli.resources.subcharacteristic import calculate_subcharacteristics
from src.cli.resources.characteristic import calculate_characteristics
logger = logging.getLogger("msgram")


def command_calculate(args):
    try:
        output_format = args["output_format"]
        config_dir_path = args["config_dir_path"]
        file_path = args["file_path"]
    except Exception as e:
        logger.error(f"KeyError: args['{e}'] - non-existent parameters")
        exit(1)

    config = open_json_file(f"{config_dir_path}/msgram.json")

    try:
        data_measures, headers_measures = calculate_measures(file_path)
        data_subcharacteristics, headers_subcharacteristics = calculate_subcharacteristics(
            config, data_measures['measures']
        )
        data_characteristics, headers_characteristics = calculate_characteristics(
            config, data_subcharacteristics['subcharacteristics']
        )
        # data_sqc, headers_sqc = calculate_sqc(host_url)

        if output_format == "tabular":
            print(colored("\nCalculated Measures: \n", "green"))
            print(tabulate(data_measures, headers=headers_measures))

            print(colored("\nCalculated Subcharacteristics: \n", "green"))
            print(tabulate(data_subcharacteristics, headers=headers_subcharacteristics))

            print(colored("\nCalculated Characteristics: \n", "green"))
            print(tabulate(data_characteristics, headers=headers_characteristics))

            # print(colored("\nCalculated SQC: \n", "green"))
            # print(tabulate(data_sqc, headers=headers_sqc))

        elif output_format == "json":
            print(colored("\nCalculated Measures: \n", "green"))
            print(json.dumps(data_measures))

            print(colored("\nCalculated Subcharacteristics: \n", "green"))
            print(json.dumps(data_subcharacteristics))

            print(colored("\nCalculated Characteristics: \n", "green"))
            print(json.dumps(data_characteristics))

            # print(colored("\nCalculated SQC: \n", "green"))
            # print(json.dumps(data_sqc))

    except MeasureSoftGramCLIException as error:
        print(colored(f"Error: {error}", "red"))
        return 1
