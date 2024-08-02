from flask import jsonify, abort, request
from flask_restful import Resource
import json
import threading
from ..services.contracts import ContractsService
from ..clients import clicksignClient, zeevClient
from ..repositories import ContractsRepository, EntriesRepository, PaymentsRepository, ProfileRepository, processedRequestRepository
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
    self.EntriesRepository = EntriesRepository.EntriesRepository()
    self.PaymentsRepository = PaymentsRepository.PaymentsRepository()
    self.ProfileRepository = ProfileRepository.ProfileRepository()
    self.ContractRepository = ContractsRepository.ContractRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.ProfileRepository, self.EntriesRepository, self.PaymentsRepository, self.ContractRepository)

    thread = threading.Thread(target=self.service.processAllContracts)
    thread.start()

    return jsonify({'message': 'Process accepted'})
class ContractsResourceRetry(Resource):
  
  def get(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.EntriesRepository = EntriesRepository.EntriesRepository()
    self.PaymentsRepository = PaymentsRepository.PaymentsRepository()
    self.ProfileRepository = ProfileRepository.ProfileRepository()
    self.ContractRepository = ContractsRepository.ContractRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.ProfileRepository, self.EntriesRepository, self.PaymentsRepository, self.ContractRepository)
    result = self.service.listManyRetries()
    return json.dumps(result, default=str)

    
  def post(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.EntriesRepository = EntriesRepository.EntriesRepository()
    self.PaymentsRepository = PaymentsRepository.PaymentsRepository()
    self.ProfileRepository = ProfileRepository.ProfileRepository()
    self.ContractRepository = ContractsRepository.ContractRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.ProfileRepository, self.EntriesRepository, self.PaymentsRepository, self.ContractRepository)
    
    thread = threading.Thread(target=self.service.runTryAgain)
    thread.start()

    return jsonify({'message': 'Request retry accepted'})

class ContractsResourceInput(Resource):
  def post(self):
    csv = request
    self.ProfileRepository = ProfileRepository.ProfileRepository()
    self.EntriesRepository = EntriesRepository.EntriesRepository()
    self.PaymentsRepository = PaymentsRepository.PaymentsRepository()
    self.ContractRepository = ContractsRepository.ContractsRepository()
    self.service = ContractsService(None, None, None, self.ProfileRepository, self.EntriesRepository, self.PaymentsRepository, self.ContractRepository)

    response = self.service.insert_contracts(csv)

    return jsonify({'message': response})