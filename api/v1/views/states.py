#!/usr/bin/python3
"""Module for states"""
import re
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.engine.file_storage import FileStorage
from models.state import State

dic_states = storage.all(State)


@app_views.route('/states', defaults={'state_id': None}, methods=['GET'],
                 strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states(state_id):
    """ Show status of the code"""
    if state_id:
        state = storage.get(State, state_id)
        print(state)
        if not state:
            abort(404)
        return jsonify(state.to_dict())
    return jsonify([state.to_dict() for state in dic_states.values()])


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id):
    """ Show status of the code"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_states():
    state_jason = request.get_json(silent=True)
    if not state_jason:
        return(jsonify({'error': 'Not a JSON'})), 400
    if 'name' not in state_jason:
        return(jsonify({'error': 'Missing name'})), 400
    state = State(**state_jason)
    storage.new(state)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    state_json = request.get_json(silent=True)
    if not state_id:
        abort(404)
    if not state_json:
        return(jsonify({'error': 'Not a JSON'})), 400
    state = storage.get(State, state_id)
    for key, value in state_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.new(state)
    state.save()

    return jsonify(state.to_dict()), 200
