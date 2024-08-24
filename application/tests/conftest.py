import pytest
from unittest.mock import MagicMock, Mock, patch
from application.extensions import database
from application.blueprints.services.contracts import ContractsService
@pytest.fixture(scope='session', autouse=True)
def mock_mongo():
    with patch('application.extensions.database.MongoClient') as MockMongoClient:
        mock_client = MockMongoClient.return_value
        mock_client.get_database.return_value = Mock()

        def mock_init_app(app, client=mock_client):
            app.db = mock_client.get_database()

        with patch('application.extensions.database.init_app', new=mock_init_app):
            from application.app import app as flask_app

            yield flask_app
            

@pytest.fixture
def app(mock_mongo):
    mock_mongo.config.update({
        "TESTING": True
    })
    mock_mongo.dbClient = MagicMock()
    with mock_mongo.app_context():
        yield mock_mongo
        
@pytest.fixture
def app_context(app):
    with app.app_context():
        yield
        
@pytest.fixture
def service(app_context):
    profileRepository = Mock()
    profileRepository.insert_one.return_value = Mock(inserted_id=1)
    entriesRepository = Mock()
    contractsRepository = Mock()
    contractsRepository.insert_one.return_value = MagicMock(return_value=12)
    
    contractService = ContractsService(None, None, None, profileRepository, entriesRepository, contractsRepository, None)
    return contractService, profileRepository, entriesRepository, contractsRepository

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
