import json

from tabulate import tabulate
from src.cli.commands.parse_get_entity.utils import get_entity

from src.cli.utils import check_host_url
from src.clients.service_client import ServiceClient
from src.config.settings import SUPPORTED_FORMATS


def parse_get_entity(
    entity_name,
    entity_id,
    host_url,
    organization_id,
    repository_id,
    product_id,
    output_format,
    history,
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
        f'products/{product_id}/'
        f'repositories/{repository_id}/'
        f'{"historical-values/" if history else "latest-values/"}'
        f'{entity_name}/'
        f'{entity_id if entity_id else ""}'
    )
    response = ServiceClient.get_entity(host_url)

    extracted_data, headers, data = get_entity(
        response,
        entity_name,
        entity_id,
        history
    )

    if output_format == 'tabular':
        print(tabulate(extracted_data, headers=headers))
    elif output_format == 'json':
        print(json.dumps(data))
