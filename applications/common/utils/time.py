from datetime import datetime
from django.utils.timezone import now

FORMAT_STR_YmdHM: str = "%Y-%m-%d %H:%M"


def get_now():
    return now()


def standard_response_datetime(time: datetime):
    return int(time.timestamp())


def standard_timestamp_response(input_time):
    return int(datetime.timestamp(input_time))


def standard_date_time_response(time: datetime):
    return time.strftime(FORMAT_STR_YmdHM)
