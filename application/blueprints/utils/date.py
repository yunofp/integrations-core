import pytz


def get_months_list():
    months = [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
    ]
    return months


def convert_date_utc(date, timezone="America/Sao_Paulo"):
    local_timezone = pytz.timezone(timezone)
    if date.tzinfo is None:
        local_time = local_timezone.localize(date)
    else:
        local_time = date
    utc_time = local_time.astimezone(pytz.utc)
    return utc_time
