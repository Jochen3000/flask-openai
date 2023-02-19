import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
from os.path import splitext, exists
from src.summary import break_up_file_to_chunks, convert_to_detokenized_text
from nltk.tokenize import word_tokenize
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Get OpenAI key
load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load csv
df = pd.read_csv("imports/summary-all.csv")
filename = "imports/summary-all.csv"

# Create instance of flask
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):

	@marshal_with(resource_fields)
	def put(self):
		args = video_put_args.parse_args()

		# Create a new video model instance with the provided data
		video = VideoModel(name=args['name'], views=args['views'], likes=args['likes'])
		
		# Add the new video to the database
		db.session.add(video)
		db.session.commit()

		# Return the new video model instance and a status code of 201
		return video, 201

api.add_resource(Video, "/video")


# Home route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']  
    file.save('imports/' + file.filename)  
    return 'File uploaded successfully'

# Simple Prompt
@app.route('/simple-prompt', methods=['POST'])
def simple_prompt():
    prompt = request.form['prompt']
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
    return response.choices[0].text

# Short Summary
@app.route('/short-summary', methods=['GET'])
def short_summary():
    chunks = break_up_file_to_chunks(filename)
    prompt_request = "Summarize this user research: " + convert_to_detokenized_text(chunks[0])
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=.5,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    short_summary = response["choices"][0]["text"]
    return jsonify({'summary': short_summary})

# Full Summary
prompt_response = []

@app.route('/full-summary', methods=['GET'])
def summarize():
    chunks = break_up_file_to_chunks(filename)
    for i, chunk in enumerate(chunks):
        prompt_request = "Summarize this user research: " + convert_to_detokenized_text(chunks[0])
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_request,
                temperature=.5,
                max_tokens=200,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
        )
        prompt_response.append(response["choices"][0]["text"])

    prompt_request = "Consolidate these user research summaries: " + str(prompt_response)

    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )

    full_summary = response["choices"][0]["text"]
    return jsonify({'summary': full_summary})

if __name__ == '__main__':
    app.run()



