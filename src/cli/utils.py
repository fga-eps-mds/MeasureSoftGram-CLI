import pytz
from datetime import datetime


def pretty_date_str(date_str, format="%m/%d/%Y %H:%M:%S", timezone="Brazil/East"):
    date_time = datetime.fromisoformat(date_str)

    date_time = date_time.astimezone(pytz.timezone(timezone))

    return date_time.strftime(format)
