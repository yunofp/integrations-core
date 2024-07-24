import pytest
from unittest.mock import Mock, call
import pandas as pd
import os
from application.blueprints.services.reserv_contracts import ContractsService

@pytest.fixture
def app_context():
    # Mock ou inicialização real do contexto da aplicação
    return Mock()

@pytest.fixture
def sample_df():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'file.csv')
    df = pd.read_csv(csv_path)
    return df.iloc[11:13]

@pytest.fixture
def service(app_context):
    zeevClient = Mock()
    processedRequestRepository = Mock()
    profileRepository = Mock()
    extractRepository = Mock()
    paymentRepository = Mock()
    contractRepository = Mock()
    clickSignClient = Mock()
    # importação do serviço que insere contratos da planilha
    contractService = ContractsService(
        zeevClient, processedRequestRepository, clickSignClient, 
        profileRepository, extractRepository, paymentRepository, 
        contractRepository
    )
    return contractService, profileRepository

def test_should_read_and_insert_data_correctly(mocker, service):
    contractsService, profileRepository = service
    # Corrigir para o seu serviço corretamente
    # acrescentar outros repositórios dentro de service para colocar spy
    # Abrir o arquivo manualmente e deixar apenas uma linha para inserção.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv = os.path.join(current_dir, 'file.csv')
    spyInsertProfile = mocker.spy(profileRepository, 'insert_profile_document')
    # spyInsertContract 
    # spyInsertPayment
    contractsService.insert_contracts(csv) # Chamando a função do serviço
    print(spyInsertProfile.call_args) # ver o resultado desse print para validar

    assert spyInsertProfile.call_args == call(
        # profile_dict
        {'name': 'Tarcísio', 'email': 'tarcisio@yunofp.com.br'}
        # parâmetros que devem chegar dentro da função do repositório
    )
    assert spyInsertProfile.call_count == 100

    # colocar asserts que validam as chamadas das funções de inserção.
