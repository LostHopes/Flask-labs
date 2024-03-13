from flask import jsonify, json
import os

from . import swagger

@swagger.route("/docs")
def swagger():
    base = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(base, "swagger.json")
    
    with open(path, "r") as file:
        return jsonify(json.load(file))