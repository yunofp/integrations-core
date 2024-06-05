import pytest
from unittest.mock import Mock, call, MagicMock
from flask import Flask
import logging
from application.tests.populate import zeev_responses
from application.blueprints.services.contracts import ContractsService
from application.blueprints.repositories.processedRequestRepository import ProcessedRequestsRepository
from application.blueprints.utils.dataProcessing import defineVariablesGrow, defineVariablesWealth, defineVariablesWork

logger = logging.getLogger(__name__)
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['PHONE_NUMBER_DEBUG'] = '123456789'
    return app

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

@pytest.fixture
def service(app_context):
    zeevClient = Mock()
    processedRequestRepository = Mock()
    clickSignClient = Mock()
    contractService = ContractsService(zeevClient, processedRequestRepository, clickSignClient)
    return contractService, zeevClient, processedRequestRepository, clickSignClient

def test_should_process_sucess_grow_contract(service, mocker):
    contractService, zeevClient, processedRequestRepository, clickSignClient = service
    requestId = zeev_responses.grow_response[0]['id']
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=zeev_responses.grow_response)
    processedRequestRepository.findByRequestId = MagicMock(return_value=False)
    clickSignClient.createEnvelope = MagicMock(return_value=1)
    clickSignClient.sendClickSignPostGrow = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addSignerToEnvelope = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addQualificationRequirements = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addAuthRequirements = MagicMock(return_value={})
    clickSignClient.activateEnvelope = MagicMock(return_value={})
    clickSignClient.notificateEnvelope = MagicMock(return_value={})
    
    spyInsert = mocker.spy(contractService, '_insertSuccessfullyProcessedRequest')  
     
    contractService.processAllContracts()
    
    spyInsert.assert_called_once_with(requestId, 'Grow', [{ 'type': 'Grow', 'id': 1 }])

    assert spyInsert.call_args == call(requestId, 'Grow', [{ 'type': 'Grow', 'id': 1 }])

def test_should_process_sucess_wealth_contract(service, mocker):
    contractService, zeevClient, processedRequestRepository, clickSignClient = service
    requestId = zeev_responses.wealth_response[0]['id']
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=zeev_responses.wealth_response)
    processedRequestRepository.findByRequestId = MagicMock(return_value=False)
    clickSignClient.createEnvelope = MagicMock(return_value=1)
    clickSignClient.sendClickSignPostWealth = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addSignerToEnvelope = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addQualificationRequirements = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addAuthRequirements = MagicMock(return_value={})
    clickSignClient.activateEnvelope = MagicMock(return_value={})
    clickSignClient.notificateEnvelope = MagicMock(return_value={})
    
    spyInsert = mocker.spy(contractService, '_insertSuccessfullyProcessedRequest')  
     
    contractService.processAllContracts()
    
    spyInsert.assert_called_once_with(requestId, 'Wealth', [{ 'type': 'Wealth', 'id': 1 }])

    assert spyInsert.call_args == call(requestId, 'Wealth', [{ 'type': 'Wealth', 'id': 1 }])
    
    
    
def test_should_process_sucess_grow_and_wealth_contract(service, mocker):
    contractService, zeevClient, processedRequestRepository, clickSignClient = service
    
    requestId = zeev_responses.grow_response_wealth_response[0]['id']
  
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=zeev_responses.grow_response_wealth_response)
    processedRequestRepository.findByRequestId = MagicMock(return_value=False)
    clickSignClient.createEnvelope = MagicMock(return_value=1)
    clickSignClient.sendClickSignPostGrow = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.sendClickSignPostWealth = MagicMock(return_value={'data': {'id': 2}})
    clickSignClient.addSignerToEnvelope = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addQualificationRequirements = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addAuthRequirements = MagicMock(return_value={})
    clickSignClient.activateEnvelope = MagicMock(return_value={})
    clickSignClient.notificateEnvelope = MagicMock(return_value={})

    spyInsert = mocker.spy(contractService, '_insertSuccessfullyProcessedRequest')

    # Call the method that processes all contracts
    contractService.processAllContracts()
    # Assert that the _insertSuccessfullyProcessedRequest method was called once with the correct arguments
    spyInsert.assert_called_once_with(requestId, 'Grow & Wealth', [{'type': 'Grow', 'id': 1}, {'type': 'Wealth', 'id': 2}])

    # Additional check to compare call arguments
    assert spyInsert.call_args == call(requestId, 'Grow & Wealth', [{'type': 'Grow', 'id': 1}, {'type': 'Wealth', 'id': 2}])

    
