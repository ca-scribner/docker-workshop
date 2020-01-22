#!/usr/bin/env python

# based on https://brandonserna.github.io/fastapi/

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import io
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
