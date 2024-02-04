#!/usr/bin/python3
"""state api"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False,
                        methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    list_dict = []
    for obj in list(storage.all(State).values()):
        list_dict.append(obj.to_dict())
    return jsonify(list_dict)


@app_views.route('/states/<state_id>', strict_slashes=False,
                        methods=['GET'])
def get_state_id(state_id):
    """Retrieves a State object"""
    for obj in list(storage.all(State).values()):
        if state_id == obj.id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                        methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    for obj in list(storage.all(State).values()):
        if state_id == obj.id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state_id():
    """Creates a State"""
    if request.headers['Content-type'] != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(name=data['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                        methods=['PUT'])
def put_state_id(state_id):
    """Updates a State object"""
    obj = 0
    for o in list(storage.all(State).values()):
        if state_id == o.id:
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
