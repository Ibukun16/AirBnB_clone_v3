#!/usr/bin/python3
"""
Creating Flask web application API for AirBnB.
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__)
"""The Flask web application instance."""
HOST = getenv('HBNB_API_HOST', '0.0.0.0')
PORT = int(getenv('HBNB_API_PORT', '5000'))
cors = CORS(app, resources={r"/api/*": {"origins": '0.0.0.0'}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_flask(exception):
    """The Flask app/request context end event listener."""
    # print(exception)
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Handles the 404 HTTP error code."""
    response = {"error": "Not found"}
    return jsonify(response), 404


@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code to return custom 404 error.'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


app.config['SWAGGER'] = {"title": 'AirBnB clone - RESTful API',
           "description": 'This api was created for the hbnb restful api project,\
           all the documentation will be shown below',
           "uiversion": 3}

Swagger(app)


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=HOST, port=PORT, threaded=True)
