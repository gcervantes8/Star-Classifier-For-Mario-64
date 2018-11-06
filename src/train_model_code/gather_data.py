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
import os
from glob import glob
#Image_directory has a folder of images that it should classify
#Model_file_path is the filepath to the Keras model that will do the classification
def classify_images(image_directory, model_file_path):
#    print(image_directory)
    image_paths = get_images_from_dir(image_directory)
#    print(image_paths)
    is_full_game_screenshot = True
    _, _, predictions = classify_from_image_paths(image_paths, model_file_path, is_full_game_screenshot)
    return image_paths, predictions
    
def classify_from_image_paths(image_paths, model_path, is_full_game_screenshot):
    if image_paths == []:
        return [], [], []
    
    from keras import backend as K
    K.clear_session()
    from keras.models import load_model
    model = load_model(model_path)
    
    pil_images = pil_images_from_paths(image_paths, is_full_game_screenshot)
    numpy_images = pil_imgs_to_numpy(pil_images)
    nn_output = model.predict(numpy_images)
    predictions = np.argmax(nn_output, axis = 1)
    return pil_images, nn_output, predictions
    

#Assumes image directory has a main_directory structure of folders
#Screenshot_tag is the folder where it should place the image in
def images_to_main_directory(image_directory, screenshot_tag, image_paths, predictions):
    
    for i, pred in enumerate(predictions):
        os.path.join(image_directory, str(pred))
        os.rename(image_paths[i], os.path.join(image_directory, str(pred), screenshot_tag, os.path.basename(image_paths[i])))

#Goes through main directories and classifies all the images in there
#Prints directory path and outputs image onto console if model gave different classification than label it has
#n_stars which star folders to go through
def check_classifications(main_directories, model_file_path, n_stars):
    from os import path
    from IPython.display import display

    for i in range(n_stars):
        star_sub_directories = []
        for directory in main_directories:
            star_sub_directories.append(path.join(directory, str(i)))
            
        for star_directory in star_sub_directories:
            player_star_directories = glob(star_directory + '/*/')
            for player_dir in player_star_directories:
                image_paths, predictions = classify_images(player_dir, model_file_path)
                if image_paths != []:
                    image_paths = np.array(image_paths)
                    indices = np.where(predictions != i)
                    pil_images = pil_images_from_paths(image_paths[indices], True)
                    print(image_paths[indices])
                    for img in pil_images:
                        display(img)
                  
    
        
if __name__ == "__main__":
#    image_directory = r'E:\MarioStarClassifier\dwhatever14159'
#    screenshot_tag = 'dwhatever14159'
    model_file_path = '../../models/Model-imgs_perclass326epochs35'
#    model_file_path = '../../models/Model-imgs_perclass325epochs50moreRegularization'
#    #For debugging to be able to look at images produced
#    
#    image_paths, predictions = classify_images(image_directory, model_file_path)
#    create_main_directory(image_directory, 122)
#    create_subdirectory(image_directory, screenshot_tag)
#    images_to_main_directory(image_directory, screenshot_tag, image_paths, predictions)
#    
#    main_directories = [r'E:\MarioStarClassifier\train_images']
    main_directories = [r'E:\MarioStarClassifier\halliinen_14347', 
                          r'E:\MarioStarClassifier\puncayshun_120_13949', r'E:\MarioStarClassifier\viro14421',
                          r'E:\MarioStarClassifier\caivs15818', r'E:\MarioStarClassifier\batora13953',
                          r'E:\MarioStarClassifier\dwhatever14159', r'E:\MarioStarClassifier\mitagi14445',
                          r'E:\MarioStarClassifier\test_images']
    check_classifications(main_directories, model_file_path, 120)
    
    