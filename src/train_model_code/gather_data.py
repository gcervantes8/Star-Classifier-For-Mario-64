# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 13:59:41 2018

@author: Gerardo Cervantes
"""

#This script is for gathering data from using an existing Keras model to gather data
#from screenshots in a single directory and creating a main directory, and putting the
#image in the correct directory


#Module in src folder to load images
from sys import path
path.insert(0, '../')

#import os
#from star_classifier import predict_star_number_from_screenshot
from load_images import pil_images_from_paths, pil_imgs_to_numpy, get_images_from_dir
import numpy as np
from create_directories import create_main_directory, create_subdirectory
import os

#Image_directory has a folder of images that it should classify
#Model_file_path is the filepath to the Keras model that will do the classification
def classify_images(image_directory, model_file_path):
    from keras import backend as K
    K.clear_session()
    from keras.models import load_model
    model = load_model(model_file_path)
    
    image_paths = get_images_from_dir(image_directory)
    
    
    is_full_game_screenshot = True
    pil_images = pil_images_from_paths(image_paths, is_full_game_screenshot)
    numpy_images = pil_imgs_to_numpy(pil_images)
    nn_output = model.predict(numpy_images)
    predictions = np.argmax(nn_output, axis = 1)
    return image_paths, predictions
    
#Assumes image directory has a main_directory structure of folders
#Screenshot_tag is the folder where it should place the image in
def images_to_main_directory(image_directory, screenshot_tag, image_paths, predictions):
    
    for i, pred in enumerate(predictions):
        os.path.join(image_directory, str(pred))
        os.rename(image_paths[i], os.path.join(image_directory, str(pred), screenshot_tag, os.path.basename(image_paths[i])))

        
if __name__ == "__main__":
    image_directory = r'E:\MarioStarClassifier\dwhatever14159'
    screenshot_tag = 'dwhatever14159'
    model_path = '../../models/High_acc_model_205_imgs_30epochs.hdf5'
    #For debugging to be able to look at images produced
    
    image_paths, predictions = classify_images(image_directory, model_path)
    create_main_directory(image_directory, 122)
    create_subdirectory(image_directory, screenshot_tag)
    images_to_main_directory(image_directory, screenshot_tag, image_paths, predictions)
    