from flask import Blueprint, jsonify
import openai
import pandas as pd
from nltk.tokenize import word_tokenize

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

full_summary_bp = Blueprint('full_summary_bp', __name__)

@full_summary_bp.route('/full-summary', methods=['GET'])
def summarize():
    chunks = break_up_file_to_chunks(filename)
    for i, chunk in enumerate(chunks):
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
        prompt_response.append(response["choices"][0]["text"])

    prompt_request = "Consolidate these user research summaries: " + str(prompt_response)

    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )

    full_summary = response["choices"][0]["text"]
    return jsonify({'summary': full_summary})