#!/usr/bin/python3
"""user api"""
from api.v1.views import app_views_users
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views_users.route('/users', strict_slashes=False,
                       methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    list_dict = []
    for obj in list(storage.all(User).values()):
        list_dict.append(obj.to_dict())
    return jsonify(list_dict)


@app_views_users.route('/users/<user_id>', strict_slashes=False,
                       methods=['GET'])
def get_user_id(user_id):
    """Retrieves a User object"""
    for obj in list(storage.all(User).values()):
        if user_id == obj.id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views_users.route('/users/<user_id>', strict_slashes=False,
                       methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    for obj in list(storage.all(User).values()):
        if user_id == obj.id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views_users.route('/users', strict_slashes=False, methods=['POST'])
def post_user_id():
    """Creates a User"""
    if request.headers['Content-type'] != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(email=data['email'], password=data['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views_users.route('/users/<user_id>', strict_slashes=False,
                       methods=['PUT'])
def put_user_id(user_id):
    """Updates a State object"""
    obj = 0
    for o in list(storage.all(User).values()):
        if user_id == o.id:
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
