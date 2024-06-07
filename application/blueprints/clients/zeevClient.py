import requests
import json
from flask import current_app as app
import logging
from datetime import datetime

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
            zeevBaseUrl = self.config['ZEEV_BASE_URL']
            url = f"{zeevBaseUrl}/tokens"
            email = self.config['ZEEV_EMAIL_LOGIN']
            password = self.config['ZEEV_PASSWORD_LOGIN']
            
            data = {
                "login": email,
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
        
    def _FormFieldNames(self):
        return [
            "quemEVoce", "qualOTipoDeTrabalho", "nomeDoIndicado", "q01", "q02", "q03",
            "q04", "q05", "q06", "q07", "q08", "q09", "q10", "q11", "q12",
            "valorDaRendaFamiliar", "pont01", "pont02", "pont03", "pont04",
            "pont05", "pont06", "pont07", "pont08", "pont09", "pont10",
            "pont11", "pont12", "pont13", "calcularTotal", "total",
            "nomeDoCliente-Llaz", "contatoDoCliente", "responsavelPelaContratacao", "emailDoCliente",
            "sugestaoDeImplantacao", "valorDeImplantacao", "sugestaoDeFEE",
            "valorDoFEE", "nomeDoCliente", "rendaMensalDoClientefamilia",
            "patrimonioFinanceiro", "patrimonioImobilizado", "perfilOrcamentario",
            "imovelQueMora", "estadoCivil", "profissaoDoTitular", "profissaoDoConjuge",
            "numeroDeFilhos", "ramoDeAtividade", "nomeDosSocios",
            "oClienteContratouAoMesmoTempoGrowWealth", "dataDoEnvioDoContrato",
            "dataEmQueOClienteAssinaraOContrato", "horaEmQueAssinaraOContrato",
            "qualOTipoDoContrato", "informeOCloser", "oClienteTambemFechouOContratoDeConsultoria",
            "codcloserResponsavel", "dataDeNascimentoDoTitular", "cPFCPNJ",
            "endereco", "bairro", "cidade", "uF", "cEP",
            "nomeDoConjugeResponsavelPelaEmpresa", "email", "dataDeNascimento",
            "prazoDeVigencia", "origemInterna", "origemExterna", "dataDoPagamentoDaImplantacao",
            "formaDePagamentoDaImplantacao", "diaDaCobrancaRecorrente", "obervacao",
            "autorizacaoDeCobrancaPelaCorretora", "haveraVinculacaoContratoPai",
            "numeroDoContratoPai", "cPF", "telefone", "observacao", "qualSeraOContrato"
        ]
      
    def getContractsRequestsByDate(self, token, formattedDate):
            headers = self._getHeaders(token)
            zeevNewClientFlowId = self.config['ZEEV_NEW_CLIENT_FLOW_ID']
    
            data = {
                "flowId": zeevNewClientFlowId,
                "StartDateIntervalBegin": formattedDate,
                "StartDateIntervalEnd": formattedDate,
                "recordsPerPage": 100,
                "formFieldNames": self._FormFieldNames()
            }
            url = self._getDefaultInstanceReportUrl()
            response = requests.post(url, json=data, headers=headers)
            return response.json()
    
    def getContractRequestById(self, token, instanceId):
            headers = self._getHeaders(token)
            zeevNewClientFlowId = self.config['ZEEV_NEW_CLIENT_FLOW_ID']
            
            data = {
                "instanceId": instanceId,
                "flowId": zeevNewClientFlowId,
                "recordsPerPage": 100,
                "formFieldNames": self._FormFieldNames()
            }
            url = self._getDefaultInstanceReportUrl()
            response = requests.post(url, json=data, headers=headers)
            return response.json()
        
    def instanceIdRequest(self, instanceId, token):
        try:
            headers = self._getHeaders(token, 'application/vnd.api+json')
            url = self.config['ZEEV_BASE_URL'] + "/instances/" + str(instanceId) 
            response = requests.get(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            logger.error("instanceIdRequest | Error during request:", exc_info=True)
            raise