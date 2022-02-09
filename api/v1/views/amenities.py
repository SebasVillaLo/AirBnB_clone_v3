#!/usr/bin/python3
"""
new view for Amenity objects that handles all default RESTFul API
actions
"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def Lists_amenitys():
    return jsonify
