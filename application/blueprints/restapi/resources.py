from flask import jsonify, abort
from flask_restful import Resource
from ..services.contracts import ContractsService
class RestApiResource(Resource):
  def get(self):
    return jsonify({'message': '> Api is alive! <'})

  def post(self):
    abort(400)
    
class ContractsResource(Resource):
  def post(self):
    self.service = ContractsService({})
    return self.service.process()