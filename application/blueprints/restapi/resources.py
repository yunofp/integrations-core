from flask import jsonify, abort
from flask_restful import Resource

class RestApiResource(Resource):
  def get(self):
    return jsonify({'message': '> Api is alive! <'})

  def post(self):
    abort(400)