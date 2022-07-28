import os
import argparse
import json
import sys
from urllib.error import HTTPError
import requests
import signal
from pathlib import Path

from tabulate import tabulate

from src.cli.show import parse_show
from src.cli.list import parse_list
from src.cli.exceptions import MeasureSoftGramCLIException
from src.cli.jsonReader import folder_reader, validate_metrics_post
from src.cli.results import validade_analysis_response
from src.cli.create import validate_pre_config_post, pre_config_file_reader
from src.cli.available import parse_available
from src.cli.utils import check_host_url, print_import_files, print_status_import_file

BASE_URL = "http://localhost:5000/"

AVAILABLE_ENTITIES = [
    "metrics",
    "measures",
    # "subcharacteristics",
    # "characteristics",
    # "sqc",
]

SUPPORTED_FORMATS = [
    "json",
    "tabular",
]

AVAILABLE_IMPORTS = [
    "sonarqube"
]


def sigint_handler(*_):
    print("\n\nExiting MeasureSoftGram...")
    sys.exit(0)


def parse_analysis(id):
    data = {"pre_config_id": id}
    response = requests.post(BASE_URL + "analysis", json=data)

    validade_analysis_response(response.status_code, response.json())


def parse_import(
    output_origin,
    dir_path,
    language_extension,
    host_url,
    organization_id,
    repository_id
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
        f'repository/{repository_id}/'
        'import/sonarqube-metrics/'
    )

    print_import_files(files)

    for idx, component in enumerate(components):
        payload["components"] = component

        for trying_idx in range(3):
            try:
                response = requests.post(host_url, json=payload)

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


def parse_create(file_path):
    available_pre_config = requests.get(
        BASE_URL + "available-pre-configs",
        headers={"Accept": "application/json"}
    ).json()

    try:
        pre_config = pre_config_file_reader(
            r"{}".format(file_path),
            available_pre_config,
        )
    except MeasureSoftGramCLIException as error:
        print("Error: ", error)
        return

    response = requests.post(BASE_URL + "pre-configs", json=pre_config)

    saved_pre_config = json.loads(response.text)

    validate_pre_config_post(response.status_code, saved_pre_config)


def parse_change_name(pre_config_id, new_name):
    response = requests.patch(
        BASE_URL + f"pre-configs/{pre_config_id}", json={"name": new_name}
    )

    response_data = response.json()

    if 200 <= response.status_code <= 299:
        print(
            f'Your Pre Configuration name was succesfully changed to "{response_data["name"]}"'
        )
    else:
        print(
            f"There was an ERROR while changing your Pre Configuration name:  {response_data['error']}"
        )


def parse_get_entity(
    entity_name,
    entity_id,
    host_url,
    organization_id,
    repository_id,
    output_format,
):
    if output_format not in SUPPORTED_FORMATS:
        print((
            "Output format not supported. "
            f"Supported formats: {SUPPORTED_FORMATS}"
        ))
        return

    host_url = check_host_url(host_url)

    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'repository/{repository_id}/'
        f'{entity_name}/'
    )

    if entity_id:
        host_url += f"{entity_id}"

    response = requests.get(host_url)

    if response.ok is False:
        print(
            f"There was an error while getting the {entity_name} with id {entity_id}."
        )
        return

    headers = ['Name', 'Value', 'Created at']

    if entity_id:
        data = response.json()
        extracted_data = [[
            data['name'],
            data['latest']['value'],
            data['latest']['created_at'],
        ]]
    else:
        data = response.json().get("results")
        extracted_data = []
        for entity_data in data:
            extracted_data.append([
                entity_data['name'],
                entity_data['latest']['value'],
                entity_data['latest']['created_at'],
            ])

    if output_format == 'tabular':
        print(tabulate(extracted_data, headers=headers))
    elif output_format == 'json':
        print(json.dumps(data))


