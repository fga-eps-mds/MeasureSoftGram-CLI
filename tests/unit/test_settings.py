import os
import pytest
from src.config.settings import (
    config_file_json,
    get_organization,
    get_product_id,
    get_repositories,
    get_repositories_urls_mapped_by_name,
    get_product_url
)

VALID_CONFIG = '{"organization":{"name": "fga-eps-mds","id": 1},"product":{"name":"MeasureSoftGram","id":3}' + \
               ',"repositories":[{"2022-1-MeasureSoftGram-CLI":1},{"2022-1-MeasureSoftGram-Core":2},{"2022-' + \
               '1-MeasureSoftGram-Service":3},{"2022-1-MeasureSoftGram-Front":4}]}'
VALID_HOST = "https://measuresoftgram-service.herokuapp.com/"


def setup_succes():
    f = open(".measuresoftgram", "w")
    f.write(VALID_CONFIG)
    f.close()


def teardown():
    try:
        os.remove(".measuresoftgram")
    except Exception:
        pass


def test_config_file_json_succes(mocker):

    setup_succes()

    mocker.patch("builtins.open", mocker.mock_open(read_data=VALID_CONFIG))
    mocker.patch("json.load", return_value=VALID_CONFIG)

    res = VALID_CONFIG.replace('"', '\'').replace(' ', '')

    assert str(config_file_json()).replace(' ', '') in res

    teardown()


def test_config_file_json_fail():

    with pytest.raises(SystemExit) as e:
        config_file_json()

    assert str(e.value) == '0'


def test_get_organization(mocker):
    setup_succes()

    mocker.patch("builtins.open", mocker.mock_open(read_data=VALID_CONFIG))
    mocker.patch("json.load", return_value=VALID_CONFIG)

    assert get_organization() == {'name': 'fga-eps-mds', 'id': 1}

    teardown()


def test_get_product_id(mocker):
    setup_succes()

    mocker.patch("builtins.open", mocker.mock_open(read_data=VALID_CONFIG))
    mocker.patch("json.load", return_value=VALID_CONFIG)

    assert get_product_id() == 3

    teardown()


def test_get_repositories(mocker):
    setup_succes()

    mocker.patch("builtins.open", mocker.mock_open(read_data=VALID_CONFIG))
    mocker.patch("json.load", return_value=VALID_CONFIG)

    print(get_repositories())
    assert get_repositories() == [
        ('2022-1-MeasureSoftGram-CLI', 1),
        ('2022-1-MeasureSoftGram-Core', 2),
        ('2022-1-MeasureSoftGram-Service', 3),
        ('2022-1-MeasureSoftGram-Front', 4)
    ]

    teardown()


def test_get_repositories_urls_mapped_by_name(mocker):
    setup_succes()

    mocker.patch("builtins.open", mocker.mock_open(read_data=VALID_CONFIG))
    mocker.patch("json.load", return_value=VALID_CONFIG)

    url = 'https://measuresoftgram-service.herokuapp.com/api/v1/organizations/1/products/3/repositories'

    assert get_repositories_urls_mapped_by_name(VALID_HOST) == {
        'fga-eps-mds-2022-1-MeasureSoftGram-CLI': f'{url}/1/',
        'fga-eps-mds-2022-1-MeasureSoftGram-Core': f'{url}/2/',
        'fga-eps-mds-2022-1-MeasureSoftGram-Service': f'{url}/3/',
        'fga-eps-mds-2022-1-MeasureSoftGram-Front': f'{url}/4/'
    }

    teardown()


def test_get_product_url(mocker):
    setup_succes()

    mocker.patch("builtins.open", mocker.mock_open(read_data=VALID_CONFIG))
    mocker.patch("json.load", return_value=VALID_CONFIG)

    print(get_product_url(VALID_HOST))

    url = 'https://measuresoftgram-service.herokuapp.com//api/v1/organizations/1/products/3/'

    assert get_product_url(VALID_HOST) == url

    teardown()
