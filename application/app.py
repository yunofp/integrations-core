from flask import Flask
from application.extensions import configuration

from application.blueprints import restapi

def create_app():
  app = Flask(__name__)
  configuration.init_app(app)
  restapi.init_app(app)
  return app