def test_should_process_many_contract(service, mocker):
    contractService, zeevClient, processedRequestRepository, clickSignClient = service
    
    manyContractsReponse = list(zeev_responses.grow_response) + list(zeev_responses.wealth_response) + list(zeev_responses.grow_response_not_filled)
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=manyContractsReponse)
    processedRequestRepository.findByRequestId = MagicMock(return_value=False)
    clickSignClient.createEnvelope = MagicMock(return_value=1)
    clickSignClient.sendClickSignPostGrow = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addSignerToEnvelope = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addQualificationRequirements = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addAuthRequirements = MagicMock(return_value={})
    clickSignClient.activateEnvelope = MagicMock(return_value={})
    clickSignClient.notificateEnvelope = MagicMock(return_value={})
    
    spyInsert = mocker.spy(contractService, '_insertSuccessfullyProcessedRequest')  
    spyInsertFaled = mocker.spy(contractService, '_insertFailedProcessedRequest')
    contractService.processAllContracts()
    assert spyInsert.call_count == 2
    assert spyInsertFaled.call_count == 1
    
def test_should_save_failed_grow_contract_request(service, mocker):
    contractService, zeevClient, processedRequestRepository, clickSignClient = service
    requestId = zeev_responses.grow_response[0]['id']
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=zeev_responses.grow_response)
    processedRequestRepository.findByRequestId = MagicMock(return_value=False)
    clickSignClient.createEnvelope = MagicMock(return_value=1)
    clickSignClient.sendClickSignPostGrow = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addSignerToEnvelope = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addQualificationRequirements = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addAuthRequirements = MagicMock(return_value={})
    clickSignClient.activateEnvelope = MagicMock(side_effect=Exception("api error"))
    clickSignClient.notificateEnvelope = MagicMock(return_value={})
    
    spyInsert = mocker.spy(contractService, '_insertFailedProcessedRequest')  
    
    spyRepository = mocker.spy(processedRequestRepository, 'insertOne')
     
    contractService.processAllContracts()
     
    expectedSaveRequest = spyRepository.call_args[0][0]
    
    assert expectedSaveRequest.get('tryAgain') == True
    assert expectedSaveRequest.get('requestId') == 1150
    assert expectedSaveRequest.get('createdAt') is not None
    assert expectedSaveRequest.get('validNewClient') == True
    assert expectedSaveRequest.get('status') == {'name': 'error', 'description': 'api error'}
    spyInsert.assert_called_once_with(requestId, True, 'api error', 'error', True)
    assert spyInsert.call_args == call(requestId, True, 'api error', 'error', True)

def test_retry_grow_contract_save_on_incomplete_contract(service, mocker):
    contractService, zeevClient, processedRequestRepository, clickSignClient = service
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=zeev_responses.grow_response_not_filled)
    processedRequestRepository.findByRequestId = MagicMock(return_value=False)
    clickSignClient.createEnvelope = MagicMock(return_value=1)
    clickSignClient.sendClickSignPostGrow = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addSignerToEnvelope = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addQualificationRequirements = MagicMock(return_value={'data': {'id': 1}})
    clickSignClient.addAuthRequirements = MagicMock(return_value={})
    clickSignClient.activateEnvelope = MagicMock(return_value={})
    clickSignClient.notificateEnvelope = MagicMock(return_value={})
    
    spyRepository = mocker.spy(processedRequestRepository, 'insertOne')
    
    contractService.processAllContracts()
     
    expectedSaveRequest = spyRepository.call_args[0][0]
    assert expectedSaveRequest.get('tryAgain') == True
    assert expectedSaveRequest.get('requestId') == 1180
    assert expectedSaveRequest.get('createdAt') is not None
    assert expectedSaveRequest.get('validNewClient') == True
    assert expectedSaveRequest.get('status') == {'name': 'waitingFill', 'description': 'Contract not completely filled to process'}

