#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['GNZ']
event_collection = db['events']

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    stats = event_collection.count_documents({})
    return jsonify({"events": stats})

@app_views.route('/events', strict_slashes=False)
def event():
    events = list(event_collection.find({}))
    events_dict = {str(event['_id']): event for event in events}
    serialized_events = dumps(events_dict)
    deserialized_events = json.loads(serialized_events)
    return jsonify(deserialized_events)


@app_views.route('/events', methods=['POST'], strict_slashes=False)
def new_event():
    data = request.json
    error_message = None
    if not data:
        return jsonify({"Error": "No data provided"}), 400
    
    if data.get('name', "") == "":
        error_message = "Missing name of event"
    if error_message is None:
      try:    
        new_event = {
            'name': data.get('name'),
            'date': data.get('date'),
            'venue': data.get('venue'),
            'time': data.get("time")
        }

        result = event_collection.insert_one(new_event)

        return jsonify({
          "message": "new event added successfully"
        }), 201
      except Exception as e:
              error_message = "Can't create User: {}".format(e)
    return jsonify({'error': error_message}), 400
        
@app_views.route('/events/<event_id>', methods=['GET'], strict_slashes=False)
def view_one_user(event_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if event_id is None:
        abort(404)
    event_id_obj = ObjectId(event_id)
    event = next((doc for doc in event_collection.find({"_id": event_id_obj})), None)
    if event is None:
        abort(404)
    serialized_events = dumps(event)
    deserialized_event = json.loads(serialized_events)
    return jsonify(deserialized_event)

@app_views.route('/events/<event_id>', methods=['DELETE'], strict_slashes=False)
def delete_event(event_id):
    if event_id is None:
        abort(404)
    try:
      event_id_obj = ObjectId(event_id)
      result = event_collection.delete_one({'_id': event_id_obj})

      if result.deleted_count == 0:
          abort(404, f"No event found with ID '{event_id}'")
      return 'Delete Successful!', 204
    except ValueError:
        abort(400, f"Invalid event ID: '{event_id}'")
    