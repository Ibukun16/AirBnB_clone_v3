#!/usr/bin/python3
"""states route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


def check(id):
    """
        checking if state is valid in storage
    """
    try:
        checker = storage.get(State, id)
        checker.to_dict()
    except Exception:
        abort(404)
    return checker


def get_all(id_state):
    """
        getting all states from storage
    """
    if id_state is not None:
        state = check(id_state)
        state_list = state.to_dict()
        return jsonify(state_list)
    all_states = []
    for s in storage.all(State).values():
        all_states.append(s.to_dict())
    return jsonify(all_states)


def delete_state(id_state):
    """
        deleting a state request
    """
    state = check(id_state)
    storage.delete(state)
    storage.save()
    response = {}
    return jsonify(response), 200


def create_state(request):
    """
        Create new state request
    """
    request_content = request.get_json()
    if request_content is None:
        abort(400, 'Not a JSON')
    try:
        state_name = request_content['name']
    except Exception:
        abort(400, "Missing name")
    state = State(name=state_name)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 200


def update_state(state_id, request):
    """
        Update state if found
    """
    state = check(state_id)
    request_content = request.get_json()
    if request_content is None:
        abort(400, 'Not a JSON')
    for key, val in request_json.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(state, key, val)
        storage.save()
        return jsonify(state.to_dict()), 200


@app_views.route('/states/', methods=['GET', 'POST'],
                 defaults={'state_id': None}, strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'])
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def states(state_id):
    """
    Global Method to handle request
    """
    if (request.method == "GET"):
        return get_all(state_id)
    elif request.method == "DELETE":
        return delete_state(state_id)
    elif request.method == "POST":
        return create_state(request), 201
    elif request.method == 'PUT':
        return update_state(state_id, request), 200
