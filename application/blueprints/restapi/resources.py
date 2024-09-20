from flask import jsonify, abort, request, Response
from flask_restful import Resource
import json
import threading
from ..services.contracts import ContractsService
from application.blueprints.services.business_service import BusinessService
from application.blueprints.services.csv_service import CsvService
from ..clients import clicksignClient, zeevClient
from ..repositories import (
    contractsRepository,
    entriesRepository,
    processedRequestRepository,
    profileRepository,
    goal_repository,
    indications_repository,
)
from application.blueprints.services.performance_service import PerformanceService
import logging

logger = logging.getLogger(__name__)


class RestApiResource(Resource):
    def get(self):
        return jsonify({"message": "> Api is alive! <"})

    def post(self):
        abort(400)


class ContractsResource(Resource):
    def post(self):
        self.zeevClient = zeevClient.ZeevClient()
        self.clicksignClient = clicksignClient.ClicksignClient()
        self.processedRequestRepository = (
            processedRequestRepository.ProcessedRequestsRepository()
        )
        self.entriesRepository = entriesRepository.EntriesRepository()
        self.profileRepository = profileRepository.ProfileRepository()
        self.contractsRepository = contractsRepository.ContractsRepository()
        self.service = ContractsService(
            self.zeevClient,
            self.processedRequestRepository,
            self.clicksignClient,
            self.profileRepository,
            self.entriesRepository,
            self.contractsRepository,
        )

        thread = threading.Thread(target=self.service.processAllContracts)
        thread.start()

        return jsonify({"message": "Process accepted"})


class ContractsResourceRetry(Resource):

    def get(self):
        self.zeevClient = zeevClient.ZeevClient()
        self.clicksignClient = clicksignClient.ClicksignClient()
        self.processedRequestRepository = (
            processedRequestRepository.ProcessedRequestsRepository()
        )
        self.entriesRepository = entriesRepository.EntriesRepository()
        self.profileRepository = profileRepository.ProfileRepository()
        self.contractsRepository = contractsRepository.ContractsRepository()
        self.service = ContractsService(
            self.zeevClient,
            self.processedRequestRepository,
            self.clicksignClient,
            self.profileRepository,
            self.entriesRepository,
            self.contractsRepository,
        )
        result = self.service.listManyRetries()
        return json.dumps(result, default=str)

    def post(self):
        self.zeevClient = zeevClient.ZeevClient()
        self.clicksignClient = clicksignClient.ClicksignClient()
        self.processedRequestRepository = (
            processedRequestRepository.ProcessedRequestsRepository()
        )
        self.entriesRepository = entriesRepository.EntriesRepository()
        self.profileRepository = profileRepository.ProfileRepository()
        self.contractsRepository = contractsRepository.ContractsRepository()
        self.service = ContractsService(
            self.zeevClient,
            self.processedRequestRepository,
            self.clicksignClient,
            self.profileRepository,
            self.entriesRepository,
            self.contractsRepository,
        )

        thread = threading.Thread(target=self.service.runTryAgain)
        thread.start()

        return jsonify({"message": "Request retry accepted"})


class ContractsResourceInput(Resource):
    def post(self):
        csv = request
        self.profileRepository = profileRepository.ProfileRepository()
        self.entriesRepository = entriesRepository.EntriesRepository()
        self.contractsRepository = contractsRepository.ContractsRepository()
        self.service = ContractsService(
            None,
            None,
            None,
            self.profileRepository,
            self.entriesRepository,
            self.contractsRepository,
            None,
        )

        thread = threading.Thread(target=self.service.insert_contracts(csv))
        thread.start()

        return jsonify({"message": "Request input process started"})


class NewBusinessResource(Resource):
    def get(self):

        year = request.args.get("year", default=None, type=int)
        contract_type = request.args.get("contract_type", default=None, type=str)
        format = request.args.get("format", default=None, type=str)
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
        self.businessService = BusinessService(
            self.contractsRepository,
            self.entriesRepository,
            self.goal_repository,
            self.indications_repository,
        )
        self.csv_service = CsvService()
        new_business = self.businessService.get_new_business_values(year, contract_type)

        if format == "json":
            return jsonify(new_business)

        if format == "csv":
            csv_buffer = self.csv_service.save_new_business_to_csv(new_business)
            return Response(
                csv_buffer,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename=new_business.csv"},
            )


class PerformanceResource(Resource):
    def get(self):
        year = request.args.get("year", default=None, type=int)
        if not year:
            return jsonify({"error": "Year is required"}), 400
        self.indications_repository = indications_repository.IndicationsRepository()
        self.goals_repository = goal_repository.GoalRepository()
        self.performance_service = PerformanceService(
            self.indications_repository, self.goals_repository
        )
        return jsonify(self.performance_service.process_all_indications_by_year(year))
