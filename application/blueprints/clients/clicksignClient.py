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
                        "data":{
                            "Nome Completo do Titular":dataVariables.get("nomeCompletoDoTitular"),
                            "Email":dataVariables.get("email"),
                            "Data de Nascimento":dataVariables.get("dataDeNascimento"),
                            "Telefone do Titular":dataVariables.get("telefoneDoTitular"),
                            "CPF do Titular":dataVariables.get("cpfDoTitular"),
                            "Endereço":dataVariables.get("endereco"),
                            "Bairro":dataVariables.get("bairro"),
                            "Cidade":dataVariables.get("cidade"),
                            "UF":dataVariables.get("uf"),
                            "CEP":dataVariables.get("cep"),
                            "Nome Completo do Cônjuge":dataVariables.get("nomeCompletoDoConjuge"),
                            "Email do Cônjuge":dataVariables.get("emailDoConjuge"),
                            "Data de Nascimento do Cônjuge":dataVariables.get("dataDeNascimentoDoConjuge"),
                            "Telefone do Cônjuge":dataVariables.get("telefoneDoConjuge"),
                            "Prazo de Vigência":dataVariables.get("prazoDeVigencia"),
                            "Closer Responsável":dataVariables.get("closerResponsavel"),
                            "Origem Interna":dataVariables.get("origemInterna"),
                            "Origem Externa":dataVariables.get("origemExterna"),
                            "Valor da Implantação":dataVariables.get("valorDaImplantacao"),
                            "Data do Pagamento da Implantação":dataVariables.get("dataDoPagamentoDaImplantacao"),
                            "Forma de Pagamento da Implantação":dataVariables.get("formaDePagamentoDaImplantacao"),
                            "Fee":dataVariables.get("fee"),
                            "Dia da Cobrança do Fee":dataVariables.get("diaDeCobrancaDoFee"),
                            "Observações":dataVariables.get("observacoes")          
                            }
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
                        "data":{
                            "Nome Completo do Titular":dataVariables.get("nomeCompletoDoTitular"),
                            "Email":dataVariables.get("email"),
                            "Data de Nascimento":dataVariables.get("dataDeNascimento"),
                            "Telefone do Titular":dataVariables.get("telefoneDoTitular"),
                            "CPF do Titular":dataVariables.get("cpfDoTitular"),
                            "Endereço":dataVariables.get("endereco"),
                            "Bairro":dataVariables.get("bairro"),
                            "Cidade":dataVariables.get("cidade"),
                            "UF":dataVariables.get("uf"),
                            "CEP":dataVariables.get("cep"),
                            "Nome Completo do Cônjuge":dataVariables.get("nomeCompletoDoConjuge"),
                            "Email do Cônjuge":dataVariables.get("emailDoConjuge"),
                            "Data de Nascimento do Cônjuge":dataVariables.get("dataDeNascimentoDoConjuge"),
                            "Telefone do Cônjuge":dataVariables.get("telefoneDoConjuge"),
                            "Prazo de Vigência":dataVariables.get("prazoDeVigencia"),
                            "Closer Responsável":dataVariables.get("closerResponsavel"),
                            "Origem Interna":dataVariables.get("origemInterna"),
                            "Origem Externa":dataVariables.get("origemExterna"),
                            "Valor da Implantação":dataVariables.get("valorDaImplantacao"),
                            "Data do Pagamento da Implantação":dataVariables.get("dataDoPagamentoDaImplantacao"),
                            "Forma de Pagamento da Implantação":dataVariables.get("formaDePagamentoDaImplantacao"),
                            "Fee":dataVariables.get("fee"),
                            "Dia da Cobrança do Fee":dataVariables.get("diaDeCobrancaDoFee"),
                            "Observações":dataVariables.get("observacoes"),
                            "Cobrança pela Corretora":dataVariables.get("cobrancaPelaCorretora"),
                            "Patrimônio Financeiro Estimado":dataVariables.get("patrimonioFinanceiroEstimado"),
                            "Patrimônio Financeiro Estimado":dataVariables.get("patrimonioFinanceiroEstimado"),
                            "Vincular à contrato pai?":dataVariables.get("vincularAContratoPai"),
                            "Número do Contrato Pai":dataVariables.get("numeroDoContratoPai")
                            }
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
                        "data":{
                            "Nome da Empresa":dataVariables.get("nomeDaEmpresa"),
                            "Email de Contato":dataVariables.get("emailDeContato"),
                            "Telefone da Empresa":dataVariables.get("telefoneDaEmpresa"),
                            "CNPJ":dataVariables.get("cnpj"),
                            "Endereço":dataVariables.get("endereco"),
                            "Bairro":dataVariables.get("bairro"),
                            "Cidade":dataVariables.get("cidade"),
                            "UF":dataVariables.get("uf"),
                            "CEP":dataVariables.get("cep"),
                            "Nome Completo do Responsável":dataVariables.get("nomeCompletoDoResponsavel"),
                            "Email do Responsável":dataVariables.get("emailDoResponsavel"),
                            "Data de Nascimento do Responsável":dataVariables.get("dataDeNascimentoDoResponsavel"),
                            "Telefone do Responsável":dataVariables.get("telefoneDoResponsável"),
                            "Cargo do Responsável":dataVariables.get("cargoDoResponsável"),
                            "CPF do Responsável":dataVariables.get("cpfDoResponsável"),
                            "Prazo de Vigência":dataVariables.get("prazoDeVigencia"),
                            "Closer Responsável":dataVariables.get("closerResponsavel"),
                            "Origem Interna":dataVariables.get("origemInterna"),
                            "Origem Externa":dataVariables.get("origemExterna"),
                            "Valor da Implantação":dataVariables.get("valorDaImplantacao"),
                            "Data do Pagamento da Implantação":dataVariables.get("dataDoPagamentoDaImplantacao"),
                            "Forma de Pagamento da Implantação":dataVariables.get("formaDePagamentoDaImplantacao"),
                            "Fee":dataVariables.get("fee"),
                            "Dia da Cobrança do Fee":dataVariables.get("diaDeCobrancaDoFee"),
                            "Observações":dataVariables.get("observacoes")
                            }
                        }
                    }
                }
            }

            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
    def addSignerToEnvelope(self, envelopeId, dataVariables, cpf, birthdate, phoneNum, email):
            url = self.clickSignBaseUrl+ "/envelopes/" + envelopeId + "/signers"
            name = dataVariables.get("nomeCompletoDoTitular")
            data = {
                    "data":{
                    "type":"signers",
                    "attributes":{
                        "name":name,
                        "birthday":birthdate,
                        "email":email,
                        "phone_number":phoneNum,
                        "has_documentation":True,
                        "documentation":cpf,
                        "refusable":True,  
                        "communicate_events":{
                            "document_signed":"whatsapp",
                            "signature_request":"whatsapp",
                            "signature_reminder":"email"
                        }
                    }
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
                    "remind_interval": 7,
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
            
