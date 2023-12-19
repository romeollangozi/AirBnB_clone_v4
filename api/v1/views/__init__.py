#!/usr/bin/python3
from flask import Blueprint
from api.v1.views.index import *
"""
Moudle to create Blueprint for our API
"""


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
