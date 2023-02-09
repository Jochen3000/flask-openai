import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/search')
def search():
    # Get the search query from the URL query string
    query = request.args.get('query')

    search_term_vector = get_embedding(query, engine="text-embedding-ada-002")

    df = pd.read_csv('earnings-embeddings.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))
    sorted_by_similarity = df.sort_values("similarities", ascending=False).head(3)

    results = sorted_by_similarity['text'].values.tolist()

    # Render the search results template, passing in the search query and results
    return results



