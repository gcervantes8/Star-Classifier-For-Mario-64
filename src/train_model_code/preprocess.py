# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 16:27:26 2017

@author: Gerardo Cervantes
"""

import numpy as np
import time

#Generates more images to be used for training data
#Generated images should help with robustness
#Generated images will shift the images around and slightly tint the images with different colors
def preprocess_images(images, labels):
    image_gen = mario_image_generator()
    preview_images(image_gen, images, 200) #Saves some generated images for previewing
    start = time.time()
    print('Generating images')
    generated_images, generated_labels = generate_images(image_gen, images, labels)
    print('Time to generate images: ' + str(time.time()-start))
    print('Generated Images size: ' + str(len(generated_images)) )
    
    images = np.concatenate((images, generated_images), axis = 0)
    labels = np.concatenate((labels, generated_labels), axis = 0)
    return images, labels
    
#Will generate images, takes in the generator, and the x_train and y_train
def generate_images(datagen, images, labels):
    sample_size = np.size(images, axis = 0)
    i = 0
    
    #Specify size of generated_images and generated_labels
    generated_images = np.empty( (0,np.size(images,axis = 1), 
                                  np.size(images,axis = 2), np.size(images,axis = 3)), np.float32)
    generated_labels = np.empty( (0,np.size(labels,axis = 1)), np.int16)
    
    batch_size = 512
    for generated_image, generated_label in datagen.flow(images, labels, batch_size = batch_size):
        generated_images = np.concatenate((generated_images, generated_image), axis = 0)
        generated_labels = np.concatenate((generated_labels, generated_label), axis = 0)
        
        #Condition used to stop generation, found empirically
        if i * batch_size > sample_size:
            break  # otherwise the generator would loop indefinitely
        i += 1
    
    return np.array(generated_images), np.array(generated_labels)

#Returns the generator it will use to generate the new images
#This generator will zoom in, shift in width and height, and slighlty change color
def mario_image_generator():
    from keras.preprocessing.image import ImageDataGenerator
    image_gen = ImageDataGenerator(
        rotation_range = 0,
        width_shift_range = 0.05,
        height_shift_range = 0.1,
        channel_shift_range = 25,
        zoom_range = 0.05,
        horizontal_flip = False,
        fill_mode='nearest')    
    return image_gen


#Saves some generated images so we can see how the generated images look like
#Datagen is the generator, images is the numpy array of images
#n_ims_to_preview is the amount of generated images it will save
def preview_images(datagen, images, n_imgs_to_preview):
    
    # the .flow() command below generates batches of randomly transformed images
    # and saves the results to the `preview/` directory
    i = 0
    batch_size = 50
    #, save_to_dir='../preview', save_prefix='item', save_format='jpeg'
    for batch in datagen.flow(images, batch_size=batch_size, save_to_dir='preview', save_prefix='item', save_format='jpeg'):
        i += batch_size
        if i > n_imgs_to_preview:
            break  # otherwise the generator would loop indefinitely