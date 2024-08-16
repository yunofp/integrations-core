from flask import jsonify, abort, request
from flask_restful import Resource
import json
import threading
from ..services.contracts import ContractsService
from ..clients import clicksignClient, zeevClient
from ..repositories import contractsRepository, entriesRepository, processedRequestRepository, profileRepository
import logging

logger = logging.getLogger(__name__)
class RestApiResource(Resource):
  def get(self):
    return jsonify({'message': '> Api is alive! <'})

  def post(self):
    abort(400)
    
class ContractsResource(Resource):
  def post(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.entriesRepository = entriesRepository.EntriesRepository()
    self.profileRepository = profileRepository.ProfileRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.entriesRepositor, self.contractsRepository)

    thread = threading.Thread(target=self.service.processAllContracts)
    thread.start()

    return jsonify({'message': 'Process accepted'})
class ContractsResourceRetry(Resource):
  
  def get(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.entriesRepository = entriesRepository.EntriesRepository()
    self.profileRepository = profileRepository.ProfileRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.entriesRepository, self.contractsRepository)
    result = self.service.listManyRetries()
    return json.dumps(result, default=str)

    
  def post(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.entriesRepository = entriesRepository.EntriesRepository()
    self.profileRepository = profileRepository.ProfileRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.entriesRepository, self.contractsRepository)
    
    thread = threading.Thread(target=self.service.runTryAgain)
    thread.start()

    return jsonify({'message': 'Request retry accepted'})

class ContractsResourceInput(Resource):
  def post(self):
    csv = request
    self.profileRepository = profileRepository.ProfileRepository()
    self.entriesRepository = entriesRepository.EntriesRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(None, None, None, self.profileRepository, self.entriesRepository, self.contractsRepository)

    response = self.service.insert_contracts(csv)

    return jsonify({'message': response})
  
class NewBusinessResource(Resource):
  def get(self):
    
    year = request.args.get('year', default=None, type=int)
    contract_type = request.args.get('contract_type', default=None, type=str)
    if not year:
      return jsonify({"error": "Year is required"}), 400
    if not contract_type:
      return jsonify({"error": "Contract type is required"}), 400
    
    self.entriesRepository = entriesRepository.EntriesRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(None,None,None,None,self.entriesRepository,self.contractsRepository)
    new_business = self.service.get_new_business_values(year, contract_type)
    
    return jsonify(new_business)