import requests

from src.cli.commands.parse_analysis.results import validade_analysis_response
from src.config.settings import BASE_URL


def parse_analysis(id):
    data = {"pre_config_id": id}
    response = requests.post(BASE_URL + "analysis", json=data)

    validade_analysis_response(response.status_code, response.json())
