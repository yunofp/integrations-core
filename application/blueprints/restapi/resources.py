from flask import jsonify, abort, request
from flask_restful import Resource
import json
import threading
from ..services.contracts import ContractsService
from ..clients import clicksignClient, zeevClient
from ..repositories import contractsRepository, entries_Repository, payments_Repository, profile_Repository, processedRequestRepository
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
    self.entriesRepository = entries_Repository.EntriesRepository()
    self.paymentsRepository = payments_Repository.PaymentsRepository()
    self.profileRepository = profile_Repository.ProfileRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.entriesRepository, self.paymentsRepository, self.contractsRepository)

    thread = threading.Thread(target=self.service.processAllContracts)
    thread.start()

    return jsonify({'message': 'Process accepted'})
class ContractsResourceRetry(Resource):
  
  def get(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.entriesRepository = entries_Repository.EntriesRepository()
    self.paymentsRepository = payments_Repository.PaymentsRepository()
    self.profileRepository = profile_Repository.ProfileRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.entriesRepository, self.paymentsRepository, self.contractsRepository)
    result = self.service.listManyRetries()
    return json.dumps(result, default=str)

    
  def post(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.entriesRepository = entries_Repository.EntriesRepository()
    self.paymentsRepository = payments_Repository.PaymentsRepository()
    self.profileRepository = profile_Repository.ProfileRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.entriesRepository, self.paymentsRepository, self.contractsRepository)
    
    thread = threading.Thread(target=self.service.runTryAgain)
    thread.start()

    return jsonify({'message': 'Request retry accepted'})

class ContractsResourceInput(Resource):
  def post(self):
    csv = request
    self.profileRepository = profile_Repository.ProfileRepository()
    self.entriesRepository = entries_Repository.EntriesRepository()
    self.paymentsRepository = payments_Repository.PaymentsRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.service = ContractsService(None, None, None, self.profileRepository, self.entriesRepository, self.paymentsRepository, self.contractsRepository)

    response = self.service.insert_contracts(csv)

    return jsonify({'message': response})