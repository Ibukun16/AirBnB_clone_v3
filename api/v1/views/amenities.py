#!/usr/bin/python3
"""amenity route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get.yml', methods=['GET'])
def get_all_amenities():
    """ get all amenities by their id """
    all_amenities = [amen.to_dict() for amen in storage.all(Amenity).values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_id.yml', methods=['GET'])
def get_amenity(amenity_id):
    """ get an amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete an amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post.yml', methods=['POST'])
def create_amenity():
    """ create new amenity instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    response = request.get_json()
    amenity = Amenity(**response)
    state.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put.yml', methods=['PUT'])
def update_amenity(amenity_id):
    """ update amenity method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
