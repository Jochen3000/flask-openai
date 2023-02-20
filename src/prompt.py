from flask import Blueprint, jsonify, request
import openai

prompt_bp = Blueprint('prompt_bp', __name__)

@prompt_bp.route('/prompt', methods=['POST'])
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



