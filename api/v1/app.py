#!/usr/bin/python3
"""
Module to instatiate an flask app
to deploy our API
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """
    Function call to close db connection
    after each app teardwon
    """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", default=5000)),
            threaded=True)
