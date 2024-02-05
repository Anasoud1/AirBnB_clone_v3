#!/usr/bin/python3
"""
Flask App
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views, app_views_states, app_views_cities
from api.v1.views import app_views_amenities, app_views_users
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)
app.register_blueprint(app_views_states)
app.register_blueprint(app_views_cities)
app.register_blueprint(app_views_amenities)
app.register_blueprint(app_views_users)


@app.teardown_appcontext
def teardown_db(obj):
    """ teardown Method """
    storage.close()


@app.errorhandler(404)
def notfound(e):
    """ handler for 404 errors """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
