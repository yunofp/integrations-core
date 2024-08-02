import pytest
from unittest.mock import Mock, call, MagicMock
from flask import Flask
import pandas as pd
import os
from application.blueprints.services import pandas_processement
from application.blueprints.utils import formatting
from application.blueprints.services.contracts import ContractsService
import logging
import requests
from io import BytesIO
from datetime import datetime, timezone
import pytz
from freezegun import freeze_time
from freezegun.api import FakeDatetime

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

@pytest.fixture
def sample_df():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'file.csv')
    df = pd.read_csv(csv_path)
    return df.iloc[11:13]

logger = logging.getLogger(__name__)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['PHONE_NUMBER_DEBUG'] = '123456789'
    app.config['CONTRACTS_PROCESSING_DAYS_INTERVAL'] = 5
    return app

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

@pytest.fixture
def service(app_context):
    zeevClient = Mock()
    processedRequestRepository = Mock()
    profileRepository = Mock()
    profileRepository.insert_profile_document.return_value = Mock(inserted_id=1)
    extractRepository = Mock()
    paymentRepository = Mock()
    paymentRepository.get_last_id.return_value = "1234"
    contractRepository = Mock()
    clickSignClient = Mock()
    contractService = ContractsService(
        zeevClient, processedRequestRepository, clickSignClient, 
        profileRepository, extractRepository, paymentRepository, 
        contractRepository
    )
    return contractService, profileRepository, extractRepository, paymentRepository, contractRepository

def convert_to_utc_date(date_string):
    date_format = "%d/%m/%Y"
    local_date = datetime.strptime(date_string, date_format)
    local_date = local_date.replace(tzinfo=pytz.UTC)
    return local_date

@freeze_time("2023-01-01")
def test_should_read_and_insert_data_correctly(mocker, service):
    contractsService, profileRepository, extractRepository, paymentRepository, contractRepository = service

    assert contractsService is not None, "contractsService is not initialized"
    assert profileRepository is not None, "profileRepository is not initialized"
    assert extractRepository is not None, "extractRepository is not initialized"
    assert paymentRepository is not None, "paymentRepository is not initialized"
    assert contractRepository is not None, "contractRepository is not initialized"

    response = create_response_with_csv()
    spyInsertProfile = mocker.spy(profileRepository, 'insert_profile_document')
    spyInsertExtract = mocker.spy(extractRepository, 'insert_extract_document')
    spyInsertPayment = mocker.spy(paymentRepository, 'insert_payment_document')
    spyInsertContract = mocker.spy(contractRepository, 'insert_contract_document')

    contractRepository.cod_already_exists = MagicMock(return_value=False)

    contractsService.insert_contracts(response)

    assert spyInsertProfile.call_args == call(
        {
            'name': 'IZA CHOZE', 
            'email': 'I.CHOZE@HOTMAIL.COM', 
            'birthdate': convert_to_utc_date("13/04/1964"), 
            'phone': '5562981471221', 
            'cpfcnpj': '35520574120', 
            'jobPosition': '', 
            'address': 'RUA T29 N 1101 APTO 804 ED BRISA DO IPÊ ', 
            'neighborhood': 'BUENO', 
            'zipCode': '74210050', 
            'city': 'GOIÂNIA', 
            'state': 'GO', 
            'financialAssets': 0.0, 
            'budgetProfile': '', 
            'residenceProperty': '', 
            'maritalStatus': False, 
            'primaryProfession': '', 
            'businessSector': '', 
            'consenting.name': '-', 
            'consenting.email': '-', 
            'consenting.birthdate': '-', 
            'consenting.phone': '-', 
            'consenting.cpfCnpj': '-'
        }
    )
    
    assert spyInsertProfile.call_count == 1

    assert spyInsertContract.call_args == call(
        {   
            "cod": 110001.0,
            "closer": "MAURÍCIO VONO",
            "profileId": 1,
            "status": "DESCONHECIDO",
            "contractType": "GROW",
            "aum.estimated": 0.0,
            "aum.actual": 0.0,
            "implantation": 500.0,
            "firstPaymentDate": convert_to_utc_date("05/02/2022"),
            "implantationPaymentMethod": "CARTÃO",
            "implantationInstallment": 1,
            "minimalFee": 500.0,
            "deadline": 12.0,
            "debtDay": "05",
            "brokerPermission": False,
            "rootContractCode": 0.0,
            "accountNumber.cpf": "35520574120",
            'sourceAcquisition': 1,
        }
    )
    assert spyInsertContract.call_count == 1

    print(spyInsertPayment.call_args)
    fake_datetime = FakeDatetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert spyInsertPayment.call_args == call(
        {   
            "cod": 110001.0,
            "payer.name": "IZA CHOZE",
            "payer.CPFCNPJ": "35520574120",
            "value": 500.0,
            "dueDate": formatting.convert_to_utc_date("05/12/2025"),
            "status": "INATIVO",
            "currency": "BRL",
            "createdAt": fake_datetime, 
            "paymentMethod": "CARTÃO"
        }
    )
    assert spyInsertPayment.call_count == 96

    assert spyInsertExtract.call_args == call(
        {   
            'paymentId': "1234",
            "cod": 110001.0,
            "payer.name": "IZA CHOZE",
            "payer.CNPJCPF": "35520574120",
            "planners.name": "DESCONHECIDO",
            "aum.estimated": 0.0,
            "aum.actual": 0.0,
            "mrr": 0.0,
            "dueDate": "05/12/2025",
            "paymentDate": "05/12/2025",
            "value": 500.0,
            "implementedPayment": 0.0,
            "status": "INATIVO",
            "currency": "BRL",
            "createdAt":fake_datetime,
            "paymentMethod": "CARTÃO",
            "income": 0.0,
            "budgetProfile": "",
        }
    )
    assert spyInsertExtract.call_count == 96
