#!/usr/bin/python3
"""Module of the APP configuration"""
from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """
    Return sotrange close
    """
    storage.close()


@app.errorhandler(404)
def error(err):
    """Return error for this page"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')), threaded=True)
