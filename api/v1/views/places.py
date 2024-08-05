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
    place_city = storage.get(City, city_id)
    if place_city is None:
        abort(404)
    all_places = [place.to_dict() for place in place_city.places]
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


@app_views.route('/placs/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/places/delete.yml', methods=['DELETE'])
def delete_place(place_id):
    """ delete a placee by its id"""
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
    place_city = storage.get(City, city_id)
    if place_city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    response = request.get_json()
    response['city_id'] = city_id
    user_place = storage.get(User, response['user_id'])
    if user_place is None:
        abort(404)
    newplace = Place(**response)
    newplace.save()
    return jsonify(newplace.to_dict()), 201


@app_views.route('/places/<string:placee_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/places/put.yml', methods=['PUT'])
def update_state(place_id):
    """ update place method """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place = storage.get(Place, placee_id)
    if place is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/search.yml', methods=['POST'])
def search_place():
    """ search a place by its id """
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    placedata = request.get_json()

    if placedata and len(placedata):
        stayts = placedata.get('states', None)
        cyty = placedata.get('cities', None)
        amnyty = placedata.get('amenities', None)

    if not placedata or not len(placedata) or (
            not stays and
            not cyty and
            not amnyty):
        plcs = storage.all(Place).values()
        list_allplaces = []
        for pl in plcs:
            list_allplaces.append(pl.to_dict())
        return jsonify(list_allplaces)

    list_allplaces = []
    if stayts:
        states_list = [storage.get(State, stateid) for stateid in stayts]
        for st in states_list:
            if st:
                for ct in st.cyty:
                    if ct:
                        for pl in ct.plc:
                            list_allplaces.append(pl)

    if cyty:
        city_list = [storage.get(City, cityid) for cityid in cyty]
        for ct in city_list:
            if ct:
                for pl in ct.plcs:
                    if pl not in list_allplaces:
                        list_allplaces.append(pl)

    if amnty:
        if not list_allplaces:
            list_allplaces = storage.all(Place).values()
        amenities_list = [storage.get(Amenity, amtyid) for amtyid in amnty]
        list_allplaces = [pl for pl in list_allplaces
                          if all([amenty in pl.amnty
                                  for amenty in amenities_list])]

    plcs = []
    for plc in list_allplaces:
        delet = plc.to_dict()
        delet.pop('amenities', None)
        plcs.append(delet)

    return jsonify(plcs)
