#!/usr/bin/python3
"""
flask RESTful API
    GET /api/v1/places/<place_id>/reviews
    GET /api/v1/reviews/<review_id>
    DELETE /api/v1/reviews/<review_id>
    POST /api/v1/places/<place_id>/reviews
    PUT /api/v1/reviews/<review_id>
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all review objects of a Place.
    If the place_id is not linked to any Place object,
        raise a 404 error
    """
    rv = []
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    for review in pl.reviews:
        rv.append(review.to_dict())
    return jsonify(rv)


@app_views.route("/reviews/<review_id>/",
                 methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a review object by id. If the review_id is not
    linked to any review object, raise a 404 error.
    """
    rv = storage.get("Review", review_id)
    if rv is None:
        abort(404)
    return jsonify(rv.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a review object. If the review_id is not
    linked to any review object, raise a 404 error.
    Returns an empty dictionary with the status code 200.
    """
    rv = storage.get("Review", review_id)
    if rv is None:
        abort(404)
    rv.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """
    Creates a review.
    f the place_id is not linked to any Place object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    If the dictionary doesn’t contain the key user_id,
        raise a 400 error with the message Missing user_id.
    If the dictionary doesn’t contain the key text,
        raise a 400 error with the message Missing text.
    Returns the new review with the status code 201.
    """
    data = request.get_json()
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    elif "user_id" not in data:
        abort(400, description="Missing user_id")
    elif "text" not in data:
        abort(400, description="Missing text")
    else:
        us = storage.get("User", data['user_id'])
        if us is None:
            abort(404)
        rv = Review(**data)
        rv.place_id = rv.id
        rv.save()
        return make_response(jsonify(rv.to_dict()), 201)


@app_views.route("/reviews/<reviews_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_review(reviews_id):
    """
    Updates a review object, with all key-value pairs
    of the dictionary.
    If the review_id is not linked to any review object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    Returns the review object with the status code 200.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    rv = storage.get("Review", reviews_id)
    if rv is None:
        abort(404)
    for k, v in data.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(rv, k, v)
    rv.save()
    return make_response(jsonify(rv.to_dict()), 200)
