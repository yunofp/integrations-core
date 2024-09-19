import pytest
from unittest.mock import MagicMock, Mock, patch
from application.extensions import database
from application.blueprints.services.contracts import ContractsService
from application.blueprints.utils import date
from application.blueprints.services.business_service import BusinessService
from application.blueprints.services.performance_service import PerformanceService


@pytest.fixture
def business_service():
    mock_contract_repository = MagicMock()
    mock_entries_repository = MagicMock()
    mock_goals_repository = MagicMock()
    mock_indications_repository = MagicMock()

    return BusinessService(
        mock_contract_repository,
        mock_entries_repository,
        mock_goals_repository,
        mock_indications_repository,
    )


@pytest.fixture
def mock_indications_repository():
    return MagicMock()


@pytest.fixture
def mock_goals_repository():
    return MagicMock()


@pytest.fixture
def performance_service(mock_indications_repository, mock_goals_repository):
    return PerformanceService(mock_indications_repository, mock_goals_repository)


@pytest.fixture(scope="session", autouse=True)
def mock_mongo():
    with patch("application.extensions.database.MongoClient") as MockMongoClient:
        mock_client = MockMongoClient.return_value
        mock_client.get_database.return_value = Mock()

        def mock_init_app(app, client=mock_client):
            app.db = mock_client.get_database()

        with patch("application.extensions.database.init_app", new=mock_init_app):
            from application.app import app as flask_app

            yield flask_app


@pytest.fixture
def app(mock_mongo):
    mock_mongo.config.update({"TESTING": True})
    mock_mongo.dbClient = MagicMock()
    with mock_mongo.app_context():
        yield mock_mongo


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def contract_service(app_context):
    profileRepository = Mock()
    profileRepository.insert_one.return_value = Mock(inserted_id=1)
    entriesRepository = Mock()
    contractsRepository = Mock()
    contractsRepository.insert_one.return_value = MagicMock(return_value=12)

    contractService = ContractsService(
        None,
        None,
        None,
        profileRepository,
        entriesRepository,
        contractsRepository,
        None,
    )
    return contractService, profileRepository, entriesRepository, contractsRepository


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def mock_repositories():
    contract_repo = MagicMock()
    entries_repo = MagicMock()
    goals_repo = MagicMock()
    indications_repo = MagicMock()
    return contract_repo, entries_repo, goals_repo, indications_repo


@pytest.fixture
def business_service(mock_repositories):
    contract_repo, entries_repo, goals_repo, indications_repo = mock_repositories
    return BusinessService(contract_repo, entries_repo, goals_repo, indications_repo)
