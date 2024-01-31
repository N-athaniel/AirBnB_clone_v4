#!/usr/bin/python3
"""
flask RESTful API
    GET /api/v1/states/<state_id>/cities
    GET /api/v1/cities/<city_id>
    DELETE /api/v1/cities/<city_id>
    POST /api/v1/states/<state_id>/cities
    PUT /api/v1/cities/<city_id>
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State.
    If the state_id is not linked to any State object,
        raise a 404 error
    """
    ct = []
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    for city in st.cities:
        ct.append(city.to_dict())
    return jsonify(ct)


@app_views.route("/cities/<city_id>/",
                 methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by id. If the city_id is not
    linked to any City object, raise a 404 error.
    """
    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)
    return jsonify(ct.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object. If the city_id is not
    linked to any City object, raise a 404 error.
    Returns an empty dictionary with the status code 200.
    """
    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)
    ct.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """
    Creates a City.
    f the state_id is not linked to any State object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    If the dictionary doesn’t contain the key name,
        raise a 400 error with the message Missing name
    Returns the new City with the status code 201.
    """
    data = request.get_json()
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    elif "name" not in data:
        abort(400, description="Missing name")
    else:
        ct = City(**data)
        ct.state_id = ct.id
        ct.save()
        return make_response(jsonify(ct.to_dict()), 201)


@app_views.route("/cities/<cities_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_city(cities_id):
    """
    Updates a City object, with all key-value pairs
    of the dictionary.
    If the city_id is not linked to any City object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    Returns the City object with the status code 200.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ct = storage.get("City", cities_id)
    if ct is None:
        abort(404)
    for k, v in data.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(ct, k, v)
    ct.save()
    return make_response(jsonify(ct.to_dict()), 200)
