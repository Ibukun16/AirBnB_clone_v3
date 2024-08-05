#!/usr/bin/python3
"""places_amenities route handler"""
import os
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place
from flasgger.utils import swag_from


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_id.yml', methods=['GET'])
def get_amenities(place_id):
    """ get all amenities from a specific place by their id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(all_amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete.yml', methods=['DELETE'])
def delete_amenities(place_id, amenity_id):
    """ delete amenity identified by its id from a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/place_amenity/post.yml', methods=['POST'])
def update_amenities(place_id, amenity_id):
    """ update amenity list by id """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return (jsonify(amenity.to_dict()), 200)
    place.amenities.append(item)
    storage.save()
    return jsonify(amenity.to_dict()), 201
