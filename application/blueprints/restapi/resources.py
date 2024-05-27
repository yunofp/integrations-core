from flask import jsonify, abort
from flask_restful import Resource
from ..services.contracts import ContractsService
from ..clients import clicksignClient, zeevClient
from ..repositories import processedRequestRepository
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
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.zeevClicksign)
    self.service.run()
    
class ContractsResourceRetry(Resource):
  def post(self):
    self.zeevClient = zeevClient.ZeevClient()
    self.clicksignClient = clicksignClient.ClicksignClient()
    self.processedRequestRepository = processedRequestRepository.ProcessedRequestsRepository()
    self.service = ContractsService(self.zeevClient, self.processedRequestRepository, self.clicksignClient)
    self.service.runTryAgain()