def test_should_get_correct_clicksign_variables_sucess_grow_contract():
    clicksignVariables = defineVariablesGrow(zeev_responses.grow_response[0].get('formFields'))
    
    assert clicksignVariables.get('nomeCompletoDoTitular') == 'Strokes INC.'
    assert clicksignVariables.get('email') == 'tarcisio.campos@yunofp.com.br'
    assert clicksignVariables.get('dataDeNascimento') == '17/05/2004'
    assert clicksignVariables.get('telefoneDoTitular') == '(64)99345-6689'
    assert clicksignVariables.get('cpfDoTitular') == '070-761-681-62'
    assert clicksignVariables.get('endereco') == 'Av 7 De Setembro'
    assert clicksignVariables.get('bairro') == 'Centro'
    assert clicksignVariables.get('cidade') == 'Joviânia'
    assert clicksignVariables.get('uf') == 'GO'
    assert clicksignVariables.get('cep') == '75610-000'
    assert clicksignVariables.get('nomeCompletoDoConjuge') == 'Nikolai Fraiture'
    assert clicksignVariables.get('emailDoConjuge') == 'nikolaifraituressss@gmail.com'
    assert clicksignVariables.get('dataDeNascimentoDoConjuge') == '14/05/1997'
    assert clicksignVariables.get('telefoneDoConjuge') == '(62)99345-6689'
    assert clicksignVariables.get('prazoDeVigencia') == '2'
    assert clicksignVariables.get('closerResponsavel') == 'aristeu'
    assert clicksignVariables.get('origemInterna') == 'Tarcísio Campos'
    assert clicksignVariables.get('origemExterna') == 'ORIGEM EXTERNA'
    assert clicksignVariables.get('valorDaImplantacao') == '400,00'
    assert clicksignVariables.get('dataDoPagamentoDaImplantacao') == '08/05/2024'
    assert clicksignVariables.get('formaDePagamentoDaImplantacao') == 'PIX'
    assert clicksignVariables.get('fee') == '2,00'
    assert clicksignVariables.get('diaDeCobrançaDoFee') == '15'
    assert clicksignVariables.get('observacoes') == 'OBSERVAÇAO'
    
def test_should_get_correct_clicksign_variables_sucess_wealth_contract():
    clicksignVariables = defineVariablesWealth(zeev_responses.wealth_response[0].get('formFields'))

    assert clicksignVariables.get('nomeCompletoDoTitular') == 'Strokes INC.'
    assert clicksignVariables.get('email') == 'tarcisio.campos@yunofp.com.br'
    assert clicksignVariables.get('dataDeNascimento') == '17/05/2004'
    assert clicksignVariables.get('telefoneDoTitular') == '(64)99345-6689'
    assert clicksignVariables.get('cpfDoTitular') == '070-761-681-62'
    assert clicksignVariables.get('endereco') == 'Av 7 De Setembro'
    assert clicksignVariables.get('bairro') == 'Centro'
    assert clicksignVariables.get('cidade') == 'Joviânia'
    assert clicksignVariables.get('uf') == 'GO'
    assert clicksignVariables.get('cep') == '75610-000'
    assert clicksignVariables.get('nomeCompletoDoConjuge') == 'Nikolai Fraiture'
    assert clicksignVariables.get('emailDoConjuge') == 'nikolaifraituressss@gmail.com'
    assert clicksignVariables.get('dataDeNascimentoDoConjuge') == '14/05/1997'
    assert clicksignVariables.get('telefoneDoConjuge') == '(62)99345-6689'
    assert clicksignVariables.get('prazoDeVigencia') == '2'
    assert clicksignVariables.get('closerResponsavel') == 'aristeu'
    assert clicksignVariables.get('origemInterna') == 'Tarcísio Campos'
    assert clicksignVariables.get('origemExterna') == 'ORIGEM EXTERNA'
    assert clicksignVariables.get('valorDaImplantacao') == '400,00'
    assert clicksignVariables.get('dataDoPagamentoDaImplantacao') == '08/05/2024'
    assert clicksignVariables.get('formaDePagamentoDaImplantacao') == 'PIX'
    assert clicksignVariables.get('fee') == '2,00'
    assert clicksignVariables.get('diaDeCobrançaDoFee') == '15'
    assert clicksignVariables.get('observacoes') == 'OBSERVAÇAO'
    assert clicksignVariables.get('cobrancaPelaCorretora') == 'Sim'
    assert clicksignVariables.get('patrimonioFinanceiroEstimado') == '3,00'
    assert clicksignVariables.get('vincularAContratoPai') == 'Sim'
    assert clicksignVariables.get('numeroDoContratoPai') == 'NAO SE APLICA'
    
