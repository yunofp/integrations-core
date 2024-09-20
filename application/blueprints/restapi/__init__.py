from flask import Blueprint
from flask_restful import Api

from .resources import (
    RestApiResource,
    ContractsResource,
    ContractsResourceRetry,
    ContractsResourceInput,
    NewBusinessResource,
    PerformanceResource,
)

bp = restapi = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(RestApiResource, "/check/")
api.add_resource(ContractsResource, "/contracts/process")
api.add_resource(ContractsResourceRetry, "/contracts/process/retry")
api.add_resource(ContractsResourceInput, "/contracts/input")
api.add_resource(NewBusinessResource, "/contracts/new-business-values")
api.add_resource(PerformanceResource, "/contracts/performance")


def init_app(app):
    app.register_blueprint(restapi)
