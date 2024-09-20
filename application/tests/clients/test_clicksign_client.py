from unittest.mock import MagicMock
from application.blueprints.clients.clicksignClient import ClicksignClient
import pytest
from flask import Flask


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["PHONE_NUMBER_DEBUG"] = "123456789"
    app.config["CONTRACTS_PROCESSING_DAYS_INTERVAL"] = 5
    app.config["CLICKSIGN_BASE_URL"] = "https://api.clicksign.com"
    app.config["CLICKSIGN_TOKEN"] = "token"

    return app


def test_should_define_correctly_contractor(app):
    # Ativar o contexto da aplicação
    with app.app_context():
        clicksignClient = ClicksignClient()

        clicksignClient.addQualificationRequirements = MagicMock()
        clicksignClient.addQualificationRequirements(
            "envelopeId", "signerId", "documentId", "contractor"
        )
        clicksignClient.addQualificationRequirements.assert_called_with(
            "envelopeId", "signerId", "documentId", "contractor"
        )


def test_should_define_correctly_contratee_and_contractor_default_role(app):
    with app.app_context():
        clicksignClient = ClicksignClient()

        clicksignClient.addQualificationRequirements = MagicMock()
        clicksignClient.addQualificationRequirements(
            "envelopeId", "signerId", "documentId"
        )
        args, kwargs = clicksignClient.addQualificationRequirements.call_args
        assert args == ("envelopeId", "signerId", "documentId")
        assert kwargs == {}
        clicksignClient.addQualificationRequirements.assert_called_with(
            "envelopeId", "signerId", "documentId"
        )
