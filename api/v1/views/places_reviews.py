#!/usr/bin/python3
"""
RESTFUL API actions for reviews
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage, User, Place, Review
import requests
import json


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=["GET"])
def review_by_place(place_id):
    """
    Retrieves the list of all Review objects of a Place
    Args:
        place_id (str): place's id
    """
    tmp = []
    reviews = storage.all(Review)

    if storage.get(Place, place_id) is None:
        abort(404)
    for review in reviews.values():
        if place_id == review.place_id:
            tmp.append(review.to_dict())
    return jsonify(tmp)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def review_by_id(review_id):
    """
    Retrieves a Review object
    Args:
        review_id (str): id of the city to return_
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["DELETE"])
def get_rid_of_review(review_id):
    """
    Deletes a Review object
    Args:
        review_id (str): review id to delete
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=["POST"])
def update_review_by_id(place_id):
    """
    Creates a Review
    Args:
        review_id (str): review's id
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a json")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if "text" not in data.keys():
        abort(400, "Missing name")
    if "user_id" not in data.keys():
        abort(400, "Missing user_id")
    if storage.get(User, data["user_id"]) is None:
        abort(404)
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """
    Updates a Review object
    Args:
        review_id (str): review's id to update
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a json")
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
