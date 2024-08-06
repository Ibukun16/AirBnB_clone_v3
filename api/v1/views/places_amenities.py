#!/usr/bin/python3
""" Places amenities routes handler for Flask API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import place
from models import amenity


def check_id(cls, amenity_id):
    """
    If the class is not linked to any classs object, raise a 404 error
    """
    try:
        get_amenity = storage.get(cls, amenity_id)
        get_amenity.to_dict()
    except Exception:
        abort(404)
    return get_amenity


def get_amenities(place_id):
    """
       Retrieves the list of all Amenity objects
       if amenity_id is not none get a Amenity object
    """
    check_id(place.Place, place_id)
    newplace = storage.get(place.Place, place_id)
    try:
        all_amenities = newplace.amenities
    except Exception:
        abort(404)
    amenities = []
    for obj in all_amenities:
        amenities.append(obj.to_dict())
    return jsonify(amenities)


def delete_amenities(place_id, amenity_id):
    """
        Deletes the link between Amenity object and a Place
        Return: an empty dictionary with the status code 200
    """
    newplace = check_id(place.Place, place_id)
    check_id(amenity.Amenity, amenity_id)
    for item in range(len(newplace.amenities)):
        if (newplace.amenities[item].id == amenity_id):
            del(newplace.amenities[item])
            storage.save()
            response = {}
            return jsonify(response), 200
    abort(404)


def create_amenities(place_id, amenity_id):
    """
        Links a amenity object
        Return: linked amenity object
    """
    newplace = check_id(place.Place, place_id)
    get_amenity = check_id(amenity.Amenity, amenity_id)
    for item in range(len(newplace.amenities)):
        if (newplace.amenities[item].id == amenity_id):
            return jsonify(get_amenity.to_dict()), 200
    newplace.amenities.append(get_amenity)
    storage.save()
    return jsonify(get_amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 defaults={'amenity_id': None},
                 strict_slashes=False)
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def places_amenities(place_id, amenity_id):
    """
        Handle amenities requests with needed functions
    """
    if (request.method == "GET"):
        return get_amenities(place_id)
    elif (request.method == "DELETE"):
        return delete_amenities(place_id, amenity_id)
    elif (request.method == "POST"):
        return create_amenities(place_id, amenity_id)
