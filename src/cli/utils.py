import pytz
from termcolor import colored
from datetime import datetime


def pretty_date_str(date_str, format="%m/%d/%Y %H:%M:%S", timezone="Brazil/East"):
    date_time = datetime.fromisoformat(date_str)

    date_time = date_time.astimezone(pytz.timezone(timezone))

    return date_time.strftime(format)


def check_host_url(host_url):
    return host_url if host_url.endswith("/") else host_url + "/"


def print_import_files(files):
    """
        Importing files:
            - sonarmetrics/file1.json
            - sonarmetrics/file2.json
            - sonarmetrics/file3.json

        Sending the file data:
    """
    print('\n\tImporting files:')

    for file in files:
        print(f'\t\t- {file}')

    print('\n\tSending the file data:')


def print_status_import_file(file, message, trying_idx):
    """
            - sonarmetrics/file1.json
            OK: Data sent successfully
    """
    print(f'\t\t- [{trying_idx}] {file}')

    if 'OK:' in message:
        print(colored(f'\t\t{message}\n', 'green'))
    else:
        print(colored(f'\t\t{message}\n', 'red'))
