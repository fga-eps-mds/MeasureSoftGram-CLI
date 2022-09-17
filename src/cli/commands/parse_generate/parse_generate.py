import json
import os
import pandas as pd
from src.clients.service_client import ServiceClient
from typing import Union


def parse_generate():
    fmt = "CSV"
    host_url = os.getenv("SERVICE_URL", "https://measuresoftgram-service.herokuapp.com/")

    print(f"Generating {fmt} output file for repository")

    organization_id = _get_org_id()
    product_id = _get_prd_id()

    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'products/{product_id}/'
        'repositories/'
    )

    output_df = _create_df()

    try:
        print("Calling MeasureSoftGram Service instance")
        body = _call_service(host_url)

        if body is None:
            raise Exception

        for repository_data in body['results']:
            repository_name = repository_data['name']

            print(f"Retrieving data from {repository_name}")

            measure_history = _call_service(repository_data['historical_values']['measures'])
            subcharacteristics_history = _call_service(repository_data['historical_values']['subcharacteristics'])
            characteristics_history = _call_service(repository_data['historical_values']['characteristics'])
            sqc_history = _call_service(repository_data['historical_values']['sqc'])

            number_of_lines = min(sqc_history['count'],
                                  min_history_count(measure_history),
                                  min_history_count(characteristics_history),
                                  min_history_count(subcharacteristics_history))

            for position in range(number_of_lines):
                # Create new line dictionary
                new_line = dict()

                # Add datetime and repository to dict
                new_line['datetime'] = sqc_history['results'][position]['created_at']
                new_line['repository'] = repository_name

                # Add measure line to dict
                measure_line = _get_measure_line(measure_history['results'], position)
                new_line.update(measure_line)

                # Add subcharacteristic line to dict

                # adiciona todas as primeiras linhas de cada caracteristica
                # adiciona a primeira linha da sqc
                print("aaaa")
                # adiciona linha inteira no dataframe

            print("a")

    except Exception:
        print("nothing at all")


def min_history_count(entity):
    counts = []
    for item in entity['results']:
        counts.append(len(item['history']))
    return min(counts)

def _get_measure_line(measure_list, position):
    def get_em(name):  # TODO: Mapear certo as medidas
        em_dict = {
            'team_throughput': 'em1',
            'passed_tests': 'em2',
            'commented_file_density': 'em3',
            'non_complex_file_density': 'em4',
            'test_builds': 'em5',
            'duplication_absense': 'em6',
            'test_coverage': 'em7',
        }

        if name in em_dict.keys():
            return em_dict[name]
        else:
            return "None"

    length = len(measure_list)
    line_dict = dict()

    for i in range(length):
        line_dict[get_em(measure_list[i]['key'])] = measure_list[i]['history'][position]['value']

    return line_dict


def _get_org_id() -> str:
    return '1'


def _get_prd_id() -> str:
    return '3'


def _call_service(host_url: str) -> Union[dict, None]:
    try:
        res = ServiceClient.make_get_request(host_url)
        if res.status_code != 200:
            raise Exception
        body = json.loads(res.content)
        return body
    except Exception:
        return None


def _create_df():
    columns = [
        'datetime',
        'repository',
        'em1',
        'em2',
        'em3',
        'em4',
        'em5',
        'em6',
        'em7',
        'modifiability',
        'maturity',
        'functional_completeness',
        'maintainability',
        'reliability',
        'functional_suitability',
        'sqc'
    ]
    output = pd.DataFrame(columns=columns)
    return output


def _add_line_to_df(df: pd.DataFrame, line: dict):
    if not verify_dict(line):
        return df
    new_line = pd.DataFrame(line, index=[0])
    new_df = pd.concat([df, new_line], ignore_index=True, axis=0)
    return new_df


def verify_dict(dic: dict):
    valid_columns = [
        'datetime',
        'repository',
        'em1',
        'em2',
        'em3',
        'em4',
        'em5',
        'em6',
        'em7',
        'modifiability',
        'maturity',
        'functional_completeness',
        'maintainability',
        'reliability',
        'functional_suitability',
    ]
    for key in dic.keys():
        if key not in valid_columns:
            return False
    return True


if __name__ == '__main__':
    parse_generate()
