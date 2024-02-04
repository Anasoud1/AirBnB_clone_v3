#!/usr/bin/python3
"""amenities api"""
from api.v1.views import app_views_amenities
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views_amenities.route('/amenities', strict_slashes=False,
                           methods=['GET'])
def get_states():
    """Retrieves the list of all Amenity objects:"""
    list_dict = []
    for obj in list(storage.all(Amenity).values()):
        list_dict.append(obj.to_dict())
    return jsonify(list_dict)


@app_views_amenities.route('/amenities/<amenity_id>', strict_slashes=False,
                           methods=['GET'])
def get_amenity_id(amenity_id):
    """Retrieves a Amenity object:"""
    for obj in list(storage.all(Amenity).values()):
        if amenity_id == obj.id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views_amenities.route('/amenities/<amenity_id>', strict_slashes=False,
                           methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    for obj in list(storage.all(Amenity).values()):
        if amenity_id == obj.id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views_amenities.route('/amenities', strict_slashes=False,
                           methods=['POST'])
def post_amenity_id():
    """Creates a Amenity"""
    if request.headers['Content-type'] != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(name=data['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views_amenities.route('/amenities/<amenity_id>', strict_slashes=False,
                           methods=['PUT'])
def put_amenities_id(amenity_id):
    """Updates a Amenity object"""
    obj = 0
    for o in list(storage.all(Amenity).values()):
        if amenity_id == o.id:
            obj = o
    if obj == 0:
        abort(404)
    if request.headers['Content-type'] != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
