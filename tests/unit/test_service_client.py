import requests
from src.clients.service_client import ServiceClient


URL = 'http://api/v1/organizations/4/products/5/repositories/10/historical-values/metrics/1'


def test_configure_session():
    session = requests.Session()
    ServiceClient.configure_session(session)
    assert session.headers["User-Agent"] == 'python-requests/2.28.1'
    assert session.headers["Accept-Encoding"] == 'gzip, deflate'
    assert session.headers["Accept"] == '*/*'
    assert session.headers["Connection"] == 'keep-alive'


def test_make_get_request():
    response = ServiceClient.make_get_request(URL)
    assert response.url == URL
    

def test_make_post_request():
    response = ServiceClient.make_post_request(URL, {})
    assert response.url == URL


def test_get_entity():
    response = ServiceClient.get_entity(URL)
    assert response.url == URL


def test_calculate_entity():
    response = ServiceClient.calculate_entity(URL, {})
    assert response.url == URL
