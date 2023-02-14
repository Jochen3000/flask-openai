import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
import re
from os.path import splitext, exists
import nltk
import ssl

# Get OpenAI key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize tokenizer
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# Load csv
df = pd.read_csv("imports/summary-all.csv")
filename = "imports/summary-all.csv"

# Create instance of flask
app = Flask(__name__)

# Test route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

###############
# Simple Prompt
###############
@app.route('/generate-text', methods=['POST'])
def generate_text():
    prompt = request.form['prompt']
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
    return response.choices[0].text

################
# Summary Prompt
################
@app.route('/summarize', methods=['POST'])
def say_hi():
    response = 'hi'
    return response

# @app.route('/search')
# def search():
#     # Get the search query from the URL query string
#     query = request.args.get('query')

#     search_term_vector = get_embedding(query, engine="text-embedding-ada-002")

#     df = pd.read_csv('earnings-embeddings.csv')
#     df['embedding'] = df['embedding'].apply(eval).apply(np.array)
#     df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))
#     sorted_by_similarity = df.sort_values("similarities", ascending=False).head(3)

#     results = sorted_by_similarity['text'].values.tolist()

#        # Return the results as a JSON response
#     return {"query": query, "results": results}

if __name__ == '__main__':
    app.run()



