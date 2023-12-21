#!/usr/bin/python3
'''
Modul to create API endpoints
'''
from models import storage
from models.amenity import Amenity
from flask import jsonify
from flask import request
from api.v1.views import app_views
from flask import abort


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def return_amenities(amenity_id=None):
    '''
    Status endpoint
    '''

    if request.method == 'GET':
        if amenity_id is None:
            amenities = []
            for obj in storage.all(Amenity).values():
                amenities.append(obj.to_dict())
            return jsonify(amenities)
        amenitiy = storage.get(Amenity, amenity_id)
        if amenitiy is None:
            return abort(404)
        return jsonify(amenitiy.to_dict())
    if request.method == 'PUT':
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return abort(404)
        data = request.get_json(force=True)
        if not data:
            return abort(400, description="Not a JSON")
        for k, v in data.items():
            if k not in ['id', 'updated_at', 'created_at']:
                setattr(amenity, k, data[k])
        storage.save()
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        if amenity_id is None:
            return abort(404)
        obj = storage.get(Amenity, amenity_id)
        if obj is None:
            return abort(404)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    if request.method == 'POST':
        data = request.get_json(silent=True, force=True)
        if not data:
            return abort(400, description="Not a JSON")
        amenity_name = data.get("name", None)
        if amenity_name is None:
            return abort(400, description="Missing name")
        new_amenity = Amenity(name=amenity_name)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
