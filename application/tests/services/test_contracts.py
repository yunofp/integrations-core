import pytest
from unittest.mock import Mock, call, MagicMock
from flask import Flask
import logging
from application.tests.populate import zeev_responses
from application.blueprints.services.contracts import ContractsService
from application.blueprints.utils.dataProcessing import defineVariablesGrow

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
    requestId = zeev_responses.response[0]['id']
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=zeev_responses.response)
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
    
    spyInsert.assert_called_once_with(requestId, 'Grow', [1])

    assert spyInsert.call_args == call(requestId, 'Grow', [1])

def test_should_get_correct_clicksign_variables_sucess_grow_contract(service, mocker):
    clicksignVariables = defineVariablesGrow(zeev_responses.response[0].get('formFields'))
    
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
    assert clicksignVariables.get('closerResponsavel') == ''
    assert clicksignVariables.get('origemInterna') == 'Tarcísio Campos'
    assert clicksignVariables.get('origemExterna') == 'ORIGEM EXTERNA'
    assert clicksignVariables.get('valorDaImplantacao') == '400,00'
    assert clicksignVariables.get('dataDoPagamentoDaImplantacao') == '08/05/2024'
    assert clicksignVariables.get('formaDePagamentoDaImplantacao') == 'PIX'
    assert clicksignVariables.get('fee') == '2,00'
    assert clicksignVariables.get('diaDeCobrançaDoFee') == '15'
    assert clicksignVariables.get('observacoes') == ''

    
    