import requests
import json
from flask import current_app as app
import logging
import datetime

logger = logging.getLogger(__name__)

class ClicksignClient:
    def __init__(self):
        self.config = app.config
        self.token = self.config['ZEEV_BASE_URL']
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': self.token
        }
        self.clickSignBaseUrl= self.config['CLICKSIGN_BASE_URL']
    
    def createEnvelope(self):
        try:
            url = self.clickSignBaseUrl+"/envelopes/"

            data = {
                "data": {
                    "type": "envelopes",
                    "attributes": {
                            "name": "Envelope Integracao ZEEV-CLICKSIGN",
                            "locale": "pt-BR"
                    }
                }
            }

            response = requests.post(url, json=data, headers=self.headers)
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                envelopeResponse = json.loads(json_response)
                return envelopeResponse.get("data").get("id")
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("createEnvelope: Error while creating envelope: " + str(e))
            raise

    def sendClickSignPostGrow(self, dataVariables, envelopeId, filename):
        try:

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
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                csResponse = json.loads(json_response)
                return csResponse.get("data").get("id")
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("sendClickSignPostGrow: Error while sending document: " + str(e))
            raise

    def sendClickSignPostWealth(self, dataVariables, envelopeId, filename):
        try:
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
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                csResponse = json.loads(json_response)
                return csResponse.get("data").get("id")
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("sendClickSignPostWealth: Error while sending document: " + str(e))
            raise

    def sendClickSignPostWork(self, dataVariables, envelopeId, filename):
        try:

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
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                csResponse = json.loads(json_response)
                return csResponse.get("data").get("id")
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("sendClickSignPostWork: Error while sending document: " + str(e))
            raise


    def sendWhatsappSign(self,signerName, urlDrive, phoneNum):
        try:
            
            url = self.clickSignBaseUrl + "/acceptance_term/whatsapps?access_token=" + self.token

            data = {
                "acceptance_term": {
                    "name": "Assinatura do Contrato do seu Plano Yuno",
                    "sender_name": "Yuno FP",
                    "sender_phone": "62981331262",
                    "content": "Olá, este é o aceite via Whatsapp do seu novo plano de consultoria da Yuno, o acesso ao documento foi enviado para o email informado pelo contratante. Segue o link do documento do contrato no Google Drive: " + urlDrive,
                    "signer_phone": phoneNum,
                    "signer_name": signerName
                }
            }

            response = requests.post(url, json=data, headers=self.headers)
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                signResponse = json.loads(json_response)
                return signResponse
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("sendWhatsappSign: Error while sending whatsapp: " + str(e))
            raise

    def addSignerToEnvelope(self, envelopeId, dataVariables, cpf, birthdate, phoneNum, email):
        try:
        
            url = self.clickSignBaseUrl+ "/envelopes/" + envelopeId + "/signers"

            data = {
                    "data":{
                    "type":"signers",
                    "attributes":{
                        "name":dataVariables.get("nomeCompletoDoTitular"),
                        "birthday":birthdate,
                        "email":email,
                        "phone_number":"64993456689",
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
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                csResponse = json.loads(json_response)
                return csResponse.get("data").get("id")
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            json_response = response.text.replace("'", '"')
            csResponse = json.loads(json_response)
            logger.error("addSignerToEnvelope: Error while sending document: " + str(e))
            raise

    def addQualificationRequirements(self, envelopeId, signerId, documentId):
        try:
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
            
            if response.status_code == 201:
                json_response = response.text.replace("'", '"')
                csResponse = json.loads(json_response)
                return csResponse.get("data").get("id")
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            json_response = response.text.replace("'", '"')
            csResponse = json.loads(json_response)
            logger.error("addQualificationRequirements: Error while sending document: " + str(e))
            raise

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
            else:
                response.raise_for_status()
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
            else:
                response.raise_for_status()
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
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            json_response = response.text.replace("'", '"')
            csResponse = json.loads(json_response)
            logger.error("notificateEnvelope: Error while sending document: " + str(e) + " " + str(csResponse))
            raise
            
