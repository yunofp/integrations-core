from datetime import datetime
import pytz

def utils_test_convert_to_utc_date(date_string):
    date_format = "%d/%m/%Y"
    local_date = datetime.strptime(date_string, date_format)
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    local_date = sao_paulo_tz.localize(local_date)
    utc_date = local_date.astimezone(pytz.UTC)
    return utc_date
