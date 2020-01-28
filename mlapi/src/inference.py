#!/bin/python3

# https://www.kaggle.com/vanausloos/solution-dogs-vs-cats-svm-model-model-2/data

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
import scipy
import numpy as np # linear algebra
import sklearn as sk
from numpy import array
import os
import io
#import skimage as ski
from PIL import Image 
from PIL import ImageFilter
from sklearn.svm import LinearSVC, SVC
#from sklearn.calibration import CalibratedClassifierCV
#from sklearn.linear_model import LogisticRegression
#import re

from subprocess import check_output
#print(check_output(["ls", "../input"]).decode("utf8"))

# Could set this as an environment variable.  In here we could have a use env var else use default
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'clf.joblib'))

from joblib import load
print(f"Loading model from {MODEL_PATH}")
clf = load(MODEL_PATH)

def cat_or_dog(bs):
    #pil_im = Image.frombytes(io.BytesIO(bs)).convert('L')
    pil_im = Image.open(io.BytesIO(bs)).convert('L')
    size=64,64
    pil_im = pil_im.resize(size, Image.ANTIALIAS)
    #pil_im =pil_im.filter(ImageFilter.FIND_EDGES)
    pil_im=pil_im.filter(ImageFilter.GaussianBlur(255))
    pix_val=pil_im.histogram()     
    result = clf.predict([pix_val])
    if result < 0.5:
        return "Cat"
    else:
        return "Dog"
