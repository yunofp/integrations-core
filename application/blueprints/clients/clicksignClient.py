import requests
import json
from flask import current_app as app
import logging

logger = logging.getLogger(__name__)

class ClicksignClient:
    def __init__(self):
        self.config = app.config
        self.token = self.config['CLICKSIGN_TOKEN']
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': self.token
        }
        self.clickSignBaseUrl= self.config['CLICKSIGN_BASE_URL']
    
    def createEnvelope(self, requestId):
    
        url = self.clickSignBaseUrl+"/envelopes/"

        data = {
            "data": {
                "type": "envelopes",
                "attributes": {
                        "name": "Envelope for request: " + str(requestId),
                        "locale": "pt-BR"
                }
            }
        }

        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def sendClickSignPostGrow(self, dataVariables, envelopeId, filename):
            url = self.clickSignBaseUrl+ "/envelopes/" + envelopeId + "/documents"

            data = {
                "data":{
                    "type":"documents",
                    "attributes":{
                    "filename":str(filename),
                    "template":{
                        "key":"CED357E0-5BC9-4D11-9EA1-17D8CB700950",
                        "data": dataVariables
                        }
                    }
                }
            }

            response = requests.post(url, json=data, headers=self.headers)

            return response.json()

    def sendClickSignPostWealth(self, dataVariables, envelopeId, filename):
            url = self.clickSignBaseUrl+ "/envelopes/" + envelopeId + "/documents"

            data = {
                "data":{
                    "type":"documents",
                    "attributes":{
                    "filename":str(filename),
                    "template":{
                        "key":"3204EFD1-12CB-4F41-9263-B38EABD14947",
                        "data": dataVariables
                        }
                    }
                }
            }

            response = requests.post(url, json=data, headers=self.headers)
            return response.json()

    def sendClickSignPostWork(self, dataVariables, envelopeId, filename):
            url = self.clickSignBaseUrl+ "/envelopes/" + envelopeId + "/documents"
    
            data = {
                "data":{
                    "type":"documents",
                    "attributes":{
                    "filename":str(filename),
                    "template":{
                        "key":"C200914F-3546-4512-8BF2-31DE1D99CA70",
                        "data": dataVariables
                        }
                    }
                }
            }

            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
    def addSignerToEnvelope(self, envelopeId, name, cpf=None, birthdate=None, phoneNum=None, email=None, signatureRequest="whatsapp", documentSigned="whatsapp"):
        url = self.clickSignBaseUrl + "/envelopes/" + envelopeId + "/signers"
        
        attributes = {
            "name": name,
            "refusable": True,
            "communicate_events": {
                "document_signed": documentSigned,
                "signature_request": signatureRequest
            }
        }
        
      
        attributes["has_documentation"] = False
            
        if email:
            attributes["email"] = email
        if phoneNum:
            attributes["phone_number"] = phoneNum
        
        data = {
            "data": {
                "type": "signers",
                "attributes": attributes
            }
        }

        response = requests.post(url, json=data, headers=self.headers)

        return response.json()


  
    def addQualificationRequirements(self, envelopeId, signerId, documentId):
            url = self.clickSignBaseUrl + "/envelopes/" + envelopeId + "/requirements"
            data = {
                "data": {
                    "type": "requirements",
                    "attributes": {
                        "action": "agree",
                        "role": "intervening"
                    },
                    "relationships": {
                        "document":{
                        "data": { "type": "documents", "id": documentId}
                        },
                        "signer":{
                            "data": { "type": "signers", "id": signerId}
                        }
                    }
                }
            }

            response = requests.post(url, json=data, headers=self.headers)
            return response.json()

    def addAuthRequirements(self, envelopeId, signerId, documentId):
        try:
            url = self.clickSignBaseUrl + "/envelopes/" + envelopeId + "/requirements"

            data = {
                "data": {
                    "type": "requirements",
                    "attributes": {
                        "action": "provide_evidence",
                        "auth": "whatsapp"
                    },
                    "relationships": {
                        "document": {
                            "data": { "type": "documents", "id": documentId}
                        },
                        "signer": {
                            "data": { "type": "signers", "id": signerId}
                        }
                    }
                }
            }

            response = requests.post(url, json=data, headers=self.headers)
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                csResponse = json.loads(json_response)

        except requests.exceptions.RequestException as e:
            json_response = response.text.replace("'", '"')
            logger.error("addAuthRequirements: Error while sending document: " + str(e))
            raise   

    def activateEnvelope(self, envelopeId):
        try:
        
            url = self.clickSignBaseUrl + "/envelopes/" + envelopeId

            data = {
                "data": {
                    "id": envelopeId,
                    "type": "envelopes",
                    "attributes": {
                    "status": "running",
                    "name": "Integraçao Zeev Clicksign",
                    "locale": "pt-BR",
                    "auto_close": True,
                    "block_after_refusal": True,
                    }
                }
            }

            response = requests.patch(url, json=data, headers=self.headers)
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                csResponse = json.loads(json_response)
        except requests.exceptions.RequestException as e:
            json_response = response.text.replace("'", '"')
            csResponse = json.loads(json_response)
            logger.error("activateEnvelope: Error while sending document: " + str(e) + " " + str(csResponse))
            raise

    
    def notificateEnvelope(self, envelopeId):
        try:

            url = self.clickSignBaseUrl + "/envelopes/" + envelopeId + "/notifications"

            data = {
                "data": {
                    "type": "notifications",
                    "attributes": {
                        "message": "YUNO CS"
                    }
                }
            }

            response = requests.post(url, json=data, headers=self.headers)
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                csResponse = json.loads(json_response)
        except requests.exceptions.RequestException as e:
            json_response = response.text.replace("'", '"')
            csResponse = json.loads(json_response)
            logger.error("notificateEnvelope: Error while sending document: " + str(e) + " " + str(csResponse))
            raise
            
