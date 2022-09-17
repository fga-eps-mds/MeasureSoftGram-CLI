import os
import itertools
import threading
import time
import sys
from generate_utils import GenerateUtils

# Global vars
done = False
m_history = None
sub_history = None
c_history = None
s_history = None


def parse_generate():
    fmt = "CSV"
    host_url = os.getenv("SERVICE_URL", "https://measuresoftgram-service.herokuapp.com/")

    print("\n--------------------***--------------------***--------------------")
    print(f"Generating {fmt} output file for repository")

    organization_id = GenerateUtils.get_org_id()
    product_id = GenerateUtils.get_prd_id()
    product_name = GenerateUtils.get_prd_name()

    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'products/{product_id}/'
        'repositories/'
    )

    output_df = GenerateUtils.create_df()

    try:
        print("Calling MeasureSoftGram Service instance")
        body = GenerateUtils.call_service(host_url)

        if body is None:
            raise Exception

        for repository_data in body['results']:
            repository_name = repository_data['name']

            globals()['done'] = False
            print("\n--------------------***--------------------***--------------------")
            print(f"Retrieving data from {repository_name}")

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
        print()
        print("\n--------------------***--------------------***--------------------")
        print(f"Generating the output file for {product_name} product")

        output_name = f"{product_name}.{fmt.lower()}"

        if fmt.upper() == "CSV":
            output_df.to_csv(output_name, index=False)

        print(f"{output_name} generated successfully!")

    except Exception:
        print()
        print("It looks like something went wrong during the file generating operation.")
        print()


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
        sys.stdout.write('\rLoading ' + c)
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\rDone!       \n')
