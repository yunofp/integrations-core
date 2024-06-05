
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
    
  def processContract(self, requestId, contractValues):
    envelopeId = self.clickSignClient.createEnvelope()
    workType = dataProcessing.findByName(contractValues, "qualOTipoDeTrabalho")
    
    if not workType:
      raise Exception("processContract | No work type found for request:" + requestId)

    workTypeFormatted = formatting.formatServiceType(workType)

    documents = []
    
    if workTypeFormatted == "Grow":
      
      contractVariables = dataProcessing.defineVariablesGrow(contractValues)
      documentId = self._processContractSteps(contractVariables, envelopeId, workTypeFormatted)
      documents.append({'type': 'Grow', 'id': documentId})
     
    elif workTypeFormatted == "Wealth":
      
      contractVariables = dataProcessing.defineVariablesWealth(contractValues)
      documentId = self._processContractSteps(contractVariables, envelopeId, workTypeFormatted)
      documents.append({'type': 'Wealth', 'id': documentId})
      
    elif workTypeFormatted == "Work":
      
      contractVariables = dataProcessing.defineVariablesWork(contractValues)
      documentId = self._processContractSteps(contractVariables, envelopeId, workTypeFormatted)
      documents.append({'type': 'Work', 'id': documentId})
      
    elif workTypeFormatted == "Grow & Wealth":
      
      contractVariablesGrow = dataProcessing.defineVariablesGrow(contractValues)
      contractVariablesWealth = dataProcessing.defineVariablesWealth(contractValues)
     
      documentIdGrow = self._processContractSteps(contractVariablesGrow, envelopeId, 'Grow')
      documentIdWealth = self._processContractSteps(contractVariablesWealth, envelopeId, 'Wealth')
      
      documents.extend([{'type': 'Grow', 'id': documentIdGrow}, {'type': 'Wealth', 'id': documentIdWealth}])
      
    else:
        logger.error("processContract | Unknown service type:" + workTypeFormatted)
        return None

    return workTypeFormatted, documents

  def _definePhoneNumber(self, contractVariables):
    if self.config.get('PHONE_NUMBER_DEBUG'):
      phoneNum = self.config.get('PHONE_NUMBER_DEBUG')
    else:
      phoneNum = formatting.clearPhoneNum(contractVariables.get("telefoneDoTitular"))
    return phoneNum
  def _processContractSteps(self, contractVariables, envelopeId, contractType):
      phoneNum = self._definePhoneNumber(contractVariables)
      logger.info("_processContractSteps | sending contract to phoneNum:" + phoneNum)
      filename = formatting.formatFilename(contractType, contractVariables)
      documentId = None
   
      if contractType == 'Grow':
        
        growResponse = self.clickSignClient.sendClickSignPostGrow(contractVariables, envelopeId, filename)
        documentId = growResponse.get('data', {}).get('id')
        if not documentId:
          raise Exception("processContract | Error while creating document:" + str(growResponse))
        
      elif contractType == 'Wealth':
        
        wealthResponse = self.clickSignClient.sendClickSignPostWealth(contractVariables, envelopeId, filename)
        documentId = wealthResponse.get('data', {}).get('id')
        
        if not documentId:
          raise Exception("processContract | Error while creating document:" + str(wealthResponse))
        
      elif contractType == 'Work':
        
        workResponse = self.clickSignClient.sendClickSignPostWork(contractVariables, envelopeId, filename)
        documentId = workResponse.get('data', {}).get('id')
        if not documentId:
          raise Exception("processContract | Error while creating document:" + str(workResponse))
        
   
      cpf = formatting.formatCpf(contractVariables.get("cpfDoTitular"))
      email = contractVariables.get("email")
      birthdate = formatting.formatBirthdate(contractVariables.get("dataDeNascimento"))
      
      response =  self.clickSignClient.addSignerToEnvelope(envelopeId, contractVariables, cpf, birthdate, phoneNum, email)
      
      signerId = response.get('data', {}).get('id')
      
      if not signerId:
        raise Exception("processContract | Error while creating signer:" + str(response))
     
      qualificationRequirementsResponse = self.clickSignClient.addQualificationRequirements(envelopeId, signerId, documentId)

      qualificationRequirementsId = qualificationRequirementsResponse.get('data', {}).get('id')
      
      if not qualificationRequirementsId:
        raise Exception("processContract | Error while creating qualification requirements:" + str(qualificationRequirementsResponse))  
    
      self.clickSignClient.addAuthRequirements(envelopeId, signerId, documentId)
      self.clickSignClient.activateEnvelope(envelopeId)
      self.clickSignClient.notificateEnvelope(envelopeId)
      return documentId

  def _isNewClientYuno(phrase):
    expectedPhrase = "new client yuno v. 1"
    phrase = phrase.lower()
    return phrase == expectedPhrase
  
  def _insertSuccessfullyProcessedRequest(self, requestId, serviceType, documents):
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
          'documents': documents,
          'status': status,
          'createdAt': datetime.now(timezone.utc)
      })
    except Exception as e:
      logger.error("_insertSuccessfullyProcessedRequest | Error inserting successfully processed request:" + requestId, exc_info=True)
  
  def _updateSuccessfullyProcessedRequest(self, requestId, serviceType, documentsData):
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
          'documents': documentsData,
          'status': status,
          'updatedAt': datetime.now(timezone.utc)
      })
    except Exception as e:
      logger.error("_updateSuccessfullyProcessedRequest | Error updating successfully processed request:" + requestId, exc_info=True)

  def _updateFailedProcessedRequest(self,requestId, statusName, statusDescription):
    try:
      status = {
        'name': statusName,
        'descritpion': statusDescription
      }
      self.processedRequestRepository.updateOne(requestId, {
          'status': status,
          'updatedAt': datetime.now(timezone.utc)
      })
    except Exception as e:
      logger.error("_updateFailedProcessedRequest | Error updating successfully processed request:" + requestId, exc_info=True)

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

  def runTryAgain(self):
      try:
          processedRequestsRetries = self.processedRequestRepository.getManyRetries()
          token = self.zeevClient.generateZeevToken()
          
          for processedRequest in processedRequestsRetries:
              requestId = processedRequest.get('requestId')
              
              contractRequest = self.zeevClient.getContractRequestById(token, requestId)
              contractValues = contractRequest['formFields']
              
              isContractCompletelyFilledToProcess = dataProcessing.findByName(contractValues, "valorDoFEE")
              
              if not isContractCompletelyFilledToProcess:
                  continue
              
              try:
                  serviceType, documents = self.processContract(requestId, contractValues)
                  self._updateSuccessfullyProcessedRequest(processedRequest['requestId'], serviceType, documents)
              except Exception as e:
                  self._updateFailedProcessedRequest(processedRequest['requestId'], 'Error', 'Retry Process error ' + str(e))
                  logger.error("runTryAgain | Error processing contract: " + str(e), exc_info=True)
                  continue
              
      except Exception as e:
          logger.error("runTryAgain | Error running try again: " + str(e), exc_info=True)

  
  def processAllContracts(self):
    logger.info("processAllContracts | starting to process all contracts")
    contractsRequests = []
    try: 
      zeevToken = self.zeevClient.generateZeevToken()
      now = datetime(2024, 5, 29)
      formattedDate = now.strftime("%Y-%m-%d")
      contractsRequests = self.zeevClient.getContractsRequestsByDate(zeevToken, formattedDate)
    except requests.exceptions.RequestException as e:
      logger.error("processAllContracts | Error during getting contracts:" + str(e), exc_info=True)
    
    if not contractsRequests:
      logger.info("processAllContracts | No contracts found to process")
      return
    
    logger.info("processAllContracts | starting to process contracts founds in date: " + formattedDate)
    
    for contractRequest in contractsRequests:

      requestId = contractRequest.get('id')

      alreadyExists = self.processedRequestRepository.findByRequestId(requestId)

      if alreadyExists:
        logger.info("processAllContracts | Contract request already exists:" + str(requestId))
        continue
      
      contractValues = contractRequest['formFields']

      isContractCompletelyFilledToProcess = dataProcessing.findByName(contractValues, "valorDoFEE")
      
      if not isContractCompletelyFilledToProcess:
        logger.info("processAllContracts | Contract not completely filled to process:" + str(requestId))
        self._insertFailedProcessedRequest(requestId, True, 'Contract not completely filled to process', 'waitingFill', True)
        continue
      
      try:

        serviceType, documents = self.processContract(requestId ,contractValues)
        self._insertSuccessfullyProcessedRequest(requestId, serviceType, documents)
      except Exception as e:
        
        self._insertFailedProcessedRequest(requestId, True, e.__str__(), 'error', True)
        logger.error("processAllContracts | Error processing contract:" + str(requestId), exc_info=True)