#!/usr/bin/python3
'''
File containing the index view of the API.
'''
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def api_status():
    """
    Obtain the status of the API.
    """
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats')
def get_stats():
    '''
    Gets the number of objects for each type.
    '''
    objs = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }
    for key, val in objs.items():
        objs[key] = storage.count(val)
    return jsonify(objs)
