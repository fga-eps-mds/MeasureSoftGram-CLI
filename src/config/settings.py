import os
import json
import sys
from termcolor import colored

from src.cli.exceptions import exceptions


SERVICE_URL = os.getenv("SERVICE_URL", "https://measuresoftgram-service.herokuapp.com/")

BASE_URL = "http://172.20.0.2:5000/"

AVAILABLE_ENTITIES = [
    "metrics",
    "measures",
    "subcharacteristics",
    "characteristics",
    # "sqc",
]

SUPPORTED_FORMATS = [
    "json",
    "tabular",
]

AVAILABLE_IMPORTS = [
    "sonarqube"
]

AVAILABLE_GEN_FORMATS = [
    "csv"
]


def config_file_json():
    filepath = os.path.join(os.getcwd(), ".measuresoftgram")

    if os.path.exists(filepath) is False:
        error_msg = ((
            "\n.measuresoftgram file not found.\n"
            f"The directory where the search was performed was: `{os.getcwd()}/`.\n"
            "Please, run the command 'measuresoftgram init repositories.json' to create the file."
        ))
        print(colored(f'\t\t\t{error_msg}\n', 'red'))
        sys.exit(0)

    with open(filepath, "r") as file:
        try:
            return json.load(file)

        except json.decoder.JSONDecodeError:
            raise exceptions.ConfigFileFormatInvalid((
                "The .measuresoftgram file is not a valid json file. "
            ))


def get_organization():
    data = config_file_json()

    if "organization" not in data:
        raise exceptions.ConfigFileQueryFailed((
            "The organization key was not found in the .measuresoftgram file. "
            "Please, run the command 'measuresoftgram init' to create the file."
        ))

    if "id" not in data["organization"]:
        raise exceptions.ConfigFileQueryFailed((
            "The organization id key was not found in the .measuresoftgram file. "
            "Please, run the command 'measuresoftgram init' to create the file."
        ))

    if "name" not in data["organization"]:
        raise exceptions.ConfigFileQueryFailed((
            "The organization name key was not found in the .measuresoftgram file. "
            "Please, run the command 'measuresoftgram init' to create the file."
        ))

    return data["organization"]


def get_organization_id():
    """
    Retorna o ID da organização.
    Para isso essa função consulta o arquivo .measuresoftgram na pasta
    onde o comando foi executado e retorna o
    valor contido em ["organization"]["id"]
    """
    organization = get_organization()
    return organization["id"]


def get_product_id():
    """
    Retorna o ID do produto.

    Para isso essa função consulta o arquivo .measuresoftgram na pasta
    onde o comando foi executado e retorna o
    valor contido em ["product"]["id"]
    """
    data = config_file_json()

    if "product" not in data:
        raise exceptions.ConfigFileQueryFailed((
            "The product key was not found in the .measuresoftgram file. "
            "Please, run the command 'measuresoftgram init' to create the file."
        ))

    if "id" not in data["product"]:
        raise exceptions.ConfigFileQueryFailed((
            "The product id key was not found in the .measuresoftgram file. "
            "Please, run the command 'measuresoftgram init' to create the file."
        ))

    return data["product"]["id"]


def get_repositories():
    data = config_file_json()

    if "repositories" not in data:
        raise exceptions.ConfigFileQueryFailed((
            "The repositories key was not found in the .measuresoftgram file. "
            "Please, run the command 'measuresoftgram init' to create the file."
        ))

    if not isinstance(data["repositories"], list):
        raise exceptions.ConfigFileQueryFailed((
            "The repositories key must be a list. "
            "Please, run the command 'measuresoftgram init' to create the file."
        ))

    repositories = []

    for repository in data["repositories"]:
        for k, v in repository.items():
            repositories.append((k, v))

    return repositories


def get_product_url(host_url):
    organization_id = get_organization_id()
    product_id = get_product_id()
    return (
        f'{host_url}/api/v1/organizations/{organization_id}/'
        f'products/{product_id}/'
    )


def get_repositories_urls_mapped_by_name(host_url):
    """
    Retorna um dicionário com o mapeamento da substring presente no nome do
    arquivo com a url do repositório que os dados deste arquivo deverão
    ser importados.
    """
    if host_url.endswith('/'):
        host_url = host_url[:-1]

    organization_id = get_organization_id()
    product_id = get_product_id()

    path = f'{host_url}/api/v1/organizations/{organization_id}'
    path += f'/products/{product_id}/repositories'

    repositories = get_repositories()
    organization_name = get_organization()["name"]

    return {
        f"{organization_name}-{repository_name}": f"{path}/{repository_id}/"
        for repository_name, repository_id in repositories
    }

    # return {
    #     'fga-eps-mds-2022-1-MeasureSoftGram-Service': f'{path}/1/',
    #     'fga-eps-mds-2022-1-MeasureSoftGram-Core': f'{path}/2/',
    #     'fga-eps-mds-2022-1-MeasureSoftGram-Front': f'{path}/3/',
    #     'fga-eps-mds-2022-1-MeasureSoftGram-CLI': f'{path}/4/',
    # }
