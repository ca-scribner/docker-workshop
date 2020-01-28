#!/usr/bin/env python

# based on https://brandonserna.github.io/fastapi/

# A more verbose explanation of what/why with fastapi (and compared to flask):
# https://www.pluralsight.com/tech-blog/porting-flask-to-fastapi-for-ml-model-serving/

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import io
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from inference import cat_or_dog
from base64 import b64decode

app = FastAPI()

class Image(BaseModel):
    filename: str
    image: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/guess/")
async def classify(image: Image):
    im = image.image.split(';base64,')[1]
    return {
        'filename' : image.filename, 
        'label' : cat_or_dog(b64decode(im))
    }
