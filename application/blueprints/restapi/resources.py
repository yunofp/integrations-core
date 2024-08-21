from flask import jsonify, abort, request, Response
from flask_restful import Resource
import json
import threading
from ..services.contracts import ContractsService
from ..services import indications_service
from ..clients import clicksignClient, zeevClient
from ..repositories import contractsRepository, entriesRepository, processedRequestRepository, profileRepository, goal_repository, indications_repository
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
    
    thread = threading.Thread(target=self.service.insert_contracts(csv))
    thread.start()

    return jsonify({'message': 'Request input process started'})
  
class NewBusinessResource(Resource):
  def get(self):
    
    year = request.args.get('year', default=None, type=int)
    contract_type = request.args.get('contract_type', default=None, type=str)
    format = request.args.get('format', default=None, type=str)
    if not year:
      return jsonify({"error": "Year is required"}), 400
    if not contract_type:
      return jsonify({"error": "Contract type is required"}), 400
    if not format:
      return jsonify({"error": "Format is required"}), 400
    
    self.entriesRepository = entriesRepository.EntriesRepository()
    self.contractsRepository = contractsRepository.ContractsRepository()
    self.goal_repository = goal_repository.GoalRepository()
    self.indications_repository = indications_repository.IndicationsRepository()
    self.indications_service = indications_service.IndicationsService(self.indications_repository)
    self.service = ContractsService(None,None,None,None,self.entriesRepository,self.contractsRepository, self.goal_repository)
    
    if format == 'json':
      # new_business = self.service.get_new_business_values(year, contract_type)
      indications = self.indications_service.get_indications_count_by_month()
      #TODO: pensar em transferir os dados de novos negocios para um outro serviço
      #TODO: corrigir retorno dos dados
      print(indications)
      return jsonify(indications)
    
    csv_buffer = self.service.save_new_business_to_csv(year, contract_type)
    return Response(
        csv_buffer,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=new_business.csv"}
    )