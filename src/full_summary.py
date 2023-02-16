
# Summarize user interviews

import pandas as pd
import openai
import re
from dotenv import load_dotenv
import os
from os.path import splitext, exists

# load OpenAI key
load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# ### Tokenize
import nltk
import ssl
#nltk.download('punkt')

from nltk.tokenize import word_tokenize

# Split into chunks
filename = "imports/summary-all.csv"

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

chunks = break_up_file_to_chunks(filename)
for i, chunk in enumerate(chunks):
    prompt_request = "Summarize this user research: " + convert_to_detokenized_text(chunks[i])
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=.5,
            max_tokens=500,
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

meeting_summary = response["choices"][0]["text"]
print(meeting_summary)

