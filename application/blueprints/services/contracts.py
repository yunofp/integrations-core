
import logging
import requests
from datetime import datetime, timezone
from ..utils import formatting, dataProcessing
from flask import current_app as app
logger = logging.getLogger(__name__)
class ContractsService:
  def __init__(self, zeevClient, processedRequestRepository, clickSignClient):
    self.zeevClient = zeevClient
    self.processedRequestRepository = processedRequestRepository
    self.clickSignClient = clickSignClient
    self.config = app.config
    
  
  def listManyRetries(self):
    try:
      result = self.processedRequestRepository.getManyRetries()
      return result
    except Exception as e:
      logger.error("listManyRetries | Error listing processed requests:" + str(e))
    
  def processContract(self, requestId):
    zeevToken = self.zeevClient.generateZeevToken()
    instanceProcess = self.zeevClient.getServiceType(requestId, zeevToken)
    envelopeId = self.clickSignClient.createEnvelope()
    instanceProcess = formatting.formatServiceType(instanceProcess)
    documentsId = []
    if instanceProcess == "Grow":
      documentsId.append(self._processGrowContract(requestId, zeevToken, envelopeId))
    elif instanceProcess == "Wealth":
      documentsId.append(self._processWealthContract(requestId, zeevToken, envelopeId))
    elif instanceProcess == "Work":
      documentsId.append(self._processWorkContract(requestId, zeevToken, envelopeId))
    elif instanceProcess == "Grow & Wealth":
        documentIdGrow = self._processGrowContract(requestId, zeevToken, envelopeId)
        documentIdWealth = self._processWealthContract(requestId, zeevToken, envelopeId)
        documentsId.extend([documentIdGrow, documentIdWealth])
    else:
        logger.error("processContract | Unknown service type:" + instanceProcess)
        return None

    return instanceProcess, documentsId

  def _processGrowContract(self, requestId, zeevToken, envelopeId):
      growResponse = self.zeevClient.firstStepContractPost(requestId, zeevToken)
      growResponse2 = self.zeevClient.secondStepContractPost(requestId, zeevToken)
      contractVariables = dataProcessing.defineVariablesGrow(growResponse, growResponse2)
      return self._processContractSteps(contractVariables, envelopeId)

  def _processWealthContract(self, requestId, zeevToken, envelopeId):
      wealthResponse = self.zeevClient.sendZeevPost(requestId, zeevToken)
      wealthResponse2 = self.zeevClient.sendZeevPost2(requestId, zeevToken)
      contractVariables = dataProcessing.defineVariablesWealth(wealthResponse, wealthResponse2)
      return self._processContractSteps(contractVariables, envelopeId)

  def _processWorkContract(self, requestId, zeevToken, envelopeId):
      workResponse = self.zeevClient.sendZeevPost(requestId, zeevToken)
      workResponse2 = self.zeevClient.sendZeevPost2(requestId, zeevToken)
      contractVariables = dataProcessing.defineVariablesWork(workResponse, workResponse2)
      return self._processContractSteps(contractVariables, envelopeId)

  def _definePhoneNumber(self, contractVariables):
    if self.config.get('PHONE_NUMBER_DEBUG'):
      phoneNum = self.config.get('PHONE_NUMBER_DEBUG')
      print('Pegando telefone do tarcisio')
    else:
      phoneNum = formatting.clearPhoneNum(contractVariables.get("telefoneDoTitular"))
    return phoneNum
  def _processContractSteps(self, contractVariables, envelopeId):
      phoneNum = self._definePhoneNumber(contractVariables)
      logger.info("_processContractSteps | sending contract to phoneNum:" + phoneNum)
      filename = formatting.formatFilename(contractVariables)
      documentId = self.clickSignClient.sendClickSignPost(contractVariables, envelopeId, filename)
      cpf = formatting.formatCpf(contractVariables.get("cpfDoTitular"))
      email = contractVariables.get("email")
      birthdate = formatting.formatBirthdate(contractVariables.get("dataDeNascimento"))
      signerId = formatting.addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
      self.clickSignClient.addQualificationRequirements(envelopeId, signerId, documentId)
      self.clickSignClient.addAuthRequirements(envelopeId, signerId, documentId)
      self.clickSignClient.activateEnvelope(envelopeId)
      self.clickSignClient.notificateEnvelope(envelopeId)
      return documentId

  def _isNewClientYuno(phrase):
    expectedPhrase = "new client yuno v. 1"
    phrase = phrase.lower()
    return phrase == expectedPhrase
  
  def _insertSuccessfullyProcessedRequest(self, requestId, serviceType, documentsId):
    try:
      status = {
        'name': 'send',
        'descritpion': 'delivered'
      }
      self.processedRequestRepository.insertOne({
          'tryAgain': False,
          'type': serviceType,
          'validNewClient': True,
          'requestId': requestId,
          'documentId': documentsId,
          'status': status,
          'createdAt': date.utcnow()
      })
    except Exception as e:
      logger.error("_insertSuccessfullyProcessedRequest | Error inserting successfully processed request:" + requestId, exc_info=True)
  
  def _updateSuccessfullyProcessedRequest(self, requestId, serviceType, documentsId):
    try:
      status = {
        'name': 'send',
        'descritpion': 'delivered'
      }
      self.processedRequestRepository.updateOne(requestId, {
          'tryAgain': False,
          'type': serviceType,
          'validNewClient': True,
          'requestId': requestId,
          'documentsId': documentsId,
          'status': status,
          'updatedAt': datetime.now(timezone.utc)
      })
    except Exception as e:
      logger.error("_updateSuccessfullyProcessedRequest | Error updating successfully processed request:" + requestId, exc_info=True)

  def _insertFailedProcessedRequest(self, requestId, tryAgain, errorMessage, statusName=None, validNewClient=False):
      try:
          document = {
              'tryAgain': tryAgain,
              'requestId': requestId,
              'createdAt': datetime.now(timezone.utc),
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
      logger.warn("run | lastProcessedRequest not found")
      return
    
    newRequestId = lastProcessedRequest['requestId'] + 1
    token = self.zeevClient.generateZeevToken()
    stopId = self.getStopInstanceId(newRequestId, token)

    if (newRequestId) == stopId:
        print('parouuu')
        return
    print('Continuou a execucao')
    data = self.zeevClient.secondStepContractPost(newRequestId, token)

    if data:
        requestName = data[0].get("requestName")
        if self._isNewClientYuno(requestName):
            readyToProcess = data[0].get("formFields")[0].get("value")
            if readyToProcess:
                  try:
                    serviceType, documentsId = self.processContract(newRequestId)
                    self._insertSuccessfullyProcessedRequest(newRequestId, serviceType, documentsId)
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


  def runTryAgain(self):
    processedRequestsRetries = self.processedRequestRepository.getManyRetries()
    token = self.zeevClient.generateZeevToken()

    for processedRequest in processedRequestsRetries:
        data = self.zeevClient.secondStepContractPost(processedRequest['requestId'], token)
        readyToProcess = data[0].get("formFields")[0].get("value")
        if readyToProcess:
            serviceType, documentsId = self.processContract(processedRequest['requestId'])
            self._updateSuccessfullyProcessedRequest(processedRequest['requestId'], serviceType, documentsId)
    
  def getStopInstanceId(self, id, zeevToken):
      stopId = id
      invalid_attempts = 0
      max_invalid_attempts = 5

      try:
          while invalid_attempts < max_invalid_attempts:
              response = self.zeevClient.instanceIdRequest(stopId, zeevToken)
              
              print('responseeeeee>>>>>>', response.status_code, 'stopID: ', stopId)
              
              if response.status_code == 200:
                  return stopId  # Retorna imediatamente o primeiro ID válido encontrado
              else:
                  invalid_attempts += 1
                  stopId += 1

          return stopId  # Retorna o ID onde parou após 5 tentativas inválidas

      except requests.exceptions.RequestException as e:
          logger.error("getStopInstanceId | Error during instance ID request:", exc_info=True)
          raise
      except Exception as e:
          logger.error("getStopInstanceId | An unexpected error occurred:", exc_info=True)
          raise

      
      