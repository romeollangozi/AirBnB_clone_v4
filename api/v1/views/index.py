#!/usr/bin/python3
'''
Module to create the routes
for our api
'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    '''
    Status handler
    '''
    return jsonify({"status": "OK"})
