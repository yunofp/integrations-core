import requests
import json
from flask import current_app as app
import logging

logger = logging.getLogger(__name__)

class ZeevClient:
    def __init__(self):
        self.config = app.config
    def _getHeaders(self, token=None, contentType='application/json'):
        headers = {
            'Content-Type': contentType
        }
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return headers
    def generateZeevToken(self):
        try:
            zeev_base_url = self.config['ZEEV_BASE_URL']
            url = f"{zeev_base_url}/tokens"
            email = self.config['ZEEV_EMAIL_LOGIN']
            password = self.config['ZEEV_PASSWORD_LOGIN']
            
            data = {
                "email": email,
                "password": password
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                json_response = response.json()
                zeev_token = json_response.get("temporaryToken")
                return zeev_token
            else:
                response.raise_for_status()
                raise Exception(f"generateZeevToken | error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error("generateZeevToken | Error during request:", exc_info=True)
            raise
    def _getDefaultInstanceReportUrl(self):
        zeevBaseUrl = self.config['ZEEV_BASE_URL']
        url = f"{zeevBaseUrl}/instances/report"
        return url
    def getServiceType(self, instanceId, token):
        try:
            headers = self._getHeaders(token)
            url = self._getDefaultInstanceReportUrl()
            zeevNewClientFlowId = self.config['ZEEV_NEW_CLIENT_FLOW_ID']
            data = {
                "instanceId": instanceId,
                "flowId": zeevNewClientFlowId,
                "formFieldNames": [
                    "qualOTipoDeTrabalho",
                ]   
            }

            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                serviceType = response.json()
                return serviceType[0].get("formFields", [{}])[0].get("value", None)
            else:
                response.raise_for_status()
                raise Exception(f"getServiceType | error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error("getServiceType | Error during request:", exc_info=True)
            raise 
    def _firstStepContractDataRequest(self, instanceId):
        data = {
            "instanceId": instanceId,
            "flowId": self.config['ZEEV_NEW_CLIENT_FLOW_ID'],
            "formFieldNames": [
                "quemEVoce",
                "qualOTipoDeTrabalho",
                "nomeDoIndicado",
                "q01",
                "q02",
                "q03",
                "q04",
                "q05",
                "q06",
                "q07",
                "q08",
                "q09",
                "q10",
                "q11",
                "q12",
                "valorDaRendaFamiliar",
                "pont01",
                "pont02",
                "pont03",
                "pont04",
                "pont05",
                "pont06",
                "pont07",
                "pont08",
                "pont09",
                "pont10",
                "pont11",
                "pont12",
                "pont13",
                "calcularTotal",
                "total",
                "nomeDoCliente-Llaz",
                "contatoDoCliente",
                "emailDoCliente",
                "sugestaoDeImplantacao",
                "valorDeImplantacao",
                "sugestaoDeFEE",
                "valorDoFEE",
                "nomeDoCliente",
                "rendaMensalDoClientefamilia",
                "patrimonioFinanceiro",
                "patrimonioImobilizado",
                "perfilOrcamentario",
                "imovelQueMora",
                "estadoCivil",
                "profissaoDoTitular",
                "profissaoDoConjuge",
                "numeroDeFilhos",
                "ramoDeAtividade",
                "nomeDosSocios",
                "oClienteContratouAoMesmoTempoGrowWealth",
                "dataDoEnvioDoContrato",
                "dataEmQueOClienteAssinaraOContrato",
                "horaEmQueAssinaraOContrato",
                "qualOTipoDoContrato",
                "informeOCloser",
                "oClienteTambemFechouOContratoDeConsultoria",
                "codcloserResponsavel",
                "dataDeNascimentoDoTitular",
                "cPFCPNJ",
                "endereco",
                "bairro",
                "cidade",
                "uf",
                "cEP",
                "nomeDoConjugeResponsavelPelaEmpresa",
                "email",
                "dataDeNascimento",
                "prazoDeVigencia",
                "origemInterna",
                "origemExterna",
                "dataDoPagamentoDaImplantacao",
                "formaDePagamentoDaImplantacao",
                "diaDaCobrancaRecorrente",
                "obervacao",
                "autorizacaoDeCobrancaPelaCorretora",
                "haveraVinculacaoContratoPai",
                "numeroDoContratoPai",
                "cPF",
                "telefone"
            ]
        }
        return data
    def _secondStepContractDataRequest(self, instanceId):
        data = {
            "instanceId": instanceId,
            "flowId": 176,
            "formFieldNames": [
                "dataDeNascimentoDoTitular",
                "cPFCPNJ",
                "endereco",
                "bairro",
                "cidade",
                "uf",
                "cEP",
                "nomeDoConjugeResponsavelPelaEmpresa",
                "email",
                "dataDeNascimento",
                "prazoDeVigencia",
                "origemInterna",
                "origemExterna",
                "dataDoPagamentoDaImplantacao",
                "formaDePagamentoDaImplantacao",
                "diaDaCobrancaRecorrente",
                "obervacao",
                "autorizacaoDeCobrancaPelaCorretora",
                "haveraVinculacaoContratoPai",
                "numeroDoContratoPai",
                "cPF",
                "telefone"
            ]
        }
        return data
    def _contractDataRequest(self, instanceId, token, data):
        try:
            headers = self._getHeaders(token)
            url = self._getDefaultInstanceReportUrl(instanceId)
            data = self._firstStepContractDataRequest()
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                json_response = response.text.replace("'", '"')
                zeevResponse = json.loads(json_response)
                return zeevResponse[0].get("formFields")
            else:
                response.raise_for_status()
                raise Exception(f"fullContractData | error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error("fullContractData | Error during request:", exc_info=True)
            raise
    def firstStepContractPost(self, instanceId, token):
        data = self._firstStepContractDataRequest()
        return self._contractDataRequest(instanceId, token, data)
    def secondStepContractPost(self, instanceId, token):
        data = self._secondStepContractDataRequest(instanceId)
        return self._contractDataRequest(instanceId, token, data)
    def instanceIdRequest(self, instanceId, token):
        try:
            headers = self._getHeaders(token, 'application/vnd.api+json')
            url = self.config['ZEEV_BASE_URL'] + "/instances/" + str(instanceId) 
            response = requests.get(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            logger.error("instanceIdRequest | Error during request:", exc_info=True)
            raise