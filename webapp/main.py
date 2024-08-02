import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import hashlib


current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")

# add a pydantic model for text string


class Text(BaseModel):
    text: str

# Create a FastAPI endpoint that accepts a POST request with a JSON body
# containing a single field called "text" and returns a checksum of the text
# using the SHA-256 algorithm.


@app.post('/checksum')
def calculate_checksum(text: Text):
    """
    Calculate the checksum of the provided text using the SHA-256 algorithm.
    Example POST request body:

    {
        "text": "Hello, World!"
    }
    """
    checksum = hashlib.sha256(text.text.encode()).hexdigest()
    return {'checksum': checksum}


class Body(BaseModel):
    length: Union[int, None] = 20


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default.
    Example POST request body:

    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    return {'token': string}