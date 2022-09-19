import re
import datetime as dt
import json
from time import sleep
from typing import Dict
from urllib.error import HTTPError
import requests

from src.config.settings import get_repositories_urls_mapped_by_name

from src.cli.exceptions import exceptions
from src.cli.jsonReader import folder_reader, validate_metrics_post
from src.cli.utils import check_host_url, print_import_files, print_status_import_file
from src.clients.service_client import ServiceClient


def match_repository_url(filename: str, repos_urls: Dict[str, str]) -> str:
    filename = filename.lower()
    filename = filename.replace('_', '-')

    for repo_name, repo_url in repos_urls.items():
        repo_name = repo_name.lower()

        if repo_name in filename:
            return repo_url

    raise exceptions.RepositoryUrlNotFound((
        'Repository url not found. Could not find the repository url '
        'where this file should be imported.'
    ))


def get_created_at_from_filename(filename: str) -> str:
    """
    filename: str = fga-eps-mds-2022-1-MeasureSoftGram-Service-09-11-2022-16-11-42-develop.json
    """
    date_str = re.search(r'\d{1,2}-\d{1,2}-\d{4}-\d{1,2}-\d{1,2}', filename)[0]
    month, day, year, hour, minutes = date_str.split('-')

    return dt.datetime.strptime(
        f'{year}-{month}-{day} {hour}:{minutes}',
        '%Y-%m-%d %H:%M',
    ).isoformat()


def parse_import(
    output_origin,
    dir_path,
    language_extension,
    host_url,
):
    print(f'--> Starting to parser import for {output_origin} output...\n')

    try:
        components, files = folder_reader(f"{dir_path}")
    except (exceptions.MeasureSoftGramCLIException, FileNotFoundError):
        print("Error: The folder was not found")
        return

    payload = {
        "components": [],
        "language_extension": language_extension,
    }

    host_url = check_host_url(host_url)

    print_import_files(files)

    repos_urls = get_repositories_urls_mapped_by_name(host_url)

    for idx, (filename, component) in enumerate(zip(files, components)):
        if idx > 1:
            sleep(1)

        payload["components"] = component

        repo_url = match_repository_url(filename, repos_urls)
        print(f'\t--> Importing {filename} to {repo_url}...')
        created_at = get_created_at_from_filename(filename)

        for trying_idx in range(3):
            try:
                response = ServiceClient.import_file(
                    repo_url + 'collectors/sonarqube/',
                    payload,
                )
                message = validate_metrics_post(response.status_code)
                print_status_import_file(files[idx], message, trying_idx + 1)

                ServiceClient.calculate_all_entities(
                    repo_url,
                    created_at=created_at,
                )

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


if __name__ == '__main__':
    parse_import(
        output_origin='sonarqube',
        dir_path='/home/durval/measure-softgram/docs/analytics-raw-data',
        language_extension='py',
        # host_url='https://measuresoftgram-service.herokuapp.com/',
        host_url='http://localhost:8181/',
        # organization_id='9',
        # repository_id='7',
        # product_id='12',
    )
