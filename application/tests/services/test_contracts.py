import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from flask import Flask

from application.blueprints.services.contracts import ContractsService  # Atualize com o caminho correto
from application.blueprints.utils import formatting, dataProcessing
# Função auxiliar para criar uma instância da classe ContractsService com mocks
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
    service = ContractsService(zeevClient, processedRequestRepository, clickSignClient)
    return service, zeevClient, processedRequestRepository, clickSignClient

def test_list_many_retries_success(service):
    service, zeevClient, processedRequestRepository, clickSignClient = service
    expected_result = ["retry1", "retry2"]
    processedRequestRepository.getManyRetries.return_value = expected_result

    result = service.listManyRetries()
    
    assert result == expected_result
    processedRequestRepository.getManyRetries.assert_called_once()

# def test_list_many_retries_exception():
#     service, zeevClient, processedRequestRepository, clickSignClient = create_service()
#     processedRequestRepository.getManyRetries.side_effect = Exception("Error")

#     result = service.listManyRetries()

#     assert result is None
#     processedRequestRepository.getManyRetries.assert_called_once()

# def test_process_contract_grow():
#     service, zeevClient, processedRequestRepository, clickSignClient = create_service()
#     requestId = "request1"
#     contractValues = [{"name": "qualOTipoDeTrabalho", "value": "Grow"}]

#     clickSignClient.createEnvelope.return_value = "envelope1"
#     dataProcessing.defineVariablesGrow.return_value = {"key": "value"}
#     clickSignClient.sendClickSignPostGrow.return_value = {"data": {"id": "document1"}}
#     clickSignClient.addSignerToEnvelope.return_value = {"data": {"id": "signer1"}}
#     clickSignClient.addQualificationRequirements.return_value = {"data": {"id": "qual1"}}

#     with patch("mymodule.services.formatting.formatServiceType", return_value="Grow"), \
#          patch("mymodule.services.formatting.clearPhoneNum", return_value="123456789"), \
#          patch("mymodule.services.formatting.formatFilename", return_value="filename"), \
#          patch("mymodule.services.formatting.formatCpf", return_value="cpf"), \
#          patch("mymodule.services.formatting.formatBirthdate", return_value="birthdate"):
#         serviceType, documentsId = service.processContract(requestId, contractValues)

#     assert serviceType == "Grow"
#     assert documentsId == ["document1"]

# def test_process_contract_no_work_type():
#     service, zeevClient, processedRequestRepository, clickSignClient = create_service()
#     requestId = "request1"
#     contractValues = []

#     with pytest.raises(Exception, match="processContract | No work type found for request:request1"):
#         service.processContract(requestId, contractValues)

# def test_run_try_again():
#     service, zeevClient, processedRequestRepository, clickSignClient = create_service()
#     processedRequestRepository.getManyRetries.return_value = [{"requestId": "request1"}]
#     zeevClient.generateZeevToken.return_value = "token"
#     zeevClient.secondStepContractPost.return_value = [{"formFields": [{"value": True}]}]
    
#     with patch.object(service, 'processContract', return_value=("Grow", ["document1"])), \
#          patch.object(service, '_updateSuccessfullyProcessedRequest') as mock_update:
#         service.runTryAgain()

#     mock_update.assert_called_once_with("request1", "Grow", ["document1"])

# def test_process_all_contracts():
#     service, zeevClient, processedRequestRepository, clickSignClient = create_service()
#     now = datetime(2024, 5, 29, tzinfo=timezone.utc)
#     contractsRequests = [
#         {'id': 'request1', 'formFields': [{'name': 'valorDoFEE', 'value': 100}]}
#     ]

#     zeevClient.generateZeevToken.return_value = "token"
#     zeevClient.getContractsRequestsByDate.return_value = contractsRequests
#     processedRequestRepository.findByRequestId.return_value = None
#     dataProcessing.findByName.return_value = True

#     with patch("mymodule.services.formatting.formatServiceType", return_value="Grow"), \
#          patch.object(service, 'processContract', return_value=("Grow", ["document1"])), \
#          patch.object(service, '_insertSuccessfullyProcessedRequest') as mock_insert:
#         service.processAllContracts()

#     mock_insert.assert_called_once_with("request1", "Grow", ["document1"])

