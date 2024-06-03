import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
from flask import Flask
from mongomock import MongoClient
import logging
from application.tests.populate import zeev_responses

from application.blueprints.services.contracts import ContractsService  # Atualize com o caminho correto
from application.blueprints.utils import formatting, dataProcessing
# Função auxiliar para criar uma instância da classe ContractsService com mocks

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

def test_processContract(service, mocker):
    contractService, zeevClient, processedRequestRepository, clickSignClient = service
    zeevClient.getContractsRequestsByDate = MagicMock(return_value=zeev_responses.response)
    # contractService._processContractSteps = MagicMock(return_value=("workType", ["documentId"]))
    
    result = contractService.processAllContracts()
    
    # Verifique se o resultado é o esperado
    # assert result == ("workType", ["documentId"])
    # service._processContractSteps.assert_called_once_with(
    #     {"name": "qualOTipoDeTrabalho", "value": "grow"}, 
    #     # mocker.ANY, 
    #     "Grow"
    # )