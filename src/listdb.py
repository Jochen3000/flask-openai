import os
from flask import Blueprint, jsonify, request
import openai
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
import certifi

# Connect to mongodb
connection_string = os.getenv('MONGO_DB_URL')
db_client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = db_client['userresearch']
collection = db['interviews']

listdb_bp = Blueprint('listdb_bp', __name__)

@listdb_bp.route('/listdb', methods=['GET'])
def get_first_user_interview():
    cursor = collection.find({}, {'_id': 1, 'title': 1})
    result = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        result.append(json.loads(json_util.dumps(document)))
    return jsonify(result)