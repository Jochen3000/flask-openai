import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
from os.path import splitext, exists
from src.short_summary import break_up_file_to_chunks, convert_to_detokenized_text
from nltk.tokenize import word_tokenize

# Get OpenAI key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load csv
df = pd.read_csv("imports/summary-all.csv")
filename = "imports/summary-all.csv"

# Create instance of flask
app = Flask(__name__)

# Home route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

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


if __name__ == '__main__':
    app.run()



