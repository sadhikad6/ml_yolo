# -*- coding: utf-8 -*-
"""Facial Recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iFRKJ9VfAGG9EqfMlU3-oAU0lSAm6acM
"""

#Sadhika Dhanasekar
#Facial Recognition Lab
#05.18.2021
#using PyPi's DeepFace: https://pypi.org/project/deepface/

#!pip install deepface

#verification: coparing two faces - for testing
from deepface import DeepFace
result  = DeepFace.verify("taylorswift.jpeg", "tswift.jpeg")
print("Is verified: ", result["verified"])

#recognition: find target image(s) in a database - for testing
import pandas as pd
df = DeepFace.find(img_path = "taylorswift.jpeg", db_path = "/content/tswifts")

changing the models: typically FaceNet does the best
models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
for model in models:
   result = DeepFace.verify("img1.jpg", "img2.jpg", model_name = model)
   df = DeepFace.find(img_path = "img1.jpg", db_path = "C:/workspace/my_db", model_name = model)

#similarity metric: euclidean_l2 seems to be the most stable
metrics = ["cosine", "euclidean", "euclidean_l2"]
for metric in metrics:
   result = DeepFace.verify("img1.jpg", "img2.jpg", distance_metric = metric)
   df = DeepFace.find(img_path = "img1.jpg", db_path = "C:/workspace/my_db", distance_metric = metric)

#Sadhika Dhanasekar
#Facial Recognition Lab
#05.18.2021
#using PyPi's DeepFace: https://pypi.org/project/deepface/
#referenced tutorial: https://gist.github.com/EncodeTS/6bbe8cb8bebad7a672f0d872561782d9

#!pip install deepface

from keras.models import Model
from keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout
from PIL import Image
import numpy as np

def vgg_face(weights_path=None):
    img = Input(shape=(3, 224, 224))

    pad1_1 = ZeroPadding2D(padding=(1, 1))(img)
    conv1_1 = Convolution2D(64, 3, 3, activation='relu', name='conv1_1')(pad1_1)
    pad1_2 = ZeroPadding2D(padding=(1, 1))(conv1_1)
    conv1_2 = Convolution2D(64, 3, 3, activation='relu', name='conv1_2')(pad1_2)
    pool1 = MaxPooling2D((2, 2), strides=(2, 2))(conv1_2)

    pad2_1 = ZeroPadding2D((1, 1))(pool1)
    conv2_1 = Convolution2D(128, 3, 3, activation='relu', name='conv2_1')(pad2_1)
    pad2_2 = ZeroPadding2D((1, 1))(conv2_1)
    conv2_2 = Convolution2D(128, 3, 3, activation='relu', name='conv2_2')(pad2_2)
    pool2 = MaxPooling2D((2, 2), strides=(2, 2))(conv2_2)

    pad3_1 = ZeroPadding2D((1, 1))(pool2)
    conv3_1 = Convolution2D(256, 3, 3, activation='relu', name='conv3_1')(pad3_1)
    pad3_2 = ZeroPadding2D((1, 1))(conv3_1)
    conv3_2 = Convolution2D(256, 3, 3, activation='relu', name='conv3_2')(pad3_2)
    pad3_3 = ZeroPadding2D((1, 1))(conv3_2)
    conv3_3 = Convolution2D(256, 3, 3, activation='relu', name='conv3_3')(pad3_3)
    pool3 = MaxPooling2D((2, 2), strides=(2, 2))(conv3_3)

    pad4_1 = ZeroPadding2D((1, 1))(pool3)
    conv4_1 = Convolution2D(512, 3, 3, activation='relu', name='conv4_1')(pad4_1)
    pad4_2 = ZeroPadding2D((1, 1))(conv4_1)
    conv4_2 = Convolution2D(512, 3, 3, activation='relu', name='conv4_2')(pad4_2)
    pad4_3 = ZeroPadding2D((1, 1))(conv4_2)
    conv4_3 = Convolution2D(512, 3, 3, activation='relu', name='conv4_3')(pad4_3)
    pool4 = MaxPooling2D((2, 2), strides=(2, 2))(conv4_3)

    pad5_1 = ZeroPadding2D((1, 1))(pool4)
    conv5_1 = Convolution2D(512, 3, 3, activation='relu', name='conv5_1')(pad5_1)
    pad5_2 = ZeroPadding2D((1, 1))(conv5_1)
    conv5_2 = Convolution2D(512, 3, 3, activation='relu', name='conv5_2')(pad5_2)
    pad5_3 = ZeroPadding2D((1, 1))(conv5_2)
    conv5_3 = Convolution2D(512, 3, 3, activation='relu', name='conv5_3')(pad5_3)
    pool5 = MaxPooling2D((2, 2), strides=(2, 2))(conv5_3)

    flat = Flatten()(pool5)
    fc6 = Dense(4096, activation='relu', name='fc6')(flat)
    fc6_drop = Dropout(0.5)(fc6)
    fc7 = Dense(4096, activation='relu', name='fc7')(fc6_drop)
    fc7_drop = Dropout(0.5)(fc7)
    out = Dense(2622, activation='softmax', name='fc8')(fc7_drop)

    model = Model(input=img, output=out)

    if weights_path:
        model.load_weights(weights_path)

    return model

if __name__ == "__main__":
    im = Image.open('A.J._Buckley.jpg')
    im = im.resize((224,224))
    im = np.array(im).astype(np.float32)
    #    im[:,:,0] -= 129.1863
    #    im[:,:,1] -= 104.7624
    #    im[:,:,2] -= 93.5940
    im = im.transpose((2,0,1))
    im = np.expand_dims(im, axis=0)

    # Test pretrained model
    model = vgg_face('vgg-face-keras-fc.h5')
    out = model.predict(im)
    print(out[0][0])