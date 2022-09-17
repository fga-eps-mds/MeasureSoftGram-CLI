import itertools
import threading
import time
import sys
import json
from src.cli.commands.parse_generate.generate_utils import GenerateUtils
from termcolor import colored

# Global vars
done = False
m_history = None
sub_history = None
c_history = None
s_history = None


def parse_generate(fmt: str, host: str) -> int:  # noqa: C901
    try:
        if not GenerateUtils.verify_available_format(fmt):
            raise Exception

    except Exception:
        print()
        print(colored("\tERROR", "red"))
        print("\tNot supported format.")
        print("\tExiting...")
        print()
        return 1

    try:
        f = open(".measuresoftgram")

        config_file = json.load(f)

        if len(config_file.keys()) == 0:
            raise Exception

    except Exception:
        print()
        print(colored("\tERROR", "red"))
        print("\tCould not get .measuresoftgram file from current directory.")
        print("\tExiting...")
        print()
        return 1

    host_url = host

    print("\n--------------------***--------------------***--------------------")
    print(f"\tGenerating {fmt.upper()} output file")
    print()

    organization_id = config_file['organization']['id']
    product_id = config_file['product']['id']
    product_name = config_file['product']['name']

    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'products/{product_id}/'
        'repositories/'
    )

    output_df = GenerateUtils.create_df()

    try:
        print("\tCalling MeasureSoftGram Service instance")
        body = GenerateUtils.call_service(host_url)

        if body is None:
            raise Exception

        for repository_data in body['results']:
            repository_name = repository_data['name']

            globals()['done'] = False
            print("\n--------------------***--------------------***--------------------")
            print(f"\tRetrieving data from {repository_name}")

            # Run service calls in a thread
            threading.Thread(target=call_for_histories, args=(repository_data['historical_values']['measures'],
                                                              repository_data['historical_values'][
                                                                  'subcharacteristics'],
                                                              repository_data['historical_values']['characteristics'],
                                                              repository_data['historical_values']['sqc'])).start()

            # Display for the user a loading screen
            display_loading()

            measure_history = globals()['m_history']
            subcharacteristics_history = globals()['sub_history']
            characteristics_history = globals()['c_history']
            sqc_history = globals()['s_history']

            number_of_lines = min(sqc_history['count'],
                                  GenerateUtils.min_history_count(measure_history),
                                  GenerateUtils.min_history_count(characteristics_history),
                                  GenerateUtils.min_history_count(subcharacteristics_history))

            for position in range(number_of_lines):
                # Create new line dictionary
                new_line = dict()

                # Add datetime and repository to dict
                new_line['datetime'] = sqc_history['results'][position]['created_at']
                new_line['repository'] = repository_name

                # Add measure line to dict
                measure_line = GenerateUtils.get_measure_line(measure_history['results'], position)
                new_line.update(measure_line)

                # Add subcharacteristic line to dict
                sub_line = GenerateUtils.get_entity_line(subcharacteristics_history['results'], position)
                new_line.update(sub_line)

                # Add characteristic line to dict
                char_line = GenerateUtils.get_entity_line(characteristics_history['results'], position)
                new_line.update(char_line)

                # Add sqc to dict
                new_line['sqc'] = sqc_history['results'][position]['value']

                # Add whole line to dataframe
                output_df = GenerateUtils.add_line_to_df(output_df, new_line)

        # Generate output file
        print("\n--------------------***--------------------***--------------------")
        print(f"\tGenerating the output file for {product_name} product")

        output_name = f"{product_name}.{fmt.lower()}"

        if fmt.upper() == "CSV":
            output_df.to_csv(output_name, index=False)

        print(colored(f"\t{output_name} generated successfully!", "green"))
        print("\n")
        return 0

    except Exception:
        print()
        print(colored("\tERROR", "red"))
        print("\tIt looks like something went wrong during the file generating operation.")
        print()
        return 1


def call_for_histories(measure_url, sub_url, char_url, sqc_url):
    glob = globals()
    glob['m_history'] = GenerateUtils.call_service(measure_url)
    glob['sub_history'] = GenerateUtils.call_service(sub_url)
    glob['c_history'] = GenerateUtils.call_service(char_url)
    glob['s_history'] = GenerateUtils.call_service(sqc_url)
    glob['done'] = True


def display_loading():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write(colored('\r\tLoading ' + c, "yellow"))
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write(colored('\r\tDone!       \n', "green"))
