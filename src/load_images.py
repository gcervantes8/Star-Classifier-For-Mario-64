# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 20:42:17 2017

@author: Gerardo Cervantes
"""


from PIL import Image
from glob import glob
import numpy as np

from random import sample


# directory_paths a list of paths to main directories, images and labels are taken from these directories
# Addtionally it will generate images from preexisting images, this is done to help with robustness of nn
# images_per_star is the max amount of images it will take from each star
# Returns list of images to be used for training, and the labels in np array of size (samples, # of stars)
def get_images(directory_paths, images_per_star, is_full_game_screenshot):
    
    from preprocess import preview_images, no_modifications_generator
    paths, labels = get_image_paths(directory_paths, images_per_star)
    print('Got paths')
    preprocess_images = True
    # List of pil_images
    images = pil_images_from_paths(paths, is_full_game_screenshot, preprocess_images)
    
    print('Got pil images')
    from keras.preprocessing.image import img_to_array
    # Returns images as numpy array of size (n_images, width, height)
    images = [img_to_array(image) for image in images]
    
    print('Converted to arrays')
    images = np.array(images).astype(np.float32)
    print('To numpy')
    # Returns images as numpy array of size (n_images, width, height) with preprocessed images added to it
    preview_images(no_modifications_generator(), images, 50)
    # images, labels = preprocess_images(images, labels)
    # print('Preprocessed images')
    # Turns to numpy array and changes range from 0 to 1
    images = np.array(images).astype(np.float32)/255
    labels = np.array(labels).astype(np.int16)
    print('Images to floats and labels to ints')
    
    return images, labels


# Converts pil images to numpy array
# rgb colors scaled down to floats between 0 to 1 instead of 0 to 255
def pil_imgs_to_numpy(pil_imgs):
    from keras.preprocessing.image import img_to_array
    np_images = [(img_to_array(image)/255) for image in pil_imgs]
    
    return np.array(np_images).astype(np.float32)


# From a list of paths, returns a list of pil images
# pil images are resized to contain only the star number of the game image.
def pil_images_from_paths(paths, is_full_game_screenshot, preprocess_images):
    
    return [crop_and_resize_image(open_image(path), is_full_game_screenshot, preprocess_images) for path in paths]


# Parameter is a path to the image, and returns the PIL_image in that path
# Files are not closed when using image.open(), this is the given error:
# [Errno 24] Too many open files
# This is a workaround for that.
def open_image(path):
    pil_img = Image.open(path).convert('RGB')
    copy_image = pil_img.copy()
    pil_img.close()
    return copy_image


# From the main directory path described in the readme
# images_per_star is the max amount of images it will take for each star label
# returns a tuple of (paths, 1-hot represenation np arrays)
def get_image_paths(directory_paths, images_per_star):
    
    paths = []
    star_numbers = []
    n_classes = 122

    # Uses first main directory path to find how many star directories there are
    subdirectory_paths = glob(directory_paths[0] + '/*/')
    from os import path
    for class_num in range(n_classes):
        
        # star_dir_name = path.basename(path.dirname(star_directory))
        
        # try:
        #    star_number = int(star_dir_name)
        # except ValueError:
        #    print('Folder name with images should be the star number,'
        #        + ' no images taken from folder named: ' + star_dir_name)
        #    continue
        
        print(class_num)
        star_directories = [path.join(main_paths, str(class_num)) for main_paths in directory_paths]
            
        
        # Retrieves all images from subdirectory
        image_paths = get_images_from_star_directory(star_directories, images_per_star)
        
        n_paths = np.size(image_paths, axis = 0)
        
        star_numbers += [class_num] * n_paths
        paths += image_paths
    return np.array(paths), one_hot_representation(star_numbers, n_classes)


# From a star directory, returns path to images from the subdirectories
# The algorithm tries to get equal amount #of images from each subdirectory,
# Unless there aren't enough imgs in that subdirectory,
# if that's the case, then it will take all from that subdirectory and end up taking more from the others
# Returns paths of images, number of paths returns is equal to image_amount unless not enough images in star directory
def get_images_from_star_directory(star_directory_paths, image_amount):
    image_directories = []
    
    for star_path in star_directory_paths:
        img_dir = glob(star_path + '/*/')
        image_directories = image_directories + img_dir
    
    # Contains list for each subdirectory and each of those lists contains image paths for all imgs in the subdirectory
    directory_image_paths = []
    for img_dir_path in image_directories:
        directory_image_paths.append(get_images_from_dir(img_dir_path, False))
        
    # Sorts the directories by amount
    dir_image_lengths = [len(image_paths) for image_paths in directory_image_paths]
    dir_arg_sorted = np.argsort(dir_image_lengths)
    dir_amount = len(dir_arg_sorted)
    
    image_paths = []
    
    for sort_index in dir_arg_sorted:
        # Takes images from smallest subdirectory
        dir_image_paths = directory_image_paths[sort_index]
        # Recalculates images_to_get after every subdir pass
        images_to_get = int(image_amount/dir_amount)
        images_it_has = len(dir_image_paths)
        # If subdirectory doesn't have enough images, then takes them all
        if images_to_get >= images_it_has:
            # Takes all images from that dir
            image_paths += dir_image_paths
            image_amount -= images_it_has
        else:
            # Takes a sample
            image_paths += sample(dir_image_paths, images_to_get)
            image_amount -= images_to_get
        dir_amount -= 1
    return image_paths


# Returns paths to all the images from the directory given
def get_images_from_dir(directory_path, recursive):
    extensions = ['png', 'jpg']
    image_paths = []
    for extension in extensions:
        if recursive:
            image_paths += glob(directory_path + '/**/*.' + extension, recursive = recursive)
        else:
            image_paths += glob(directory_path + '/' + '*.' + extension, recursive = recursive)
    return image_paths


# Crops and re-sizes pil images from images of the whole game to images of the
# star number of the game, re-sizes accordingly
# pre-process should be True if you want varying x and y coordinates and sizes (Done to make model robust)
def crop_and_resize_image(pil_img, is_full_game_screenshot, preprocess):
    from random import randint

    if is_full_game_screenshot: 
        pil_img = pil_img.resize((452, 345), Image.ANTIALIAS)  # Width,height
        img_width = pil_img.size[0]
        
        x, y = 380, 1
        size = img_width - 2 - x
        w, h = size + x, round(size/1.675) + y
        
        size_modifier = 0
        if preprocess:
            size_modifier = randint(-1, 1)  # If positive makes screen grab bigger, negative makes it smaller
            x_modifier = randint(-1, 1)
            y_modifier = randint(0, 1)
            x += x_modifier
            w -= x_modifier
            y += y_modifier
            h -= y_modifier
            
        w = min(img_width, w)  # Should not be outside of the image
        y = max(y, 0)  # Y should be inside the image (Shouldn't be negative)
        pil_img = pil_img.crop((x-size_modifier, y-size_modifier, w+size_modifier, h+size_modifier))
    pil_img = pil_img.resize((67, 40), Image.ANTIALIAS)  # Width,height
    
#    Debugging
#   img.save(directory_path + '/test/' + 'output image name' + str(star_number) + '.png')
    return pil_img


def resize_image(pil_img):
    pil_img = pil_img.resize((67, 40), Image.ANTIALIAS)  # Width,height
    return pil_img


# Given list of star numbers, returns the one hot representation for them
# Returns 2D numpy matrix of size (samples, size)
def one_hot_representation(star_numbers, size):
    star_numbers = np.array(star_numbers)
    n_samples = np.size(star_numbers, axis = 0)
    one_hot = np.zeros((n_samples, size))
    one_hot[np.arange(n_samples), star_numbers] = 1
    return one_hot


def crop_images_from_dir(images_directory, output_directory):
    image_paths = get_images_from_dir(images_directory, True)
    for i, path in enumerate(image_paths):
        pil_img = open_image(path)
        img_width, img_height = pil_img.size[0], pil_img.size[1]
#    pil_images = [img.crop((10, 10, img_width-9, img_height-11)) for img in pil_images]
        pil_img = pil_img.crop((296, 0, img_width, img_height))
        if output_directory != None:
            pil_img.save(output_directory + '/' + str(i) + '.png')
        else:
            pil_img.save(path)


if __name__ == "__main__":
    # Module in src folder to load images
    # from sys import path
    # path.insert(0, 'train_model_code')
    # # For debugging to be able to look at images produced
    # images, y = get_images(r'E:\MarioStarClassifier\train_images', 2, True)
    
    import os
    # images_directory = 'E:/MarioStarClassifier/caivs15818'
    images_directory = 'D:/mario_data/lozplyr-120star-3-58-46'
#    output_directory = os.path.join(images_directory, 'cropped')
    
    # To preview
#    image_paths = get_images_from_dir(images_directory, False)
#    pil_images = [open_image(path) for path in image_paths]

    crop_images_from_dir(images_directory, None)
