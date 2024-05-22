from flask import Blueprint
from flask_restful import Api

from .resources import RestApiResource, ContractsResource
bp = restapi = Blueprint('restapi', __name__, url_prefix='/api/v1')
api = Api(bp)
api.add_resource(RestApiResource, '/check/')
api.add_resource(ContractsResource, '/contracts/process')

def init_app(app):
  app.register_blueprint(restapi)