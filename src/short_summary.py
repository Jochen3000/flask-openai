from flask import Blueprint, jsonify, request
import openai
import os
import pandas as pd
from nltk.tokenize import word_tokenize
import nltk

# Load csv
df = pd.read_csv("imports/summary-all.csv")
filename = "imports/summary-all.csv"

# Split into chunks
def break_up_file(tokens, chunk_size, overlap_size):
    if len(tokens) <= chunk_size:
        yield tokens
    else:
        chunk = tokens[:chunk_size]
        yield chunk
        yield from break_up_file(tokens[chunk_size-overlap_size:], chunk_size, overlap_size)

def break_up_file_to_chunks(filename, chunk_size=2000, overlap_size=100):
    with open(filename, 'r') as f:
        text = f.read()
    tokens = word_tokenize(text)
    return list(break_up_file(tokens, chunk_size, overlap_size))

# ### Summarize
def convert_to_detokenized_text(tokenized_text):
    prompt_text = " ".join(tokenized_text)
    prompt_text = prompt_text.replace(" 's", "'s")
    prompt_text = prompt_text.replace(" 's", "'s")
    prompt_text = prompt_text.replace("\n", " ")
    return prompt_text

prompt_response = []

short_summary_bp = Blueprint('short_summary_bp', __name__)

@short_summary_bp.route('/short-summary', methods=['GET'])
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



