from flask import Blueprint, jsonify, request
import openai
import tempfile
import os

whisper_bp = Blueprint('whisper_bp', __name__)

@whisper_bp.route('/whisper', methods=['POST'])
def whisper_submit():
    file = request.files['file']
    print('uploaded file', file)

    # create a temporary directory to store the uploaded file
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    # load the temporary file to generate the transcript
    with open(file_path, 'rb') as f:
        transcript = openai.Audio.transcribe("whisper-1", f)

    # delete the temporary directory and its contents
    os.remove(file_path)
    os.rmdir(temp_dir)

    # create a response JSON object
    response_data = {"transcript": transcript}

    # set the Content-Type header to application/json
    headers = {"Content-Type": "application/json"}

    # return the response as JSON with the appropriate header
    return jsonify(response_data), 200, headers

