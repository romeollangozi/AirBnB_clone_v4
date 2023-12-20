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
import json


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
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
        if state is None:
            return abort(404)
        return jsonify(state.to_dict())
    if request.method == 'PUT':
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        data = request.get_json(force=True)
        if not data:
            return abort(400, description="Not a JSON")
        for k, v in data.items():
            if k not in ['id', 'updated_at', 'created_at']:
                setattr(state, k, data[k])
        storage.save()
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        if state_id is None:
            return abort(404)
        obj = storage.get(State, state_id)
        if obj is None:
            return abort(404)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        if not data:
            return abort(400, description="Not a JSON")
        state_name = data.get("name", None)
        if state_name is None:
            return abort(400, description="Missing name")
        new_state = State(name=state_name)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
