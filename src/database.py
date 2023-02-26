import os
from flask import Blueprint, jsonify, request
import openai
from pymongo import MongoClient
from bson import ObjectId

# Connect to mongodb
db_client = MongoClient(os.getenv("MONGO_DB_URL"))
db = db_client['userresearch']
collection = db['interviews']

database_bp = Blueprint('database_bp', __name__)

@database_bp.route('/database')
def get_first_user_interview():
    result = collection.find_one({}, {'userid': 1, '_id': 1, 'title': 1})
    result['_id'] = str(result['_id'])
    return jsonify(result)