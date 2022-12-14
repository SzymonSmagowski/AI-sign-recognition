# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aF8-KWeYllT1uP8PTmFsJ1_vyfz0vlXm
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

import tensorflow as tensorflow
from tensorflow import keras
import keras.utils
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import random
import PIL
# importing libraries



!pip install anvil-uplink

import os
from google.colab import drive
drive.mount('/content/drive')
Root = "/content/drive/MyDrive/archive(1)"
os.chdir(Root)
# setting a proper folder in google drive

imgs_path = "/content/drive/MyDrive/archive(1)/Train"
data_list = []
labels_list = []
classes_list = 43
for i in range(classes_list):
    i_path = os.path.join(imgs_path, str(i)) #0-42
    for img in os.listdir(i_path):
        im = Image.open(i_path +'/'+ img)
        im = im.resize((32,32))
        im = np.array(im)
        data_list.append(im)
        labels_list.append(i)
data = np.array(data_list)
labels = np.array(labels_list)
# loading the data from the folder

plt.figure(figsize = (12,12))

for i in range(4) :
    plt.subplot(1, 4, i+1)
    plt.imshow(data[i], cmap='gray')

plt.show()
# showing what data looks like

from tensorflow.keras.utils import to_categorical

def prep_dataset(X,y):
    X_prep = X.astype('float32')
    y_prep = to_categorical(np.array(y))
    return (X_prep, y_prep)

X, y = prep_dataset(data,labels)

# preparing a data set

X_train, X_val, Y_train, Y_val = train_test_split(X,y, test_size=0.2, shuffle=True,stratify=y)
X_val, X_test, Y_val, Y_test = train_test_split(X_val,Y_val, test_size=0.5, shuffle=True)

#dividing between train and validation test

from tensorflow.keras import models, layers

model = keras.models.Sequential([
		keras.layers.Rescaling(scale=1./255.),
		keras.layers.Conv2D(filters=72, kernel_size=(3, 3), strides=1,
							activation="relu",  input_shape=X.shape[1:]),
		keras.layers.MaxPooling2D(pool_size=(2), strides=2),
		keras.layers.Conv2D(filters=72, kernel_size=(5, 5), strides=1, activation="relu"),
		keras.layers.MaxPooling2D(pool_size=(2), strides=2),
		keras.layers.Conv2D(filters=144, kernel_size=(5, 5), activation="relu"),
		keras.layers.MaxPooling2D(pool_size=(1)),
		keras.layers.Flatten(),
		keras.layers.Dense(units=86, activation="relu"),
		keras.layers.BatchNormalization(),
		keras.layers.Dropout(0.2),
		keras.layers.Dense(units=43, activation="softmax"),
	])
# creating a sequential model

model.compile(optimizer='adam',
             loss='categorical_crossentropy',
             metrics=['accuracy'])

history= model.fit(X_train,Y_train,
                 epochs=4,
                 batch_size=64,
                 validation_data=(X_val,Y_val))
# fitting data to a model

import json
with open('classes.json', 'r') as fp:
		CLASSES = json.load(fp)
# this is the file with names of signs

img = Image.open("00006.png")
img = img.resize((32,32))

from numpy import argmax

from tensorflow.io import read_file
from tensorflow.image import decode_png, resize
img = read_file("00006.png")
img = decode_png(img, channels=3)
img = resize(img, [32, 32])
img = img[None,:,:,:]
predicted_class = argmax(model.predict(img), axis=-1)
print('The sign is: ', CLASSES[str(predicted_class[0])])
# this is just an example

fig, ax=plt.subplots(2,1,figsize=(12,10))
fig.suptitle('Train evaluation')


sns.lineplot(ax= ax[0],x=np.arange(0,len(history.history['accuracy'])),y=history.history['accuracy'])
sns.lineplot(ax= ax[0],x=np.arange(0,len(history.history['accuracy'])),y=history.history['val_accuracy'])

ax[0].legend(['Train','Validation'])
ax[0].set_title('Accuracy')
ax[0].set_ylabel("Accuracy")
ax[0].set_xlabel("Epoch number")

sns.lineplot(ax= ax[1],x=np.arange(0,len(history.history['loss'])),y=history.history['loss'])
sns.lineplot(ax= ax[1],x=np.arange(0,len(history.history['loss'])),y=history.history['val_loss'])

ax[1].legend(['Train','Validation'])
ax[1].set_title('Loss')
ax[1].set_ylabel("Loss")
ax[1].set_xlabel("Epoch number")
# creating charts and plotting them

Y_test = np.argmax(Y_test,axis=1)

Y_pred= model.predict(X_test)

Y_pred = np.argmax(Y_pred, axis=1)

print('-Acuracy achieved: {:.2f}%\n-Accuracy by model was: {:.2f}%\n-Accuracy by validation was: {:.2f}%'.
      format(accuracy_score(Y_test,Y_pred)*100,(history.history['accuracy'][-1])*100,(history.history['val_accuracy'][-1])*100))
# getting some accuracy and validation

import anvil.server
anvil.server.connect('OIEZHARKQDRZZPSJCQ2ZIDV4-YJAT3AWAJXN3PEGD')

# this is connection to we application

from keras.preprocessing.image import load_img
from numpy import amax

import anvil.media
@anvil.server.callable
def classify_image(file):
  with anvil.media.TempFile(file) as filename:
    img = read_file(filename)
  img = decode_png(img, channels=3)
  img = resize(img, [32, 32])
  img = img[None,:,:,:]
  score = argmax(model.predict(img), axis=-1)
  
  tmp = model.predict(img)[0].tolist()
  result = "The sign is: " + CLASSES[str(score[0])]
  count=0
  if amax(model.predict(img), axis=-1)<0.93:
    result = "The sign is not recognized."
  else:
    result += "\n"
    result += "\n"
    result += "Result for each sign:"
    result += "\n"
    for i in tmp:
      result += CLASSES[str(count)]
      result += ": "
      result += str(i)
      result += ".\n"
      count +=1
  return result
# function for loading the sign from web application

from sklearn import metrics
# https://towardsdatascience.com/multi-class-metrics-made-simple-part-i-precision-and-recall-9250280bddc2
# we should not look at f1 score that much with so many classifiers
flat = Y_test.flatten()
flat2 = Y_pred.flatten()

# indexes are classifiers
classification = metrics.classification_report(flat, flat2,digits=3)
print(classification)
# printing data about precision, recall, f1-score and counter

!pip install pyyaml h5py

model.save('my_model.h5')