#!/usr/bin/python3
"""
flask RESTful API
    GET /api/v1/amenities
    GET /api/v1/amenities/<amenity_id>
    DELETE /api/v1/amenities/<amenity_id>
    POST /api/v1/amenities
    PUT /api/v1/amenities/<amenity_id>
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def get_all_amenities():
    """
    Retrieves the list of all Amenity objects.
    """
    l_amenities = []
    for a in storage.all(Amenity).values():
        l_amenities.append(a.to_dict())
    return jsonify(l_amenities)


@app_views.route("/amenities/<amenity_id>/",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a Amenity objectby id. If the amenity_id is not
    linked to any Amenity object, raise a 404 error.
    """
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    return jsonify(a.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object. If the amenity_id is not
    linked to any Amenity object, raise a 404 error.
    Returns an empty dictionary with the status code 200.
    """
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    a.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities",
                 methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """
    Creates a Amenity.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    If the dictionary doesn’t contain the key name,
        raise a 400 error with the message Missing name
    Returns the new Amenity with the status code 201.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    elif "name" not in data:
        abort(400, description="Missing name")
    else:
        a = Amenity(**data)
        a.save()
        return make_response(jsonify(a.to_dict()), 201)


@app_views.route("/amenities/<amenities_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenities_id):
    """
    Updates a Amenity object, with all key-value pairs
    of the dictionary.
    If the amenity_id is not linked to any Amenity object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    Returns the Amenity object with the status code 200.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    a = storage.get("Amenity", amenities_id)
    if a is None:
        abort(404)
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(a, k, v)
    a.save()
    return make_response(jsonify(a.to_dict()), 200)
