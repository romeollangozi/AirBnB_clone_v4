#!/usr/bin/python3
'''
Modul to create API endpoints
'''
from models import storage
from models.state import State
from flask import jsonify
from flask import request
from api.v1.views import app_views
from flask import abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'PUT'])
def return_states(state_id=None):
    '''
    Status endpoint
    '''
    if request.method == 'GET':
        if state_id is None:
            states = []
            for obj in storage.all(State).values():
                states.append(obj.to_dict())
            return jsonify(states)
        state = storage.get(State, state_id)
        print(state)
        if state is None:
            return abort(404)
        return jsonify(state.to_dict())
    if request.method == 'PUT':
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        data = request.get_json()
        if not data:
            return abort(400, "Not a JSON")
        for k, v in data.items():
            if k not in ['id', 'updated_at', 'created_at']:
                setattr(state, k, data[k])
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    '''
    Status endpoint
    '''
    if state_id is None:
        return abort(404)
    obj = storage.get(State, state_id)
    if obj is None:
        return abort(404)
    print(obj)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    '''
    Status endpoint
    '''
    data = request.get_json()
    if not data:
        return abort(400, "Not a JSON")
    state_name = data.get("name", None)
    if state_name is None:
        return abort(400, "Missing name")
    new_state = State(name=state_name)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201
