#!/usr/bin/python3
""" A script return the status of the API """

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def teardown(exception):
    """
    calls storage.close()
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    handls for 404 errors, returns a JSON-formatted.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host, port, threaded=True)
