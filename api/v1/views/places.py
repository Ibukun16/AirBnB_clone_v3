#!/usr/bin/python3
"""places route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
from flasgger.utils import swag_from


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/places/get.yml', methods=['GET'])
def get_allplaces(city_id):
    """ get list of all places by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = [place.to_dict() for place in city.places]
    return jsonify(all_places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_place(place_id):
    """ get a place by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/places/delete.yml', methods=['DELETE'])
def delete_place(place_id):
    """ identify and delete a place using its id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/post.yml', methods=['POST'])
def create_newplace():
    """ create new state instance """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    response = request.get_json()
    response['city_id'] = city_id
    user = storage.get(User, response['user_id'])
    if user is None:
        abort(404)
    newplace = Place(**response)
    newplace.save()
    return jsonify(newplace.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/places/put.yml', methods=['PUT'])
def update_place(place_id):
    """ get list of places as updated """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/search.yml', methods=['POST'])
def search_place():
    """ search a place by its id """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    response = request.get_json()
    if response and len(response):
        states = response.get('states', None)
        cities = response.get('cities', None)
        amenities = response.get('amenities', None)

    if not response or not len(response) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_allplaces = []
        for place in places:
            list_allplaces.append(place.to_dict())
        return jsonify(list_allplaces)

    list_allplaces = []
    if states:
        states_list = [storage.get(State, stateid) for stateid in states]
        for state in states_list:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_allplaces.append(place)

    if cities:
        city_list = [storage.get(City, cityid) for cityid in cities]
        for city in city_list:
            if city:
                for place in city.places:
                    if place not in list_allplaces:
                        list_allplaces.append(place)

    if amenities:
        if not list_allplaces:
            list_allplaces = storage.all(Place).values()
        amenities_list = [storage.get(Amenity, amtyid) for amtyid in amenities]
        list_allplaces = [place for place in list_allplaces
                          if all([amenty in place.amenities
                                  for amenty in amenities_list])]


    places = []
    for plc in list_allplaces:
        delet = plc.to_dict()
        delet.pop('amenities', None)
        places.append(delet)

    return jsonify(places)
