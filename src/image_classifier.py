# -*- coding: utf-8 -*-
"""
Created on Sat May 25 11:02:38 2019

@author: Jerry C
"""

import numpy as np
from src.load_images import pil_imgs_to_numpy
import time


# Loads the neural network model, including configuration settings and weights
# Blocks calling thread until the model loads
def _load_nn_model(model_path):
    
    # Clears any previous sessions, bug in keras caused by threading/wrong graph
    from keras import backend as K
    K.clear_session()
            
    # Keras Library to load neural networks (importing from Keras or Tensorflow is slow)
    from keras.models import load_model
    model = load_model(model_path)
    
    return model

    
# Model is the keras loaded model that will make the predictions
# image is the PIL image that it will classify
# Returns 3-tuple (category predicted, probability of prediction, time in seconds)
def classify(image, model):
    start_time = time.time()
    
    img_np = pil_imgs_to_numpy([image])
    nn_output = model.predict(img_np)
    prediction = np.argmax(nn_output)
    prediction_probability = np.max(nn_output)
    
    star_prediction_time = time.time() - start_time
    return prediction, prediction_probability, star_prediction_time
