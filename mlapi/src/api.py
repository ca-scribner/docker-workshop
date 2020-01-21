#!/usr/bin/env python

# based on https://brandonserna.github.io/fastapi/

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import io
from inference import cat_or_dog

app = FastAPI()

#class Image(BaseModel):
#    name: str
#    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/guess")
async def classify(request: Request, file: bytes=File(...)):
    return {
        item.name : cat_or_dog(image.content)
    }
