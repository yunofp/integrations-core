import requests
from io import BytesIO
import os
from unittest.mock import call, MagicMock
import os
import pytz
from freezegun import freeze_time
from datetime import datetime, timezone
import numpy as np
from io import BytesIO
import requests
from application.tests.utils.date import utils_test_convert_to_utc_date


def create_response_with_csv():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'file.csv')
    
    with open(csv_path, 'rb') as f:
        csv_content = f.read()
    
    response = requests.Response()
    response.status_code = 200
    response._content = b''
    response.headers['Content-Type'] = 'multipart/form-data'
    
    response.files = {
        'file': BytesIO(csv_content)
    }
    response.files['file'].filename = 'file.csv'
     
    return response