import pytest
from unittest.mock import Mock
from application import app as appRoot
from application.extensions import database

@pytest.fixture()
def app():
    database.init_app = Mock()
    app = appRoot.create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()