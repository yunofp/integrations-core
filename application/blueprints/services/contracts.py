
import logging
import requests
from datetime import datetime
logger = logging.getLogger(__name__)
class ContractsService:
  def __init__(self, zeevClient, processedRequestRepository):
    self.zeevClient = zeevClient
    self.processedRequestRepository = processedRequestRepository
  
  def processContract(self,requestId):
    zeevToken = self.zeevClient.generateZeevToken()
    print(zeevToken)
    instanceProcess = self.zeevClient.getServiceType(requestId, zeevToken)
    envelopeId = createEnvelope()
    instanceProcess = formatServiceType(instanceProcess)

    if instanceProcess == "Grow":
    
        growResponse = sendZeevPost(requestId, zeevToken)
        growResponse2 = sendZeevPost2(requestId, zeevToken)
        contractVariables = defineVariablesGrow(growResponse, growResponse2)
        filename = formatFilename(contractVariables)
        documentId = sendClickSignPostGrow(contractVariables, envelopeId, filename)
        phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
        cpf = formatCpf(contractVariables.get("cpfDoTitular"))
        email = contractVariables.get("email")
        birthdate = formatBirthdate(contractVariables.get("dataDeNascimento"))
        signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
        addQualificationRequirements(envelopeId, signerId, documentId)
        addAuthRequirements(envelopeId, signerId, documentId)
        activateEnvelope(envelopeId)
        notificateEnvelope(envelopeId)

        filename =  datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " +  contractVariables.get("qualOTipoDeTrabalho") + " " + contractVariables.get("nomeCompletoDoTitular") + ".doc"
        downloadContract(clicksignContract, filename)
        signerName = contractVariables.get("nomeCompletoDoTitular")
        contractUrl = uploadContractToDrive(filename, contractVariables.get("email"))
        print(contractUrl)
        phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
        print(phoneNum + " " + signerName)
        signResponse = sendWhatsappSign(signerName, contractUrl, phoneNum)
        return sendZeevPost

    elif instanceProcess == "Wealth":

        wealthResponse = sendZeevPost(requestId, zeevToken)
        wealthResponse2 = sendZeevPost2(requestId, zeevToken)
        contractVariables = defineVariablesWealth(wealthResponse, wealthResponse2)
        filename = formatFilename(contractVariables)
        documentId = sendClickSignPostWealth(contractVariables, envelopeId, filename)
        phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
        cpf = formatCpf(contractVariables.get("cpfDoTitular"))
        email = contractVariables.get("email")
        birthdate = formatBirthdate(contractVariables.get("dataDeNascimento"))
        signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
        addQualificationRequirements(envelopeId, signerId, documentId)
        addAuthRequirements(envelopeId, signerId, documentId)
        activateEnvelope(envelopeId)
        notificateEnvelope(envelopeId)

        return sendZeevPost
    
    elif instanceProcess == "Work":

        workResponse = sendZeevPost(requestId, zeevToken)
        workResponse2 = sendZeevPost2(requestId, zeevToken)
        contractVariables = defineVariablesWork(workResponse, workResponse2)
        filename = formatFilename(contractVariables)
        documentId = sendClickSignPostWork(contractVariables, envelopeId, filename)
        phoneNum = clearPhoneNum(contractVariables.get("telefoneDaEmpresa"))
        cpf = formatCpf(contractVariables.get("cnpj"))
        email = contractVariables.get("emailDeContato")
        birthdate = formatBirthdate(contractVariables.get("dataDeNascimentoDoResponsavel"))
        signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
        addQualificationRequirements(envelopeId, signerId, documentId)
        addAuthRequirements(envelopeId, signerId, documentId)
        activateEnvelope(envelopeId)
        notificateEnvelope(envelopeId)

        return sendZeevPost

    elif instanceProcess == "Grow & Wealth":

        growResponse = sendZeevPost(requestId, zeevToken)
        growResponse2 = sendZeevPost2(requestId, zeevToken)
        contractVariables = defineVariablesGrow(growResponse, growResponse2)
        filename = formatFilename(contractVariables)
        documentId = sendClickSignPostGrow(contractVariables, envelopeId, filename)
        phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
        cpf = formatCpf(contractVariables.get("cpfDoTitular"))
        email = contractVariables.get("email")
        birthdate = formatBirthdate(contractVariables.get("dataDeNascimento"))
        signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
        addQualificationRequirements(envelopeId, signerId, documentId)
        addAuthRequirements(envelopeId, signerId, documentId)
        activateEnvelope(envelopeId)
        notificateEnvelope(envelopeId)

        wealthResponse = sendZeevPost(requestId, zeevToken)
        wealthResponse2 = sendZeevPost2(requestId, zeevToken)
        contractVariables = defineVariablesWealth(wealthResponse, wealthResponse2)
        filename = formatFilename(contractVariables)
        documentId = sendClickSignPostWealth(contractVariables, envelopeId, filename)
        phoneNum = clearPhoneNum(contractVariables.get("telefoneDoTitular"))
        cpf = formatCpf(contractVariables.get("cpfDoTitular"))
        email = contractVariables.get("email")
        birthdate = formatBirthdate(contractVariables.get("dataDeNascimento"))
        signerId = addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
        addQualificationRequirements(envelopeId, signerId, documentId)
        addAuthRequirements(envelopeId, signerId, documentId)
        activateEnvelope(envelopeId)
        notificateEnvelope(envelopeId)
    
        return sendZeevPost
    
    else:
        print("Não foi possível gerar o documento")
    return instanceProcess
  def _isNewClientYuno(phrase):
    expectedPhrase = "new client yuno v. 1"
    phrase = phrase.lower()
    return phrase == expectedPhrase
  
  def _insertSuccessfullyProcessedRequest(self, requestId, serviceType,documentId):
    try:
      self.processedRequestRepository.insertOne({
          'tryAgain': False,
          'type': serviceType,
          'validNewClient': True
          'requestId': requestId,
          'documentId': documentId,
          'status': {
            'name': 'send',
            'descritpion': 'delivered'
          }
          'createdAt': date.utcnow()
      })
    except Exception as e:
      logger.error("_insertSuccessfullyProcessedRequest | Error inserting successfully processed request:" + requestId, exc_info=True)
  


  def _insertFailedProcessedRequest(self, requestId, tryAgain, errorMessage, statusName=None, validNewClient=False):
      try:
          document = {
              'tryAgain': tryAgain,
              'requestId': requestId,
              'createdAt': datetime.now(datetime.UTC),
              'validNewClient': validNewClient
          }
          
          if statusName:
              document['status'] = {
                  'name': statusName,
                  'description': errorMessage
              }
          
          self.processedRequestRepository.insertOne(document)
      except Exception as e:
          logger.error("_insertFailedProcessedRequest | Error inserting failed processed request:" + requestId, exc_info=True)

  def run(self):
    
    lastProcessedRequest = self.processedRequestRepository.getLastProcessedRequest()
    if 'requestId' not in lastProcessedRequest:
      return
    
    newRequestId = lastProcessedRequest['requestId'] + 1
    token = self.zeevClient.generateZeevToken()
    stopId = self.getStopInstanceId(lastProcessedRequest.get('requestId'), token)

    if (lastProcessedRequest['requestId'] + 1) == stopId:
        return
  
    data = self.zeevClient.secondStepContractPost(newRequestId, token)

    if data:
        requestName = data[0].get("requestName")
        if self._isNewClientYuno(requestName):
            readyToProcess = data[0].get("formFields")[0].get("value")
            if readyToProcess:
                  try:
                    serviceType = self.processContract(newRequestId)
                    self._insertSuccessfullyProcessedRequest(newRequestId, serviceType)
                    self.run()
                  except Exception as e:
                    self._insertFailedProcessedRequest(newRequestId, True, e.__str__(), 'error', True)
                    logger.error("run | Error processing contract:" + newRequestId, exc_info=True)
                    self.run()
            else:
              self._insertFailedProcessedRequest(newRequestId, False, None, None, True) 
              self.run()
        else:
          self._insertFailedProcessedRequest(newRequestId, False) 
          self.run()
    else:
        self._insertFailedProcessedRequest(newRequestId, False, False) 
        self.run()

    
  def getStopInstanceId(self, id, zeevToken):
    
    stop = True
    stopId = id
    try:
        while stop:
            response = self.zeevClient.instanceIdRequest(stopId, zeevToken)
            if response.status_code == 200:
                stopId += 1
            else:
                stop = False
                return stopId
    except requests.exceptions.RequestException as e:
        logger.error("getStopInstanceId | Error during instance ID request:", exc_info=True)
        raise
    except Exception as e:
        logger.error("getStopInstanceId | An unexpected error occurred:", exc_info=True)
        raise

              
      