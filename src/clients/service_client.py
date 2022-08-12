import requests
from requests.adapters import HTTPAdapter, Retry


class ServiceClient:
    @staticmethod
    def configure_session(session):
        errors = [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511]
        retries = Retry(total=5, backoff_factor=5, status_forcelist=errors)
        # session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))

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
        return ServiceClient.make_post_request(url, payload)