def test_should_get_correct_clicksign_variables_success_work_contract():    
    clicksignVariables = defineVariablesWork(zeev_responses.work_response[0].get('formFields'))
    
    assert clicksignVariables.get('nomeDaEmpresa') == 'Nikolai Fraiture'
    assert clicksignVariables.get('emailDeContato') == 'tarcisio.campos@yunofp.com.br'
    assert clicksignVariables.get('telefoneDaEmpresa') == '(64)99345-6689'
    assert clicksignVariables.get('cnpj') == '070-761-681-62'
    assert clicksignVariables.get('endereco') == 'Av 7 De Setembro'
    assert clicksignVariables.get('bairro') == 'Centro'
    assert clicksignVariables.get('cidade') == 'Joviânia'
    assert clicksignVariables.get('uf') == ''
    assert clicksignVariables.get('cep') == '75610-000'
    assert clicksignVariables.get('nomeCompletoDoResponsavel') == 'Nikolai Fraiture'
    assert clicksignVariables.get('cargoDoResponsavel') == 'Arquiteto'
    assert clicksignVariables.get('emailDoResponsavel') == 'nikolaifraituressss@gmail.com'
    assert clicksignVariables.get('dataDeNascimentoDoResponsavel') == '14/05/1997'
    assert clicksignVariables.get('cpfDoResponsavel') == '000.000.000-00'
    assert clicksignVariables.get('telefoneDoResponsavel') == '(62)99345-6689'
    assert clicksignVariables.get('prazoDeVigencia') == '2'
    assert clicksignVariables.get('closerResponsavel') == 'aristeu'
    assert clicksignVariables.get('origemInterna') == 'Tarcísio Campos'
    assert clicksignVariables.get('origemExterna') == 'ORIGEM EXTERNA'
    assert clicksignVariables.get('valorDaImplantacão') == '400,00'
    assert clicksignVariables.get('dataDoPagamentoDaImplantacao') == '08/05/2024'
    assert clicksignVariables.get('formaDePagamentoDaImplantacao') == 'PIX'
    assert clicksignVariables.get('fee') == '2,00'
    assert clicksignVariables.get('diaDeCobrançaDoFee') == '15'
    assert clicksignVariables.get('observacoes') == 'OBSERVAÇAO'

def test_should_not_process_saved_request(service, mocker):
    contractService, zeevClient, processedRequestRepository, clickSignClient = service
    
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=zeev_responses.grow_response)
    processedRequestRepository.findByRequestId = MagicMock(return_value=True)
    
    spyInsert = mocker.spy(contractService, '_insertSuccessfullyProcessedRequest')  
    spyInsertFaled = mocker.spy(contractService, '_insertFailedProcessedRequest')
    contractService.processAllContracts()
    assert spyInsert.call_count == 0
    assert spyInsertFaled.call_count == 0
    
   
     
        

    
    