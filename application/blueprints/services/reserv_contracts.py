
import logging
import pandas as pd
from io import StringIO
import requests
from datetime import datetime, timezone, timedelta
from ..utils import formatting, dataProcessing
from flask import current_app as app
from flask import jsonify
import pytz 
from . import pandas_processement
import time

logger = logging.getLogger(__name__)
class ContractsService:
  def __init__(self, zeevClient, processedRequestRepository, clickSignClient, profileRepository, extractRepository, paymentRepository, contractRepository):
    self.zeevClient = zeevClient
    self.processedRequestRepository = processedRequestRepository
    self.clickSignClient = clickSignClient
    self.config = app.config
    self.profileRepository = profileRepository
    self.extractRepository = extractRepository
    self.paymentRepository = paymentRepository
    self.contractRepository = contractRepository

  def listManyRetries(self):
    try:
      result = self.processedRequestRepository.getManyRetries()
      return result
    except Exception as e:
      logger.error("listManyRetries | Error listing processed requests:" + str(e))

  def listManyRetriesContract(self):
    try:
      result = self.contractRepository.getManyRetries()
      return result
    except Exception as e:
      logger.error("listManyRetries | Error listing processed requests:" + str(e))
    
  def processContract(self, requestId, contractValues):
    envelope = self.clickSignClient.createEnvelope(requestId)
    envelopeId = envelope.get('data', {}).get('id')
    logger.info("processContract | envelopeId:" + str(envelopeId))
    workType = dataProcessing.findByName(contractValues, "qualSeraOContrato")

    if not workType or 'Não sei' in workType:
      raise Exception("processContract | Invalid work type:" + str(requestId))

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
      newEnvelope = self.clickSignClient.createEnvelope(str(requestId) + 'Wealth')
      newEnvelopeId = newEnvelope.get('data', {}).get('id')
      documentIdWealth = self._processContractSteps(contractVariablesWealth, newEnvelopeId, 'Wealth')
      
      documents.extend([{'type': 'Grow', 'id': documentIdGrow}, {'type': 'Wealth', 'id': documentIdWealth}])
      
    else:
        logger.error("processContract | Unknown service type:" + workTypeFormatted)
        return None
    logger.info("processContract | workType:" + workTypeFormatted)
    return workTypeFormatted, documents

  def _definePhoneNumber(self, contractVariables):
    if self.config.get('PHONE_NUMBER_DEBUG'):
      phoneNum = self.config.get('PHONE_NUMBER_DEBUG')
    else:
      phoneNum = formatting.clearPhoneNum(contractVariables.get("telefoneDoTitular"))
    return phoneNum
  def _processContractSteps(self, contractVariables, envelopeId, contractType):
    try:
      phoneNum = self._definePhoneNumber(contractVariables)
      logger.info("_processContractSteps | sending contract to phoneNum:" + phoneNum)
      filename = formatting.formatFileName(contractType, contractVariables)
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
        
    
      self._addSignersRequirements(envelopeId, contractVariables, phoneNum, documentId)
      self.clickSignClient.activateEnvelope(envelopeId)
      self.clickSignClient.notificateEnvelope(envelopeId)
      return documentId
    except Exception as e:
        logger.error(f"_processContractSteps | Error: {str(e)}")
        raise e
    
    
  def _addSignersRequirements(self, envelopeId, contractVariables, phoneNum, documentId):
      clientName = contractVariables.get("nomeCompletoDoTitular")
      clientCpf = formatting.formatCpf(contractVariables.get("cpfDoTitular") or contractVariables.get("cpfDoResponsavel"))
      clientEmail = contractVariables.get("email")
      clientBirthdate = formatting.formatBirthdate(contractVariables.get("dataDeNascimento"))
      
      
      clientSignerResponse =  self.clickSignClient.addSignerToEnvelope(envelopeId, clientName, clientCpf, clientBirthdate, phoneNum, clientEmail)

      signerId = clientSignerResponse.get('data', {}).get('id')
      
      if not signerId:
        raise Exception("processContract | Error while creating signer:" + str(clientSignerResponse))
     
      qualificationRequirementsResponse = self.clickSignClient.addQualificationRequirements(envelopeId, signerId, documentId)

      qualificationRequirementsId = qualificationRequirementsResponse.get('data', {}).get('id')
    
      if not qualificationRequirementsId:
        logger.error("processContract | data:", " envelopeId: ", envelopeId, " signerId: ", signerId," documentId: ", documentId )
        raise Exception("processContract | Error while creating qualification requirements:" + str(qualificationRequirementsResponse))  
      
      self.clickSignClient.addAuthRequirements(envelopeId, signerId, documentId)
      
      jgvName = self.config.get('JGV_NAME')
      jgvEmail = self.config.get('JGV_EMAIL')
      jgvPhone = self.config.get('JGV_PHONE')
      
      jgvSignerResponse =  self.clickSignClient.addSignerToEnvelope(envelopeId, jgvName, None, None, jgvPhone, jgvEmail,'email')
      
      jgvSignerId = jgvSignerResponse.get('data', {}).get('id')
      
      if not jgvSignerId:
        raise Exception("processContract | Error while creating jgv signer:" + str(jgvSignerResponse))
      
      jgvQualificationRequirementsResponse = self.clickSignClient.addQualificationRequirements(envelopeId, jgvSignerId, documentId)
      
      jgvQualificationRequirementsId = jgvQualificationRequirementsResponse.get('data', {}).get('id')
      
      if not jgvQualificationRequirementsId:
        raise Exception("processContract | Error while creating jgv qualification requirements:" + str(jgvQualificationRequirementsId))
      
      self.clickSignClient.addAuthRequirements(envelopeId, jgvSignerId, documentId)
          

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
      logger.error("_insertSuccessfullyProcessedRequest | Error inserting successfully processed request:" + str(requestId), exc_info=True)
  
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
              logger.info('runTryAgain | started to process contract: ' + str(processedRequest))
              requestId = processedRequest.get('requestId')
              contractRequest = self.zeevClient.getContractRequestById(token, requestId)
              
              if not contractRequest:
                  self._insertFailedProcessedRequest(requestId, True, 'Contract not found')
                  continue
              
              contractValues = contractRequest[0]['formFields']
              
              isContractCompletelyFilledToProcess = dataProcessing.findByName(contractValues, "valorDoFEE")
              
              if not isContractCompletelyFilledToProcess:
                  logger.info('runTryAgain | Contract not completely filled to process: ' + str(requestId))
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

  def _getIntervalsDate(self):
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    intervalDays = self.config.get('CONTRACTS_PROCESSING_DAYS_INTERVAL')
    
    if not intervalDays:
      raise Exception("CONTRACTS_PROCESSING_DAYS_INTERVAL not defined")
    
    end = now + timedelta(days=intervalDays)
    formattedStartDate = now.strftime("%Y-%m-%d")
    formattedEndDate = end.strftime("%Y-%m-%d")
    logger.info("getIntervalsDate | startDate: " + formattedStartDate + " | endDate: " + formattedEndDate)
    return formattedStartDate, formattedEndDate
  def processAllContracts(self): 
    logger.info("processAllContracts | starting to process all contracts")
    contractsRequests = []
    
    try: 
      zeevToken = self.zeevClient.generateZeevToken()
      formattedStartDate, formattedEndDate = self._getIntervalsDate()
  
      contractsRequests = self.zeevClient.getContractsRequestsByDate(zeevToken, formattedStartDate, formattedEndDate)
      
    except requests.exceptions.RequestException as e:
      logger.error("processAllContracts | Error during getting contracts:" + str(e), exc_info=True)
    print(contractsRequests)
    if not contractsRequests:
      logger.info("processAllContracts | No contracts found to process")
      return
    
    logger.info("processAllContracts | starting to process contracts founds in date: " + formattedStartDate)
    
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

  def validate_csv_file(self, response): #OK
    if 'file' not in response.files:
        raise ValueError("No file part in the request")
    
    file = response.files['file']
    
    if file.filename == '':
        raise ValueError("No selected file")
    
    if not file.filename.lower().endswith('.csv'):
        raise ValueError("The received file is not a CSV")

    try:
        content = file.read().decode('utf-8')
        
        df = pd.read_csv(StringIO(content))
        
        # print(df.iloc[3]['Nome do Cliente'])
        
        return content
    
    except Exception as e:
        raise ValueError(f"Error processing CSV file: {e}")

  def horizontal_iteration_new(self, df, index, profile_dict, contract_dict, cod):
    for columns in range(47, len(df.columns), 7):
        # MMAAAA e MRR
        print(df.iloc[index]['Nome do Cliente'], "  //  ", df.iloc[0, columns])

        month_year = formatting.get_mmaaaa(df.iloc[0, columns])
        payment_dict = pandas_processement.create_payment_dict(index, df, month_year, profile_dict, contract_dict, columns + 3)

        # INSERINDO O PAGAMENTO
        self.paymentRepository.insert_payment_document(payment_dict)

        payment_id = self.paymentRepository.get_last_id()
        contract_id = self.contractRepository.get_last_id()

        extract_dict = pandas_processement.create_extract_dict(
            index, df, cod, month_year, payment_id, contract_id, 
            columns + 1, 
            columns, 
            columns + 2, 
            columns + 3, 
            columns + 4, 
            columns + 5, 
            columns + 6
        )

        # INSERINDO O EXTRATO
        self.extractRepository.insert_extract_document(extract_dict)

  def insert_contracts(self, csv):
    content = self.validate_csv_file(csv)

    if not content:
        logger.info("Missing file or in a invalid form.")
        raise ValueError("Invalid CSV file")

    logger.info("File sent on request is valid.")
    df = pd.read_csv(StringIO(content))

    for index, row in df.iterrows():
        readyStart = index >= 2  # true or false
        if not readyStart:
            continue      

        is_code_null = pd.isnull(df.iloc[index]['COD'])
        is_name_null = pd.isnull(df.iloc[index]['Nome do Cliente'])

        if not is_code_null and not is_name_null:
            cod_exists = self.contractRepository.cod_already_exists(df.iloc[index]['COD'])
            if not cod_exists:
                profile_dict = pandas_processement.create_profile_dict(index, df, df.iloc[index]['COD'])
                profile_id = self.profileRepository.insert_profile_document(profile_dict)
                profile_id = profile_id.inserted_id
                print(profile_id)

                contract_dict = pandas_processement.create_contract_dict(index, df.iloc[index]['COD'], df, profile_id)
                self.contractRepository.insert_contract_document(contract_dict)
                
                self.horizontal_iteration_new(df, index, profile_dict, contract_dict, df.iloc[index]['COD'])
                
        if is_code_null and not is_name_null:
            new_cod = formatting.generate_cod(df, index)
            while self.contractRepository.cod_already_exists(new_cod):
                new_cod = formatting.get_next_sequence(new_cod)

            cod_exists = self.contractRepository.cod_already_exists(new_cod)
            if not cod_exists:
                profile_dict = pandas_processement.create_profile_dict(index, df, new_cod)
                self.profileRepository.insert_profile_document(profile_dict)
                profile_id = self.profileRepository.get_last_profile_document_id(new_cod)

                contract_dict = pandas_processement.create_contract_dict(index, new_cod, df, profile_id)
                self.contractRepository.insert_contract_document(contract_dict)

                self.horizontal_iteration_new(df, index, profile_dict, contract_dict, new_cod)