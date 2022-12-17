import requests
import json
from io import StringIO
from src.clients.service_client import ServiceClient


DUMMY_HOST = "http://dummy_host.com/"
URL = 'http://api/v1/organizations/4/products/5/repositories/10/historical-values/metrics/1'


class DummyResponse:
    def __init__(self, status_code, res_data):
        self.status_code = status_code
        self.res_data = res_data
        self.text = json.dumps(res_data)

    def json(self):
        return self.res_data


def test_configure_session():
    session = requests.Session()
    ServiceClient.configure_session(session)
    assert session.headers["User-Agent"] == 'python-requests/2.28.1'
    assert session.headers["Accept-Encoding"] == 'gzip, deflate'
    assert session.headers["Accept"] == '*/*'
    assert session.headers["Connection"] == 'keep-alive'


# def test_make_get_request():
#     response = ServiceClient.make_get_request(URL)
#     assert response.url == URL


def test_make_post_request(mocker):
    mocker.patch(
        "src.clients.service_client.ServiceClient.make_post_request",
        return_value=DummyResponse(201, {"id": 1})
    )
    with mocker.patch("sys.stdout", new=StringIO()):
        response = ServiceClient.make_post_request(DUMMY_HOST, "tests/unit/data/init.json")

        assert response.status_code == 201


# def test_get_entity():
#     response = ServiceClient.get_entity(URL)
#     assert response.url == URL


# def test_calculate_entity(mocker):
#     response = ServiceClient.calculate_entity(URL, {})
#     assert response.url == URL


# def test_import_file():
#     response = ServiceClient.import_file(URL, {})
#     assert response.url == URL


def test_calculate_all_entities_sucess(mocker):
    mocker.patch(
        "src.clients.service_client.ServiceClient.make_post_request",
        return_value=DummyResponse(201, {})
    )
    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        ServiceClient.calculate_all_entities(DUMMY_HOST, "2022-09-18T13:54:58.598413-03:00")

        expected_lines = [
            'Calculating measures...',
            'Calculating subcharacteristics...',
            'Calculating characteristics...',
            'Calculating sqc...',
            '--> OK',
        ]

        for line in expected_lines:
            assert line in fake_out.getvalue()


def test_calculate_all_entities_fail(mocker):
    mocker.patch(
        "src.clients.service_client.ServiceClient.make_post_request",
        return_value=DummyResponse(200, {})
    )
    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:
        ServiceClient.calculate_all_entities(DUMMY_HOST, {})

        expected_lines = [
            '--> FAIL',
        ]

        for line in expected_lines:
            assert line in fake_out.getvalue()
