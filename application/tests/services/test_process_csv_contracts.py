from unittest.mock import call, MagicMock
from freezegun import freeze_time
from datetime import datetime, timezone
import numpy as np
from application.tests.utils.date import utils_test_convert_to_utc_date
from application.tests.populate.csv_response import create_response_with_csv

@freeze_time("2023-01-01")
def test_should_read_and_insert_data_correctly(mocker, service, app):
    contractsService, ProfileRepository, EntriesRepository, ContractRepository = service

    assert contractsService is not None, "contractsService is not initialized"

    response = create_response_with_csv()

    spyInsertProfile = mocker.spy(ProfileRepository, 'insert_one')
    spyInsertEntry = mocker.spy(EntriesRepository, 'insert_many')
    spyInsertContract = mocker.spy(ContractRepository, 'insert_one')

    session_mock = app.dbClient.start_session().__enter__()

    contractsService.cod_already_exists = MagicMock(return_value=False)
    mock_insert_one = MagicMock(return_value=12)
    
    def spy_and_return(*args, **kwargs):
        spyInsertContract(*args, **kwargs)
        return mock_insert_one(*args, **kwargs)

    ContractRepository.insert_one = spy_and_return

    contractsService.insert_contracts(response)

    assert_profile_insertion(spyInsertProfile, session_mock)
    assert_contract_insertion(spyInsertContract, session_mock)
    assert_entry_insertion(spyInsertEntry)

def assert_profile_insertion(spyInsertProfile, session_mock):
    expected_profile_call = call(
        {
            'name': 'CLARISSA BONAFÉ GASPAR RUAS',
            'email': 'CBGRUAS@GMAIL.COM',
            'birthdate': utils_test_convert_to_utc_date('27/11/1984'),
            'phone': '5562994388448',
            'cpf_cnpj': '33850545830',
            'job_position': '',
            'address': 'AV. DR OLINDO RUSSOLO, N 380, CASA 06, PORTAL DO LAGO',
            'neighborhood': 'PORTAL DO LAGO',
            'zip_code': '13607568',
            'city': 'ARARAS',
            'state': 'SP',
            'financial_assets': 0.0,
            'budget_profile': '',
            'residence_property': '',
            'marital_status': False,
            'primary_profession': '',
            'business_sector': '',
            'consenting': {'name': None, 'email': None, 'birthdate': None, 'phone': None, 'cpf': None}
        },
        session_mock
    )
    assert spyInsertProfile.call_args == expected_profile_call
    assert spyInsertProfile.call_count == 1

def assert_contract_insertion(spyInsertContract, session_mock):
    expected_contract_call = call(
        {
            'code': 110002.0,
            'closer': 'JOÃO GONDIM',
            'profile_id': 1,
            'source_acquisition': 1,
            'status': 'A definir',
            'type': 'GROW',
            'aum': {'estimated': 0.0, 'actual': 0.0},
            'implantation': 250.0,
            'first_implantation_payment_date': utils_test_convert_to_utc_date('10/01/2018'),
            'first_payment_date': utils_test_convert_to_utc_date('10/01/2018'),
            'implantation_payment_method': 'CARTÃO',
            'implantation_installment': 1,
            'minimal_fee': 250.0,
            'deadline': 12.0,
            'debt_day': 15,
            'broker_permission': False,
            'root_contract_code': 0.0,
            'account': {'number': 0, 'cpf_cnpj': '33850545830'},
        },
        session_mock
    )
    assert spyInsertContract.call_args == expected_contract_call
    assert spyInsertContract.call_count == 1
    
def assert_entry_insertion(spyInsertEntry):
    due_date = datetime(2018, 1, 1, 2, 0, tzinfo=timezone.utc)
    payment_date = datetime(2018, 1, 1, 2, 0, tzinfo=timezone.utc)
    created_at = datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc)

    assert spyInsertEntry.call_args is not None, "insert_many was not called"
    call_args = spyInsertEntry.call_args[0][0] 
    assert isinstance(call_args, list), "The argument passed is not a list"

    expected_length = 86 
    assert len(call_args) == expected_length, f"Expected list length {expected_length}, but got {len(call_args)}"

    assert call_args[0].get('due_date') == due_date
    assert call_args[0].get('contract_id') == 12
    assert call_args[0].get('code') == np.float64(110002.0)
    assert call_args[0].get('payer').get('name') == 'CLARISSA BONAFÉ GASPAR RUAS'
    assert call_args[0].get('payer').get('cpf') == '33850545830'
    assert call_args[0].get('planners')[0].get('name') == 'JOÃO GONDIM'
    assert call_args[0].get('aum').get('estimated') == 0.0
    assert call_args[0].get('aum').get('actual') == 0.0
    assert call_args[0].get('payment_date') == payment_date
    assert call_args[0].get('value') == 250.0
    assert call_args[0].get('implemented_payment') == 0.0
    assert call_args[0].get('status') == 'approved'
    assert call_args[0].get('currency') == 'BRL'
    assert call_args[0].get('created_at') == created_at
    assert call_args[0].get('payment_method') == 'CARTÃO'
    assert call_args[0].get('income') == ''
    assert call_args[0].get('budget_profile') == ''
    assert call_args[0].get('cancel_day') == ''
