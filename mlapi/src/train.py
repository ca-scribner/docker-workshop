#!/bin/python3

# taken from
# https://www.kaggle.com/vanausloos/solution-dogs-vs-cats-svm-model-model-2/data

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
import os
import glob
import numpy as np # linear algebra
from PIL import Image
from PIL import ImageFilter
from sklearn.svm import LinearSVC, SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression

#get full dataset
POSITIVE_DIR = '/training_data/Dog/'
NEGATIVE_DIR = '/training_data/Cat/'

DOGS = glob.glob(POSITIVE_DIR + '/*')
CATS = glob.glob(NEGATIVE_DIR + '/*')

images = DOGS + CATS
labels = np.concatenate((
    np.ones(len(DOGS)),
    np.zeros(len(CATS))
))



def preprocess(i):
    try:
        pil_im = Image.open(i).convert('L')
        #pil_im = Image.open(i)
        size=64,64

        pil_im = pil_im.resize(size, Image.ANTIALIAS)
        #pil_im =pil_im.filter(ImageFilter.FIND_EDGES)
        pil_im = pil_im.filter(ImageFilter.GaussianBlur(255))
        pix_val = pil_im.histogram()
        return pix_val
    except:
        return None

#clf = sk.linear_model.LogisticRegression
#clf = LogisticRegression()
clf = LinearSVC(loss='l2', penalty='l1', dual=False)
pixels = map(preprocess, images)

pixels, labels = zip(*[ (p,l) for (p,l) in zip(pixels, labels) if p is not None ])

clf = clf.fit(pixels, labels)

from joblib import dump
dump(clf, "/model/clf.joblib")
