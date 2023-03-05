import os
import io
from flask import Blueprint, jsonify, request
import openai
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
from openai.embeddings_utils import distances_from_embeddings
import certifi

querydb_bp = Blueprint('querydb_bp', __name__)

@querydb_bp.route('/query-db', methods=['POST'])
def get_answer():
    # Connect to mongodb
    connection_string = os.getenv('MONGO_DB_URL')
    db_client = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = db_client['userresearch']
    collection = db['interviews']

    # Get embeddings from mongodb
    def get_first_user_interview():
        result = collection.find_one({}, {'userid': 1, 'embeddings': 1})
        if result is None:
            return None
        return result['embeddings']

    csv_data = get_first_user_interview()

    # Read the string as a file-like object using StringIO
    csv_file = io.StringIO(csv_data)

    # Read the CSV data from the file-like object using pd.read_csv
    df = pd.read_csv(csv_file, index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

    data = request.json
    question = data['chatPrompt']
    result = answer_question(df, question=question)
    return jsonify({"botResponse": result})

def create_context(question, df, max_len=1800, size="ada"):

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')
    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        
        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4
        
        # If the context is too long, break
        if cur_len > max_len:
            break
        
        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)

def answer_question(
    df,
    model="text-davinci-003",
    question="",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the question and context
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know.\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""
    




