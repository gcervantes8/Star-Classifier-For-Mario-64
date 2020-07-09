# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:38:09 2019

@author: Gerardo Cervantes
"""

from src.load_images import pil_imgs_to_numpy

import numpy as np
import time


# star_image is of type PIL
# Returns 2-tuple (is_whitefadeout, pred_time) 1st item is bool, 2nd item is time in seconds
def is_white_img(star_image):
    start_time = time.time()
    consider_nonwhite = 0.80 
    num_nonwhite_pixels, num_pixels = _pixels_meet_threshold(star_image, consider_nonwhite)
    is_whitefadeout = num_nonwhite_pixels < num_pixels * 0.08  # If there's under 8% of pixels aren't white
    pred_time = time.time() - start_time
    return is_whitefadeout, pred_time


# star_image is of type PIL
# Returns 2-tuple (is_whitefadeout, pred_time) 1st item is bool, 2nd item is time in seconds
def is_black_img(star_image):
    start_time = time.time()
    consider_gray = 0.08  # If value is lower than this consider it black/fadeout pixel
    img_np = pil_imgs_to_numpy([star_image])[0] 
    
    red = img_np[:, :, 0]
    green = img_np[:, :, 1]
    blue = img_np[:, :, 2]
    threshold_dist = 0.035
    has_close_color_dist = _are_color_dist_close(red, green, blue, threshold_dist)

    num_black_pixels, num_pixels = _pixels_meet_threshold(star_image, consider_gray)

    # If more than 92% of pixels in image are black, then say image is a fadeout image
    is_img_blackish = num_black_pixels > num_pixels * 0.98
    
    is_blackfadeout = is_img_blackish and has_close_color_dist
    pred_time = time.time() - start_time
    return is_blackfadeout, pred_time
    

def _are_color_dist_close(red, green, blue, threshold_dist):
    outlier_ratio = 0.03  # If more outliers than outlier ratio, returns false
    # Count num pixels above threshold
    rg_count = np.sum(abs(red-green) > threshold_dist)
    rb_count = np.sum(abs(red-blue) > threshold_dist)
    gb_count = np.sum(abs(green-blue) > threshold_dist)
    max_count = max(rg_count, rb_count, gb_count)
    if max_count > (red.size * outlier_ratio):  # If more than 3% of pixels are outliers
        return False
    return True


# Returns true if the given PIL image is black, has to meet a specific threshold
def _pixels_meet_threshold(image, color_threshold):
    
    # grayscale_star_image = image.convert('LA') #Converts to grayscale image
    img_np = pil_imgs_to_numpy([image])
    flattened_img = img_np.flatten()
    
    num_threshold_pixels = np.sum(flattened_img < color_threshold)
    
    return num_threshold_pixels, len(flattened_img)

