import requests
from requests.adapters import HTTPAdapter, Retry


class ServiceClient:
    def __init__(self, host_service_url):
        self.host = host_service_url

    def calculate_measure(self, params):
        with requests.Session() as session:
            errors = [500, 502, 503, 504]
            retries = Retry(total=5, backoff_factor=5, status_forcelist=errors)
            session.mount("http://", HTTPAdapter(max_retries=retries))
            session.mount("https://", HTTPAdapter(max_retries=retries))
            url = f'{self.host}/calculate-measures/'
            return session.post(url, json=params)
