from api.v1.views import app_views
from flask import jsonify
"""
Module to create the routes
"""


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})
