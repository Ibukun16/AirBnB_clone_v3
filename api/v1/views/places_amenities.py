#!/usr/bin/python3
"""places_amenities route handler for API"""
from api.v1.views import app_views
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def handle_places_amenities(place_id=None, amenity_id=None):
    '''The method handler for the places endpoint.
    '''
    handlers = {
        'GET': get_allamenities,
        'DELETE': delete_amenities,
        'POST': update_amenities
    }
    if request.method in handlers:
        return handlers[request.method](place_id, amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_allamenities(place_id=None, amenity_id=None):
    '''Gets the amenities of a place with the given id.
    '''
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            all_amenities = list(map(lambda obj: obj.to_dict(),
                                     place.amenities))
            return jsonify(all_amenities)
    raise NotFound()


def delete_amenities(place_id=None, amenity_id=None):
    '''Removes an amenity with a given id from a place with a given id.
    '''
    if place_id and amenity_id:
        place = storage.get(Place, place_id)
        if not place:
            raise NotFound()
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            raise NotFound()
        link_place_amenity = list(
            filter(lambda obj: obj.id == amenity_id, place.amenities)
        )
        if not link_place_amenity:
            raise NotFound()
        if storage_t == 'db':
            link_amenity_place = list(
                filter(lambda obj: obj.id == place_id, amenity.place_amenities)
            )
            if not link_amenity_place:
                raise NotFound()
            place.amenities.remove(amenity)
            place.save()
            return jsonify({}), 200
        else:
            indx_amenity = place.amenity_ids.index(amenity_id)
            place.amenity_ids.pop(idnx_amenity)
            place.save()
            return jsonify({}), 200
    raise NotFound()


def update_amenities(place_id=None, amenity_id=None):
    '''Adds an amenity with a given id to a place with a given id.
    '''
    if place_id and amenity_id:
        place = storage.get(Place, place_id)
        if not place:
            raise NotFound()
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            raise NotFound()
        if storage_t == 'db':
            link_place_amenity = list(
                filter(lambda obj: obj.id == amenity_id, place.amenities)
            )
            link_amenity_place = list(
                filter(lambda obj: obj.id == place_id, amenity.place_amenities)
            )
            if link_amenity_place and link_place_amenity:
                data = amenity.to_dict()
                del data['place_amenities']
                return jsonify(data), 200
            place.amenities.append(amenity)
            place.save()
            data = amenity.to_dict()
            del data['place_amenities']
            return jsonify(data), 201
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.push(amenity_id)
            place.save()
            return jsonify(amenity.to_dict()), 201
    raise NotFound()
