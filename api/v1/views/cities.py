#!/usr/bin/python3
"""
Module for cities requests
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities_from_state(state_id):
    """returns a list of dictionary of the cities from a given state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City).values()
    cities_list = [city.to_dict()
                   for city in cities if city.state_id == state.id]
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """Get the city identified by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city_id(city_id=None):
    """Delete city identified by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """creates a city only using the name
    and returns it as a dictionary"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif not data.get('name'):
        abort(400, "Missing name")
    else:
        data['state_id'] = state_id
        NewCity = City(**data)
        storage.new(NewCity)
        NewCity.save()
        return jsonify(NewCity.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city_id(city_id):
    """updates instance but asking for its id and returns it as a dictionary"""
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        for key, value in request_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        result = city.to_dict()
        return jsonify(result), 200
