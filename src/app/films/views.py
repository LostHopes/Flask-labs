from flask import jsonify

from . import films


@films.route("/", methods=["GET"])
def show():
    return jsonify({})

