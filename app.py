import os
from dotenv import load_dotenv
from flask import Flask, jsonify
import openai
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# import blueprints
from src.default import default_bp
from src.upload import upload_bp
from src.prompt import prompt_bp
from src.short_summary import short_summary_bp
from src.full_summary import full_summary_bp

# Get OpenAI key
load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create instance of flask
app = Flask(__name__)

# blueprint routes
app.register_blueprint(default_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(short_summary_bp)
app.register_blueprint(full_summary_bp)

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


if __name__ == '__main__':
    app.run()



