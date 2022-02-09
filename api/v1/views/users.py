#!/usr/bin/python3
"""
Module for Users Requests
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def list_users():
    """returns a list with all the dictionary representation of a User"""
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def instance_users_id(user_id):
    """returns a list with all the instances of user"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)

    return jsonify(users.to_dict())


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_users():
    """creates instance requesting only the name
    and returns it as a dictionary"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif not data.get('email'):
        abort(400, "Missing email")
    elif not data.get('password'):
        abort(400, "Missing password")
    else:
        NewUser = User(**data)
        storage.new(NewUser)
        NewUser.save()
        return jsonify(NewUser.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_users_id(user_id):
    """ returns dictionary representation of of users"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    else:
        for key, value in request_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(users, key, value)
        storage.save()
        return jsonify(users.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_users_id(user_id=None):
    """remove instance by id and return an empty dictionary"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)

    storage.delete(users)
    storage.save()

    return jsonify({}), 200
