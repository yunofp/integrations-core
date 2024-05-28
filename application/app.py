from flask import Flask
from application.extensions import configuration, database, logger

from application.blueprints import restapi

def create_app():
  app = Flask(__name__)
  configuration.init_app(app)
  database.init_app(app)
  restapi.init_app(app)
  logger.configure_logging(app)
  return app
