from flask import Blueprint, jsonify, request

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']  
    file.save('imports/' + file.filename)  
    return 'File uploaded successfully'



