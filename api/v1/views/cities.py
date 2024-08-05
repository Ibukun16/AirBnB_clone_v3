#!/usr/bin/python3
"""citiesi route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from flasgger.utils import swag_from


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/get.yml', methods=['GET'])
def get_cities_by_states(state_id):
    """ get list of cities for all states by the states' id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = [city.to_dict() for city in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/get_id.yml', methods=['GET'])
def get_city(city_id):
    """ get list of cities of a state by the city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/city/delete.yml', methods=['DELETE'])
def delete_city(city_id):
    """ delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post.yml', methods=['POST'])
def create_city(state_id):
    """ create new city instance """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    response = request.get_json()
    city = City(**response)
    city.state_id = state.id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/city/put.yml', methods=['PUT'])
def update_city(city_id):
    """ update city method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated']:
            setattr(city, key, value)
    storage.save()
    return jsonify(cty.to_dict()), 200
