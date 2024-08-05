#!/usr/bin/python3
"""states route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get.yml', methods=['GET'])
def get_all():
    """ get all by id """
    all_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_state(state_id):
    """ get state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def delete_state(state_id):
    """ delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post.yml', methods=['POST'])
def create_state():
    """ create new state instance """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    response = request.get_json()
    state = State(**response)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/state/put.yml', methods=['PUT'])
def update_state(state_id):
    """ post state method """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
