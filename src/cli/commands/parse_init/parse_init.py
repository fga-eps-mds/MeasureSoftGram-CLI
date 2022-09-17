from src.cli.jsonReader import check_file_extension, open_json_file
from src.cli.commands.parse_init.utils import check_if_init_file_already_exists, validate_user_file
from src.cli.exceptions import MeasureSoftGramCLIException
from src.cli.utils import check_host_url


def parse_init(file_path, host_url):
    file_path = str(file_path)

    try:
        check_if_init_file_already_exists()
        check_file_extension(file_path)

        user_config_file = open_json_file(file_path)
        validate_user_file(user_config_file)
    except MeasureSoftGramCLIException as error:
        print("Error:", error)
        return

    host_url = check_host_url(host_url)
