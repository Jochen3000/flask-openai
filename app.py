import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import openai
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId

# import blueprints
from src.default import default_bp
from src.upload import upload_bp
from src.prompt import prompt_bp
from src.short_summary import short_summary_bp
from src.full_summary import full_summary_bp
from src.query import query_bp
from src.query_db import querydb_bp
from src.database import database_bp
from src.listdb import listdb_bp

# configuration
load_dotenv(".env")
app = Flask(__name__)
cors = CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

# blueprint routes
app.register_blueprint(default_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(short_summary_bp)
app.register_blueprint(full_summary_bp)
app.register_blueprint(query_bp)
app.register_blueprint(querydb_bp)
app.register_blueprint(database_bp)
app.register_blueprint(listdb_bp)

@app.route('/test', methods=['POST'])
def hello_world():
    data = request.json
    print(data) 
    return jsonify({"botResponse": 'hello'})


if __name__ == "__main__":
    app.run()






