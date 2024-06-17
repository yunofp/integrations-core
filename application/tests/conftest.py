import pytest
from unittest.mock import Mock, patch
from application.extensions import database

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

@pytest.fixture()
def app(mock_mongo):
    mock_mongo.config.update({
        "TESTING": True
    })
    with mock_mongo.app_context():
        yield mock_mongo

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
