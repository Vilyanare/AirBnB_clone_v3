#!/usr/bin/python3
'''
    Module containing instructions for the flask blueprint app_views with
    Amenity objects
'''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, classes


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_all_amenities_to_json():
    '''
    When a GET request is made with no specifications, retrieves all amenity
    objects and returns them in JSON form
    '''
    cls_dict = storage.all("Amenity")
    cls_list = []
    for key, value in cls_dict.items():
        cls_list.append(value.to_dict())
    return jsonify(cls_list)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_make_new_amenity():
    '''
    When a POST request is made, an Amenity object is created with the values
    in the request
    Returns:
        Raises a 400 error if no valid JSON or if there is no name
        The new amenity object with code 201
    '''
    post_dict = request.get_json()
    if not post_dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in post_dict:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = classes["Amenity"](**post_dict)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_specific_amenity(amenity_id):
    '''
    When a GET request is made with an extra parameter, this method will
    look for the Amenity ID specified and return the JSON format of that
    object.
    Otherwise, raises a 404
    '''
    cls_obj = storage.get("Amenity", amenity_id)
    if cls_obj is None:
        abort(404)
    else:
        return jsonify(cls_obj.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_spcific_amenity(amenity_id):
    '''
    When a DELETE request is made with the <amenity_id> parameter, this method
    will look for the amenity object that matches and remove it from the
    database
    Otherwise, raises a 404
    '''
    cls_obj = storage.get("Amenity", amenity_id)
    if cls_obj is None:
        abort(404)
    else:
        storage.delete(cls_obj)
        return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def put_specific_amenity(amenity_id):
    '''
    When a PUT request is made, the object that corresponds to the correct
    Amenity ID is updated with the information passed in the request
    Return:
        If no object with ID matches, raise a 404 code
        The amenity object with a status code 200
    '''
    cls_obj = storage.get("Amenity", amenity_id)
    if cls_obj is None:
        abort(404)
    else:
        put_dict = request.get_json()
        if not put_dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        put_dict.pop("id", None)
        put_dict.pop("created_at", None)
        put_dict.pop("updated_at", None)
        for key, value in put_dict.items():
            setattr(cls_obj, key, value)
        cls_obj.save()
        return jsonify(cls_obj.to_dict()), 200
