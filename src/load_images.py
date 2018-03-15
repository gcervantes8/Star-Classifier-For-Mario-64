# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 20:42:17 2017

@author: Gerardo Cervantes
"""

import os
from PIL import Image
from glob import glob
import numpy as np
from keras.preprocessing.image import img_to_array
from preprocess import preprocess_images
import random

#directory_path is the one described in the readme, images and star label will be gotten from this directory
#Addtionally it will generate images from preexisting images, this is done to help with robustness of nn
#images_per_star is the max amount of images it will take from each star
#Returns list of images to be used for training, and the labels in np array of size (samples, # of stars)
def get_images(directory_path, images_per_star):
    paths, y_train = get_image_paths(directory_path, images_per_star)


    pil_images = pil_images_from_paths(paths)
    
    np_images = pil_imgs_to_numpy(pil_images)
    
    np_images, y_train = preprocess_images(np_images, y_train)
    
    return np_images, y_train
    
#Converts pil images to numpy array
#rgb colors are converted from 0 to 1 instead of 0 to 255
def pil_imgs_to_numpy(pil_imgs):
    
    np_images = [(img_to_array(image)/255) for image in pil_imgs]
    
    return np.array(np_images)
    
#From a list of paths, returns a list of pil images
#pil images are resized to contain only the star number of the game image.
def pil_images_from_paths(paths):
    
    pil_images = [crop_and_resize_image(open_image(path)) for path in paths]
    return pil_images


#Parameter is a path to the image, and returns the PIL_image in that path
#Files are not closed when using image.open(), this is the given error:
#[Errno 24] Too many open files
#This is a workaround for that.
def open_image(path):
    pil_img = Image.open(path).convert('RGB')
    copy_image = pil_img.copy()
    pil_img.close()
    return copy_image

#From the main directory path described in the readme
#images_per_star is the max amount of images it will take for each star label
#returns a tuple of (paths, 1-hot represenation np arrays)
def get_image_paths(directory_path, images_per_star):
    
    paths = []
    star_numbers = []
    subdirectory_paths = glob(directory_path +'/*/')
    for star_directory in subdirectory_paths:
        
        dir_name = os.path.basename(os.path.dirname(star_directory))
        
        try:
            star_number = int(dir_name)
        except ValueError:
            print('Folder name with images should be the star number,'
                + ' no images taken from folder named: ' + dir_name)
            continue;
        
        print(star_number)
        #Retrieves all images from subdirectory
        image_paths = get_images_from_star_directory(star_directory, images_per_star)
        
        n_paths = np.size(image_paths, axis = 0)
        
        star_numbers += [star_number] * n_paths
        paths += image_paths
    return np.array(paths), one_hot_representation(star_numbers, 123)

#From a star directory, returns path to images from the subdirectories.
#The algorithm tries to get equal amount #of images from each subdirectory,
#Unless there aren't enough imgs in that subdirectory, 
#if that's the case, then it will take all from that subdirectory and end up taking more from the others    
#Returns paths of images, number of paths returns is equal to image_amount unless there wasn't enough images in star directory.
def get_images_from_star_directory(star_directory_path, image_amount):
    image_directories = glob(star_directory_path +'/*/')
    
    #Contains a list for each subdirectory and each of those lists contains image paths for all imgs in the subdirectory
    directory_image_paths = []
    for img_dir_path in image_directories:
        directory_image_paths.append(get_images_from_dir(img_dir_path))
        
    #Sorts the directories by amount
    dir_image_lengths = [len(image_paths) for image_paths in directory_image_paths]
    dir_arg_sorted = np.argsort(dir_image_lengths)
    dir_amount = len(dir_arg_sorted)
    
    image_paths = []
    
    for sort_index in dir_arg_sorted:
        #Takes images from smallest subdirectory
        dir_image_paths = directory_image_paths[sort_index]
        #Recalculates images_to_get after every subdir pass
        images_to_get = int(image_amount/dir_amount)
        images_it_has = len(dir_image_paths)
        #If subdirectory doesn't have enough images, then takes them all
        if images_to_get >= images_it_has:
            #Takes all images from that dir
            image_paths += dir_image_paths
            image_amount -= images_it_has
        else:
            #Takes a sample
            image_paths += random.sample(dir_image_paths, images_to_get)
            image_amount -= images_to_get
        dir_amount -= 1
    return image_paths


#Returns paths to all the images from the directory given
def get_images_from_dir(directory_path):
    extensions = ['png', 'jpg']
    image_paths = []
    for extension in extensions:
        image_paths += glob(directory_path + '/' + '*.' + extension)
    return image_paths
    
#Crops and resizes pil images from images of the whole game to images of the 
#star number of the game, resizes accordingly
def crop_and_resize_image(pil_img):
    
    pil_img = pil_img.resize((452, 345), Image.ANTIALIAS) #Width,height
    img_width, img_height = pil_img.size[0], pil_img.size[1]
    pil_img = pil_img.crop((380, 0, img_width, img_height-300))
    pil_img = pil_img.resize((67, 40), Image.ANTIALIAS) #Width,height
#   img = img.convert('L') #Converts to black and white
#   img.save(directory_path + '/test/' + 'output image name' + str(star_number) + '.png')
    return pil_img

#Given list of star numbers, returns the one hot representation for them
#Returns 2D numpy matrix of size (samples, size)
def one_hot_representation(star_numbers, size):
    star_numbers = np.array(star_numbers)
    n_samples = np.size(star_numbers, axis = 0)
    one_hot = np.zeros((n_samples, size))
    one_hot[np.arange(n_samples), star_numbers] = 1
    return one_hot
    
    