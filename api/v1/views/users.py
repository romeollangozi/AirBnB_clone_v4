#!/usr/bin/python3
'''
Modul to create API endpoints
'''
from models import storage
from models.user import User
from flask import jsonify
from flask import request
from api.v1.views import app_views
from flask import abort


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def return_users(user_id=None):
    '''
    Status endpoint
    '''

    if request.method == 'GET':
        if user_id is None:
            users = []
            for obj in storage.all(User).values():
                users.append(obj.to_dict())
            return jsonify(users)
        user = storage.get(User, user_id)
        if user is None:
            return abort(404)
        return jsonify(user.to_dict())
    if request.method == 'PUT':
        user = storage.get(User, user_id)
        if user is None:
            return abort(404)
        data = request.get_json(force=True)
        if not data:
            return abort(400, description="Not a JSON")
        for k, v in data.items():
            if k not in ['id', 'updated_at', 'created_at', 'email']:
                setattr(user, k, data[k])
        storage.save()
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        if user_id is None:
            return abort(404)
        obj = storage.get(User, user_id)
        if obj is None:
            return abort(404)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        if not data:
            return abort(400, description="Not a JSON")
        user_email = data.get("email", None)
        user_password = data.get("password", None)
        if user_email is None:
            return abort(400, description="Missing email")
        if user_password is None:
            return abort(400, description="Missing password")
        new_user = User(email=user_email, password=user_password)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
