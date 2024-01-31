#!/usr/bin/python3
"""
flask RESTful API
    GET /api/v1/users
    GET /api/v1/users/<user_id>
    DELETE /api/v1/users/<user_id>
    POST /api/v1/users
    PUT /api/v1/users/<user_id>
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users",
                 methods=["GET"],
                 strict_slashes=False)
def get_all_users():
    """
    Retrieves the list of all User objects.
    """
    l_users = []
    for u in storage.all(User).values():
        l_users.append(u.to_dict())
    return jsonify(l_users)


@app_views.route("/users/<user_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object by id. If the user_id is not
    linked to any User object, raise a 404 error.
    """
    u = storage.get("User", user_id)
    if u is None:
        abort(404)
    return jsonify(u.to_dict())


@app_views.route("/users/<user_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object. If the user_id is not
    linked to any User object, raise a 404 error.
    Returns an empty dictionary with the status code 200.
    """
    u = storage.get("User", user_id)
    if u is None:
        abort(404)
    u.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users",
                 methods=["POST"],
                 strict_slashes=False)
def post_user():
    """
    Creates a User.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    If the dictionary doesn’t contain the key email,
        raise a 400 error with the message Missing email.
    If the dictionary doesn’t contain the key password,
        raise a 400 error with the message Missing password
    Returns the new User with the status code 201.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    elif "email" not in data:
        abort(400, description="Missing email")
    elif "password" not in data:
        abort(400, description="Missing password")
    else:
        u = User(**data)
        u.save()
        return make_response(jsonify(u.to_dict()), 201)


@app_views.route("/users/<users_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_user(users_id):
    """
    Updates a User object, with all key-value pairs
    of the dictionary.
    If the user_id is not linked to any User object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    Returns the User object with the status code 200.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    u = storage.get("User", users_id)
    if u is None:
        abort(404)
    for k, v in data.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(u, k, v)
    u.save()
    return make_response(jsonify(u.to_dict()), 200)
