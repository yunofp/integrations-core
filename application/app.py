from flask import Flask
from application.extensions import configuration, database, logger

from application.blueprints import restapi

def create_app():
  app = Flask(__name__)
  logger.configure_logging(app)
  configuration.init_app(app)
  database.init_app(app)
  restapi.init_app(app)

  return app

app = create_app()