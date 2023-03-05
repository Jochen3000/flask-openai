import os
from flask import Blueprint, jsonify, request
import openai
import certifi
from pymongo import MongoClient
from bson import ObjectId

database_bp = Blueprint('database_bp', __name__)

@database_bp.route('/database')
def get_first_user_interview():
    # Connect to mongodb
    connection_string = os.getenv('MONGO_DB_URL')
    db_client = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = db_client['userresearch']
    collection = db['interviews']
    
    result = collection.find_one({}, {'userid': 1, '_id': 1, 'title': 1})
    result['_id'] = str(result['_id'])
    return jsonify(result)