def setup():
    parser = argparse.ArgumentParser(
        description="Command line interface for measuresoftgram"
    )
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    parser_import = subparsers.add_parser("import", help="Import a folder with metrics")

    parser_import.add_argument(
        "output_origin",
        type=str,
        help=(
            "Import a metrics files from some origin. Valid values are: "
            + ", ".join(AVAILABLE_IMPORTS)
        ),
    )

    parser_import.add_argument(
        "dir_path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the directory",
    )

    parser_import.add_argument(
        "language_extension",
        type=str,
        help="The source code language extension",
    )

    parser_import.add_argument(
        "--host",
        type=str,
        nargs='?',
        default=os.getenv(
            "MSG_SERVICE_HOST",
            "https://measuresoftgram-service.herokuapp.com/"
        ),
        help="The host of the service",
    )

    parser_import.add_argument(
        "--organization_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_ORGANIZATION_ID", "1"),
        help="The ID of the organization that the repository belongs to",
    )

    parser_import.add_argument(
        "--repository_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_REPOSITORY_ID", "1"),
        help="The ID of the repository",
    )

    parser_get_entity = subparsers.add_parser(
        "get",
        help="Gets the last record of a specific entity",
    )

    parser_get_entity.add_argument(
        "entity",
        type=str,
        help=(
            "The entity to get. Valid values are: "
            + ", ".join(AVAILABLE_ENTITIES)
        ),
    )

    parser_get_entity.add_argument(
        "entity_id",
        type=int,
        nargs='?',
        help=(
            "The ID of the entity to get. If not provided, a list with the "
            "last record of all available entities will be returned."
        ),
    )

    parser_get_entity.add_argument(
        "--host",
        type=str,
        nargs='?',
        default="https://measuresoftgram-service.herokuapp.com/",
        help="The host of the service",
    )

    parser_get_entity.add_argument(
        "--output_format",
        type=str,
        nargs='?',
        default="tabular",
        help=(
            "The format of the output. "
            "Valid values are: " + ", ".join(SUPPORTED_FORMATS)
        ),
    )

    parser_get_entity.add_argument(
        "--organization_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_ORGANIZATION_ID", "1"),
        help="The ID of the organization that the repository belongs to",
    )

    parser_get_entity.add_argument(
        "--repository_id",
        type=str,
        nargs='?',
        default=os.getenv("MSG_REPOSITORY_ID", "1"),
        help="The ID of the repository",
    )

    parser_create = subparsers.add_parser(
        "create",
        help="Create a new model pre configuration from a JSON file",
    )

    subparsers.add_parser(
        "available",
        help="Shows all characteristics, sub-characteristics and measures available in measuresoftgram",
    )

    parser_create.add_argument(
        "path",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "data",
        help="Path to the JSON file",
    )

    parser_analysis = subparsers.add_parser("analysis", help="Get analysis result")
    parser_analysis.add_argument(
        "id",
    )
    subparsers.add_parser("list", help="List all pre configurations")

    parser_show = subparsers.add_parser(
        "show", help="Show all information of a pre configuration"
    )

    parser_show.add_argument(
        "pre_config_id",
        type=str,
        help="Pre config ID",
    )

    change_name = subparsers.add_parser(
        "change-name", help="Change pre configuration name"
    )

    change_name.add_argument(
        "pre_config_id",
        type=str,
        help="Pre config ID",
    )

    change_name.add_argument(
        "new_name",
        type=str,
        help="New pre configuration name",
    )

    args = parser.parse_args()

    # if args is empty show help
    if not sys.argv[1:]:
        parser.print_help()
        return

    elif args.command == "import":
        parse_import(
            args.output_origin,
            args.dir_path,
            args.language_extension,
            args.host,
            args.organization_id,
            args.repository_id,
        )

    elif args.command == "create":
        parse_create(args.path)

    elif args.command == "analysis":
        parse_analysis(args.id)

    elif args.command == "available":
        parse_available()

    elif args.command == "list":
        parse_list()

    elif args.command == "show":
        parse_show(args.pre_config_id)

    elif args.command == "change-name":
        parse_change_name(args.pre_config_id, args.new_name)

    elif args.command == 'get':
        parse_get_entity(
            args.entity,
            args.entity_id,
            args.host,
            args.organization_id,
            args.repository_id,
            args.output_format,
        )


def main():
    """Entry point for the application script"""

    signal.signal(signal.SIGINT, sigint_handler)

    setup()
