import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import Image

import tensorflow as tensorflow
from tensorflow import keras
import keras.utils
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import random
import PIL
import anvil.media
import anvil.server
import json

# !pip install anvil-uplink -install this
from keras.preprocessing.image import load_img
from numpy import amax

with open("classes.json", 'r') as fp:
		CLASSES = json.load(fp)

anvil.server.connect('OIEZHARKQDRZZPSJCQ2ZIDV4-YJAT3AWAJXN3PEGD')

model = tensorflow.keras.models.load_model('my_model.h5')

@anvil.server.callable
def classify_image(file):
  with anvil.media.TempFile(file) as filename:
    img = tensorflow.io.read_file(filename)
  img = tensorflow.image.decode_png(img, channels=3)
  img = tensorflow.image.resize(img, [32, 32])
  img = img[None,:,:,:]
  score = np.argmax(model.predict(img), axis=-1)
  
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

print("Open an application now!")
while True:pass