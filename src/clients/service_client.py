import requests
import os
from requests.adapters import HTTPAdapter, Retry


class ServiceClient:
    @staticmethod
    def configure_session(session):
        errors = [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511]
        retries = Retry(total=5, backoff_factor=5, status_forcelist=errors)
        # session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

    @staticmethod
    def make_get_request(url):
        with requests.Session() as session:
            ServiceClient.configure_session(session)
            return session.get(url)

    @staticmethod
    def make_post_request(url, payload):
        with requests.Session() as session:
            ServiceClient.configure_session(session)
            return session.post(url, json=payload)

    @staticmethod
    def get_entity(url):
        return ServiceClient.make_get_request(url)

    @staticmethod
    def import_file(url, payload):
        if os.getenv('DEBUG'):
            print()
            print(f'POST {url}')
            print()

        response = ServiceClient.make_post_request(url, payload)

        if os.getenv('DEBUG'):
            print(f'RESPONSE: {response}')
            print()

        return response

    @staticmethod
    def calculate_all_entities(repo_url, created_at=None):
        entities = {
            'measures': {
                'measures': [
                    {'key': 'passed_tests'},
                    {'key': 'test_builds'},
                    {'key': 'test_coverage'},
                    {'key': 'non_complex_file_density'},
                    {'key': 'commented_file_density'},
                    {'key': 'duplication_absense'},
                ],
            },
            'subcharacteristics': {
                'subcharacteristics': [
                    {'key': 'modifiability'},
                    {'key': 'testing_status'}
                ],
            },
            'characteristics': {
                'characteristics': [
                    {'key': 'reliability'},
                    {'key': 'maintainability'}
                ],
            },
            'sqc': {},
        }

        url = repo_url + 'calculate/'

        for entity in entities:
            endpoint = url + f'{entity}/'
            data = entities[entity]

            if created_at:
                data['created_at'] = created_at

            if os.getenv('DEBUG'):
                print("endpoint:", endpoint)

            print(f'\t\t\t--> Calculating {entity}...', end=' ')

            response = ServiceClient.make_post_request(endpoint, data)

            if response.status_code != 201:
                print(f'--> FAIL: {response.text}')

            else:
                print('--> OK')

    def calculate_entity(url, payload):
        return ServiceClient.make_post_request(url, payload)
