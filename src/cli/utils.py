import pytz
from datetime import datetime


def pretty_date_str(date_str, format="%m/%d/%Y %H:%M:%S", timezone="Brazil/East"):
    date_time = datetime.fromisoformat(date_str)

    date_time = date_time.astimezone(pytz.timezone(timezone))

    return date_time.strftime(format)


def check_host_url(host_url):
    return host_url if host_url.endswith("/") else host_url + "/"
