#!/usr/bin/env python

# based on https://brandonserna.github.io/fastapi/

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import io
import base64
import os
from inference import cat_or_dog

app = FastAPI()

class Image(BaseModel):
    filename: str
    image: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/guess/")
async def classify(image: Image):
    fname = '/tmp_' + image.filename
    with open(fname, 'w') as f:
        f.write(image.image.split(';base64,')[1])
    response = {image.filename : cat_or_dog(fname)}
    os.remove(fname)
    return response
