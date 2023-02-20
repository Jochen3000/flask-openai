from flask import Blueprint, jsonify

default_bp = Blueprint('default_bp', __name__)

@default_bp.route('/', methods=['GET'])
def hello_world():
    return "<p>Hello, Blueprint!</p>"



