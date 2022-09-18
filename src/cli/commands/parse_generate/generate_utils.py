import pandas as pd
import json
from typing import Union
from src.clients.service_client import ServiceClient
from src.config.settings import AVAILABLE_GEN_FORMATS


class GenerateUtils:
    @staticmethod
    def verify_available_format(fmt: str) -> bool:
        return fmt.lower() in AVAILABLE_GEN_FORMATS

    @staticmethod
    def call_service(host_url: str) -> Union[dict, None]:
        try:
            res = ServiceClient.make_get_request(host_url)
            if res.status_code != 200:
                raise Exception
            body = json.loads(res.content)
            return body
        except Exception:
            return None

    @staticmethod
    def create_df():
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
            'functional_completeness',
            'testing_status',
            'maintainability',
            'reliability',
            'functional_suitability',
            'sqc',
        ]
        output = pd.DataFrame(columns=columns)
        return output

    @staticmethod
    def min_history_count(entity):
        counts = []
        for item in entity['results']:
            counts.append(len(item['history']))
        return min(counts)

    @staticmethod
    def get_measure_line(measure_list, position):
        em_dict = {
            'non_complex_file_density': 'em1',
            'commented_file_density': 'em2',
            'duplication_absense': 'em3',
            'passed_tests': 'em4',
            'test_builds': 'em5',
            'test_coverage': 'em6',
            'team_throughput': 'em7',
        }

        def get_em(name):
            if name in em_dict.keys():
                return em_dict[name]
            else:
                return "None"

        length = len(measure_list)
        line_dict = dict()

        for i in range(length):
            line_dict[get_em(measure_list[i]['key'])] = measure_list[i]['history'][position]['value']

        return line_dict

    @staticmethod
    def get_entity_line(entity_list, position):
        length = len(entity_list)
        line_dict = dict()

        for i in range(length):
            line_dict[entity_list[i]['key']] = entity_list[i]['history'][position]['value']

        return line_dict

    @staticmethod
    def add_line_to_df(df: pd.DataFrame, line: dict):
        if "None" in line.keys():
            line.pop("None")
        new_line = pd.DataFrame(line, index=[0])
        new_df = pd.concat([df, new_line], ignore_index=True, axis=0)
        return new_df
