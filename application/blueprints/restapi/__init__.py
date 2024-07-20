from flask import Blueprint
from flask_restful import Api

from .resources import RestApiResource, ContractsResource, ContractsResourceRetry, ContractsResourceInput
bp = restapi = Blueprint('restapi', __name__, url_prefix='/api/v1')
api = Api(bp)
api.add_resource(RestApiResource, '/check/')
api.add_resource(ContractsResource, '/contracts/process')
api.add_resource(ContractsResourceRetry, '/contracts/process/retry')
api.add_resource(ContractsResourceInput, '/contracts/input')


def init_app(app):
  app.register_blueprint(restapi)