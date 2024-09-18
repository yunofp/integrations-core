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


def get_months_dict_and_map():

    months_dict = {
        "JAN": 0,
        "FEB": 0,
        "MAR": 0,
        "APR": 0,
        "MAY": 0,
        "JUN": 0,
        "JUL": 0,
        "AUG": 0,
        "SEP": 0,
        "OCT": 0,
        "NOV": 0,
        "DEC": 0,
    }

    month_map = {
        1: "JAN",
        2: "FEB",
        3: "MAR",
        4: "APR",
        5: "MAY",
        6: "JUN",
        7: "JUL",
        8: "AUG",
        9: "SEP",
        10: "OCT",
        11: "NOV",
        12: "DEC",
    }

    return months_dict, month_map


def convert_date_utc(date, timezone="America/Sao_Paulo"):
    local_timezone = pytz.timezone(timezone)
    if date.tzinfo is None:
        local_time = local_timezone.localize(date)
    else:
        local_time = date
    utc_time = local_time.astimezone(pytz.utc)
    return utc_time
