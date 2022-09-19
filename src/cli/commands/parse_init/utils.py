import contextlib
import json
from os.path import exists

import validators
from termcolor import colored

from src.cli.exceptions import exceptions
from src.clients.service_client import ServiceClient

INIT_FILE_NAME = ".measuresoftgram"


def check_if_init_file_already_exists():
    if exists(INIT_FILE_NAME):
        raise exceptions.InitFileAlreadyExists(
            "Init file already exists. Check the file '.measuresoftgram'"
        )


def validate_user_file(config_json_file):
    check_file_keys(config_json_file)
    check_file_data(config_json_file)


def check_file_keys(json_file):
    file_keys_diff = {"organization_name", "product_name", "repositories"} - json_file.keys()
    if len(file_keys_diff) > 0:
        raise exceptions.InvalidMeasuresoftgramFormat(
            f"Provided file is missing the required keys: {', '.join(file_keys_diff)}."
        )


def check_file_data(json_file):
    organization = json_file["organization_name"]
    product = json_file["product_name"]
    repositories = json_file["repositories"]

    if not isinstance(organization, str) or not organization.strip():
        raise exceptions.InvalidMeasuresoftgramFormat(
            "Organization name must be a not empty string."
        )

    if not isinstance(product, str) or not product.strip():
        raise exceptions.InvalidMeasuresoftgramFormat(
            "Product name must be a not empty string."
        )

    if not isinstance(repositories, list):
        raise exceptions.InvalidMeasuresoftgramFormat(
            "Repositories must be a list of urls."
        )

    for repository in repositories:
        if validators.url(repository) is not True:
            raise exceptions.InvalidMeasuresoftgramFormat(
                f"Invalid url format for repository: {repository}"
            )


def create_org_prod_n_repos(host_url, json_file):
    organization_url = host_url + "api/v1/organizations/"
    organization_name = json_file["organization_name"]
    organization_id = create_entity(organization_url, organization_name, "organization")

    product_url = organization_url + f"{organization_id}/products/"
    product_name = json_file["product_name"]
    product_id = create_entity(product_url, product_name, "product")

    repositories = []
    repository_url = product_url + f"{product_id}/repositories/"
    for repository in json_file["repositories"]:
        repository_name = repository.split("/")[-1]
        repository_id = create_entity(repository_url, repository_name, "repository")
        repositories.append({repository_name: repository_id})

    return {
        "organization": {
            "name": organization_name,
            "id": organization_id,
        },
        "product": {
            "name": product_name,
            "id": product_id,
        },
        "repositories": repositories,
    }


def create_entity(url, name, entity):
    payload = dict(name=name)
    response = ServiceClient.make_post_request(url, payload)

    if response.status_code == 201:
        entity_id = json.loads(response.text)["id"]
        print(colored(f"\tCreated {entity} with name {name} and id {entity_id} ...", "blue"))
        return entity_id

    elif response.status_code == 400:
        print(colored(f"\t{entity} with name {name} already exists ...", "blue"))

        with contextlib.suppress(Exception):
            response = ServiceClient.make_get_request(url)
            data = response.json()

            for entity_d in data['results']:
                if entity_d['name'] == name:
                    print(colored(f"\t{entity} with name {name} returned id {entity_d['id']} ...", "blue"))
                    return entity_d['id']

        raise exceptions.MeasureSoftGramCLIException(
            f"An {entity} with the provided name already exists. "
            f"Use a new one or change the '.measuresoftgram' file manually."
        )
    else:
        raise exceptions.MeasureSoftGramCLIException(
            f"Unable to create an {entity}. Check the connection to the Service host."
        )
