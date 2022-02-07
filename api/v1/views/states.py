#!/usr/bin/python3
"""Module for states"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.engine.file_storage import FileStorage
from models.state import State


@app_views.route('/states', defaults={'id': None}, methods=['GET'],
                 strict_slashes=False)
@app_views.route('/states/<id>', strict_slashes=False)
def states(id):
    """ Show status of the code"""
    dic_states = storage.all(State)
    print(dic_states)
    if id:
        lst_states = [state.to_dict() for state in dic_states.values()
                      if state.id == id]
        if not lst_states:
            abort(404)
    else:
        lst_states = [state.to_dict() for state in dic_states.values()]
    return jsonify(lst_states)
