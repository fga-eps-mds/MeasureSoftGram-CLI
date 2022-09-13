import json
from urllib.error import HTTPError
import requests

from src.cli.exceptions.exceptions import MeasureSoftGramCLIException
from src.cli.jsonReader import folder_reader, validate_metrics_post
from src.cli.utils import check_host_url, print_import_files, print_status_import_file
from src.clients.service_client import ServiceClient


def parse_import(
    output_origin,
    dir_path,
    language_extension,
    host_url,
    organization_id,
    repository_id,
    product_id,
):
    print(f'--> Starting to parser import for {output_origin} output...\n')

    try:
        components, files = folder_reader(r"{}".format(dir_path))
    except (MeasureSoftGramCLIException, FileNotFoundError):
        print("Error: The folder was not found")
        return

    payload = {
        "components": [],
        "language_extension": language_extension,
    }

    host_url = check_host_url(host_url)

    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'products/{product_id}/'
        f'repositories/{repository_id}/'
        'collectors/sonarqube/'
    )

    print_import_files(files)

    for idx, component in enumerate(components):
        payload["components"] = component

        for trying_idx in range(3):
            try:
                response = ServiceClient.import_file(host_url, payload)

                message = validate_metrics_post(response.status_code)

                print_status_import_file(files[idx], message, trying_idx + 1)
                break
            except (
                requests.RequestException,
                ConnectionError,
                HTTPError,
                json.decoder.JSONDecodeError
            ):
                print_status_import_file(
                    files[idx],
                    "FAIL: Can't connect to host service.",
                    trying_idx + 1
                )

    print('\nAttempt to save all files in the directory finished!')
