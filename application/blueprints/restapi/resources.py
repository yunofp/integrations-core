from flask import jsonify, abort, request
from flask_restful import Resource
import json
import threading
from ..services.reserv_contracts import ContractsService
from ..clients import clicksignClient, zeevClient
from ..repositories import processedRequestRepository, profile, extract, payment, contract
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
    self.extractRepository = extract.extractRepository()
    self.paymentRepository = payment.paymentRepository()
    self.profileRepository = profile.profileRepository()
    self.contractRepository = contract.contractRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.extractRepository, self.paymentRepository, self.contractRepository)

    thread = threading.Thread(target=self.service.processAllContracts)
    thread.start()

    return jsonify({'message': 'Process accepted'})
class ContractsResourceRetry(Resource):
  
  def get(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.extractRepository = extract.extractRepository()
    self.paymentRepository = payment.paymentRepository()
    self.profileRepository = profile.ProfileRepository()
    self.contractRepository = contract.contractRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.extractRepository, self.paymentRepository, self.contractRepository)
    result = self.service.listManyRetries()
    return json.dumps(result, default=str)

    
  def post(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.extractRepository = extract.extractRepository()
    self.paymentRepository = payment.paymentRepository()
    self.profileRepository = profile.ProfileRepository()
    self.contractRepository = contract.contractRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient, self.profileRepository, self.extractRepository, self.paymentRepository, self.contractRepository)
    
    thread = threading.Thread(target=self.service.runTryAgain)
    thread.start()

    return jsonify({'message': 'Request retry accepted'})

class ContractsResourceInput(Resource):
  def post(self):
    csv = request
    self.profileRepository = profile.profileRepository()
    self.extractRepository = extract.extractRepository()
    self.paymentRepository = payment.paymentRepository()
    self.contractRepository = contract.contractRepository()
    self.service = ContractsService(None, None, None, self.profileRepository, self.extractRepository, self.paymentRepository, self.contractRepository)

    response = self.service.insert_contracts(csv)

    return jsonify({'message': response})