from os.path import exists

import validators

from src.cli.exceptions import exceptions

INIT_FILE_NAME = ".measuresoftgram.json"


def check_if_init_file_already_exists():
    if exists(INIT_FILE_NAME):
        raise exceptions.InitFileAlreadyExists("Init file already exists. Check the file '.measuresoftgram.json'")


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
