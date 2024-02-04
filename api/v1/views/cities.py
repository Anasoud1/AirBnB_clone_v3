#!/usr/bin/python3
"""cities api"""
from api.v1.views import app_views_cities
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views_cities.route('/states/<state_id>/cities', strict_slashes=False,
                        methods=['GET'])
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    list_cities = []
    for city in list(storage.all(City).values()):
        if state_id == city.state_id:
            list_cities.append(city.to_dict())
    if list_cities:
        return jsonify(list_cities)
    abort(404)


@app_views_cities.route('/cities/<city_id>', strict_slashes=False,
                        methods=['GET'])
def get_city_id(city_id):
    """Retrieves a City object."""
    for obj in list(storage.all(City).values()):
        if city_id == obj.id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views_cities.route('/cities/<city_id>', strict_slashes=False,
                        methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    for obj in list(storage.all(City).values()):
        if city_id == obj.id:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views_cities.route('/states/<state_id>/cities', strict_slashes=False,
                        methods=['POST'])
def post_city_id(state_id):
    """Creates a City"""
    if request.headers['Content-type'] != 'application/json':
        abort(400, 'Not a JSON')
    for state in list(storage.all(State).values()):
        if state_id == state.id:
            data = request.get_json()
            if 'name' not in data:
                abort(400, 'Missing name')
            new_city = City(state_id=state_id, name=data['name'])
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
    abort(404)


@app_views_cities.route('/cities/<city_id>', strict_slashes=False,
                        methods=['PUT'])
def put_city_id(city_id):
    """Updates a City object"""
    obj = 0
    for o in list(storage.all(City).values()):
        if city_id == o.id:
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
