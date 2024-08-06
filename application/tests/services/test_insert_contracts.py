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
    app.dbClient = MagicMock()
    return app

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

@pytest.fixture
def service(app_context, mocker):
    zeevClient = Mock()
    processedRequestRepository = Mock()
    ProfileRepository = Mock()
    ProfileRepository.insert_one.return_value = Mock(inserted_id=1)
    EntriesRepository = Mock()
    PaymentRepository = Mock()
    PaymentRepository.insert_one.return_value = "1234"
    ContractRepository = Mock()
    clickSignClient = Mock()
    contractService = ContractsService(
        zeevClient, processedRequestRepository, clickSignClient, 
        ProfileRepository, EntriesRepository, PaymentRepository, 
        ContractRepository
    )
    return contractService, ProfileRepository, EntriesRepository, PaymentRepository, ContractRepository

def convert_to_utc_date(date_string):
    date_format = "%d/%m/%Y"
    local_date = datetime.strptime(date_string, date_format)
    local_date = local_date.replace(tzinfo=pytz.UTC)
    return local_date

def is_utc(date):
    return date.tzinfo is not None and date.tzinfo.utcoffset(date) == timezone.utc.utcoffset(date)

@freeze_time("2023-01-01")
def test_should_read_and_insert_data_correctly(mocker, service, app):
    contractsService, ProfileRepository, EntriesRepository, PaymentRepository, ContractRepository = service

    assert contractsService is not None, "contractsService is not initialized"
    assert ProfileRepository is not None, "ProfileRepository is not initialized"
    assert EntriesRepository is not None, "EntriesRepository is not initialized"
    assert PaymentRepository is not None, "PaymentRepository is not initialized"
    assert ContractRepository is not None, "ContractRepository is not initialized"

    response = create_response_with_csv()

    spyInsertProfile = mocker.spy(ProfileRepository, 'insert_one')
    spyInsertEntry = mocker.spy(EntriesRepository, 'insert_one')
    spyInsertPayment = mocker.spy(PaymentRepository, 'insert_one')
    spyInsertContract = mocker.spy(ContractRepository, 'insert_one')

    session_mock = app.dbClient.start_session().__enter__()

    contractsService.cod_already_exists = MagicMock(return_value=False)

    contractsService.insert_contracts(response)

    expected_profile_call = call(
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
        },
        session_mock
    )

    assert spyInsertProfile.call_args == expected_profile_call
    assert spyInsertProfile.call_count == 1

    expected_contract_call = call(
        {   
            "code": 110001.0,
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
        },
        session_mock
    )

    assert spyInsertContract.call_args == expected_contract_call
    assert spyInsertContract.call_count == 1

    fake_datetime = FakeDatetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc)
    
    expected_payment_call = call(
        {   
            "code": 110001.0,
            "payer.name": "IZA CHOZE",
            "payer.CPFCNPJ": "35520574120",
            "value": 500.0,
            "dueDate": "05/12/2025",
            "status": "INATIVO",
            "currency": "BRL",
            "createdAt": fake_datetime,
            "paymentMethod": "CARTÃO"
        },
        session_mock
    )
    
    assert spyInsertPayment.call_args == expected_payment_call
    assert spyInsertPayment.call_count == 96

    expected_entry_call = call(
        {   
            'paymentId': "1234",
            "code": 110001.0,
            "payer.name": "IZA CHOZE",
            "payer.CNPJCPF": "35520574120",
            "planners.name": "DESCONHECIDO",
            "aum.estimated": 0.0,
            "aum.actual": 0.0,
            "mrr": 0.0,
            "dueDate": convert_to_utc_date("05/12/2025"),
            "paymentDate": "05/12/2025",
            "value": 500.0,
            "implementedPayment": 0.0,
            "status": "INATIVO",
            "currency": "BRL",
            "createdAt":fake_datetime,
            "paymentMethod": "CARTÃO",
            "income": 0.0,
            "budgetProfile": "",
        },
        session_mock
    )
    
    assert spyInsertEntry.call_args == expected_entry_call
    assert spyInsertEntry.call_count == 96

    profile_data = spyInsertProfile.call_args[0][0]
    assert is_utc(profile_data['birthdate']), "Birthdate should be in UTC format"

    contract_data = spyInsertContract.call_args[0][0]
    assert is_utc(contract_data['firstPaymentDate']), "FirstPaymentDate should be in UTC format"

    payment_data = spyInsertPayment.call_args[0][0]
    assert is_utc(payment_data['createdAt']), "CreatedAt should be in UTC format"

    entry_data = spyInsertEntry.call_args[0][0]
    assert is_utc(entry_data['createdAt']), "CreatedAt should be in UTC format"
