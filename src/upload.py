from flask import Blueprint, jsonify, request

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    title = request.form.get('title')  # extract the title from the form data

    file.save('imports/' + file.filename)

    # Do something with the title (e.g., save it to a database)
    if title:
        # save the title to a database, for example
        print(title)

    return 'File uploaded successfully'



