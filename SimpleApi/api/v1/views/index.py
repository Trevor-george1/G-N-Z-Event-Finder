#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import pymongo
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




#  post likes
#=================
  
@app_views.route('/events/<event_id>/like', methods=['POST'], strict_slashes=False)
def add_likes(event_id):
    if event_id is None:
        abort(404)
    try:
        event_id_obj = ObjectId(event_id)
    
        event = event_collection.find({'_id': event_id_obj})

        if not event:
          return jsonify({"message": "event not found"}), 404
    
    #increment likes count
        updated_event = event_collection.update_one(
            {'_id': event_id_obj},
            {'$inc': {'likes': 1}}
        )
        if updated_event.modified_count > 0:
          return jsonify({"message": "Event liked successfully"}), 200
        else:
          return jsonify({"message": "Event already liked"}), 400
    except ValueError:
        abort(400, f"Invalid event ID: '{event_id}'")



@app_views.route('/most_liked_events', methods=['GET'])
def get_most_liked_events():
    pipeline = [
        {"$sort": {"likes": -1}},
        {"$limit": 5},
        {"$project": {
           "name": "$name",
           "venue": "$venue",
           "likes": "$likes"
        }}
    ]
    
    most_liked_events = list(db.events.aggregate(pipeline))
    for event in most_liked_events:
        event['_id'] = str(event['_id'])
    
    return jsonify(most_liked_events), 200