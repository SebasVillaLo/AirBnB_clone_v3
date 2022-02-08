#!/usr/bin/python3
"""Module for states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.engine.file_storage import FileStorage
from models.state import State

dic_states = storage.all(State)


@app_views.route('/states', defaults={'id': None}, methods=['GET'],
                 strict_slashes=False)
@app_views.route('/states/<id>', strict_slashes=False)
def get_states(id):
    """ Show status of the code"""
    if id:
        state = storage.get(State, id)
        print(state)
        if not state:
            abort(404)
        return jsonify(state.to_dict())
    return jsonify([state.to_dict() for state in dic_states.values()])


@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def delete_states(id):
    """ Show status of the code"""
    state = storage.get(State, id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<id>', methods=['POST'], strict_slashes=False)
def put_states(id):
    state_jason = request.get_json(silent=True)
    if not state_jason:
        return(jsonify({'error': 'Not a JSON'})), 400
    if 'name' not in state_jason:
        return(jsonify({'error': 'Missing name'})), 400
    state = State(**state_jason)
    storage.save()
    return jsonify(state.to_dict()), 201
