import requests
import json
from flask import current_app as app
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
    
class govClient:
    def __init__(self):
        return None
    
    def verifyCnpj(self, cnpj):

        url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
        querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}

        response = requests.get(url, params=querystring)
        return response.status_code