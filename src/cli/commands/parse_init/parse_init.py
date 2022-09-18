import json

from termcolor import colored

from src.cli.jsonReader import check_file_extension, open_json_file
from src.cli.commands.parse_init.utils import (
    check_if_init_file_already_exists,
    validate_user_file,
    create_org_prod_n_repos
)
from src.cli.exceptions import MeasureSoftGramCLIException
from src.cli.utils import check_host_url


def parse_init(file_path, host_url):
    file_path = str(file_path)
    host_url = check_host_url(host_url)

    try:
        check_if_init_file_already_exists()
        check_file_extension(file_path)

        user_config_file = open_json_file(file_path)
        validate_user_file(user_config_file)

        init_data = create_org_prod_n_repos(host_url, user_config_file)

        with open('.measuresoftgram', 'w') as file:
            file.write(json.dumps(init_data, indent=4))

        print(colored("'.measuresoftgram' init file created with success", "green"))
    except MeasureSoftGramCLIException as error:
        print(colored(f"Error: {error}", "red"))
        return 1
