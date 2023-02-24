import os
from dotenv import load_dotenv
from flask import Flask, jsonify
import openai
from pymongo import MongoClient
from flask_cors import CORS

# import blueprints
from src.default import default_bp
from src.upload import upload_bp
from src.prompt import prompt_bp
from src.short_summary import short_summary_bp
from src.full_summary import full_summary_bp
from src.query import query_bp

# Get OpenAI key
load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create instance of flask
app = Flask(__name__)

# Allow CORS
CORS(app)

# Connect to mongodb
client = MongoClient('mongodb://localhost:27017/')
db = client['userresearch']
collection = db['interviews']

# blueprint routes
app.register_blueprint(default_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(short_summary_bp)
app.register_blueprint(full_summary_bp)
app.register_blueprint(query_bp)


class UserInterview:
    def __init__(self, data):
        self.id = str(data['_id'])
        self.title = data['title']
        self.userid = data['userid']
        self.summary = data['summary']
        self.text = data['text']
        self.embeddings = data['embeddings']
        self.csv = data['csv']

    def to_json(self):
        return {"id": self.id,
                "title": self.title,
                "userid": self.userid,
                "summary": self.summary,
                "text": self.text,
                "embeddings": self.embeddings,
                "csv": self.csv}

@app.route('/userinterviews/first')
def get_first_user_interview():
    result = collection.find_one()
    if not result:
        return jsonify({'error': 'data not found'})
    else:
        user_interview = UserInterview(result)
        return jsonify(user_interview.to_json())

if __name__ == "__main__":
    app.run()






