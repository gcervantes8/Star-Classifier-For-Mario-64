"""

@author: Gerardo Cervantes
"""
#First star counter appearance is 49.27 seconds into the run (English version of Mario 64 NSTC)

import numpy as np


from src.load_images import resize_image, pil_imgs_to_numpy

import time
from threading import Thread
from win32com.client import Dispatch
from pythoncom import CoInitialize

from src.screenshot_taker import ScreenshotTaker
from src.print_progress import print_progress_information

class StarClassifier():
    
    #Default model
    model_path = 'models/sm64Model4.hdf5'
    
    splitting_program = 'LiveSplit'
    
    hotkeys = None
    coordinates = None
    route_name = ''
    
    #Specify how many frames of in game time (29.97fps) it should wait before making another prediction
    error_frames = 2
    game_fps = 29.97
    time_per_pred = error_frames * (1/game_fps)
    
    #Module to take screenshots
    screenshot_taker = ScreenshotTaker()
    
    #Threshold are between 0 and 1, if higher than threshold then does the split or reset
    split_threshold = 0.4
    reset_threshold = 0.8
    
    
    def __init__(self):
        self.is_running = False
        
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
        
    def set_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys
        
    #Loads the neural network model, including the configuration settings and the weights
    def _load_nn_model(self, path):
        
        #Clears any previous sessions, bug in keras caused by threading/wrong graph
        from keras import backend as K
        K.clear_session()
                
        #Keras Library to load neural networks (importing from Keras or Tensorflow is slow)
        from keras.models import load_model
        model = load_model(path)
        return model
    
    #Returns true if the prediction classified was a black or white image.
    def is_white_black_img(self, prediction):
        return prediction == 121 or prediction == 122
    
    #Should be called after star number just changed and wants to split at fadeout
    #Split key is the key that will be given to livesplit to split, should be a str
    #Split_wait_time is float of how long it should wait until it should split
    def split(self, split_key, split_wait_time):
        CoInitialize()
    
        if split_wait_time > 0:
            time.sleep(split_wait_time)
        print('split')
        wsh = Dispatch("WScript.Shell")
        wsh.AppActivate('LiveSplit') # select livesplit application
        wsh.SendKeys(split_key)
    
    def stop(self):
        self.is_running = False
        
    #Returns True if we think another star was gotten based on the models output, false otherwise
    def got_next_star(self, current_star_number, prediction, pred_prob):
        is_high_probabilty = pred_prob >= self.split_threshold
        is_next_star = prediction == current_star_number + 1
        
        return is_high_probabilty and is_next_star
    
    
    #Split and reset keys should be a string from ones specified in https://msdn.microsoft.com/en-us/library/8c6yea83(v=vs.84).aspx
    #x,y, width, and height contain coordinates to screenshot for pil, should be set to cover the game screen
    #Only handles 1 thread doing classification at a time.
    #start_fn called after the model has started making preditions
    def start(self, route, display_handler = print_progress_information, start_fn = None):
        
        self.is_running = True
        
        x, y, width, height = self.coordinates.get_coordinates()
        print('Model path: ', self.model_path)
        print('Coordinates\nx', x , 'y', y, 'width', width, 'height', height)
        split_key, reset_key = self.hotkeys.get_hotkeys()
        print('Split key', split_key, 'Reset key', reset_key)
        
        #Loads neural network model used to make predictions
        model = self._load_nn_model(self.model_path)
        
        starting_star_num, immediate_splits, fadeout_splits, fadeout_amounts = route.get_category_splitting_information()
        
        #Star we are in, start at -1 if you would like for it to split when it finds the number 0
        star_num = starting_star_num - 1
        
        #Has the amount of fadeouts it needs to see for it to split, updated everytime a new star is collected
        black_fadeouts, white_fadeouts = [], []
        
        black_fadeouts_found, white_fadeouts_found = 0, 0
        
        time_without_star_count = 0 #Keeps track of the amount of time it hasn't seen the star counter in seconds (used for reseting)
        estimate_intro_length_in_seconds = 38 #If hasn't seen a star counter in this amount of time, it's likely game was reset
        
        if start_fn != None:
            start_fn()
        
        while self.is_running:
            
            pil_img, screenshot_time = self.take_screenshot_and_resize()
            
            
            prediction, prediction_prob, predict_time = self.predict_star_number_from_screenshot(pil_img, model)
            
            time_to_screenshot_and_pred = screenshot_time + predict_time
            
            game_was_reset = prediction == starting_star_num and prediction_prob > self.reset_threshold and time_without_star_count > estimate_intro_length_in_seconds
            
            if game_was_reset:
                star_num = starting_star_num - 1
                time_without_star_count = 0
                self.split_in_new_thread(reset_key, 0)
                continue
               
            if black_fadeouts != []:
                is_black_fadeout, time_black_fadeout = self.img_in_blackfadeout(pil_img)
                black_fadeouts_found += is_black_fadeout
                time_to_screenshot_and_pred += time_black_fadeout
                
                if is_black_fadeout:
                    #Handles black fadeouts
                    self.handle_fadeouts(black_fadeouts_found, black_fadeouts, 0.45, 3.1)
                    continue
            
            if white_fadeouts != []:
                is_white_fadeout, time_white_fadeout = self.img_in_whitefadeout(pil_img)
                white_fadeouts_found += is_white_fadeout
                time_to_screenshot_and_pred += time_white_fadeout
                if is_white_fadeout:
                    #Handles white fadeouts
                    self.handle_fadeouts(black_fadeouts_found, black_fadeouts, 0.15, 8)
                    continue

            #Returns immediate_split, fade_out_split, or don't split
            is_next_star = self.got_next_star(star_num, prediction, prediction_prob)
            if is_next_star:
                #Moves onto next star because they grabbed another star
                star_num += 1
                
                #Immediate split
                if star_num in immediate_splits:
                    self.split_in_new_thread(split_key, 0) 
                
                time_without_star_count = 0
                
                #Update fadout amounts needed for this new star
                black_fadeouts_found, white_fadeouts_found = 0, 0
                black_fadeouts, white_fadeouts = self.get_fadeouts(star_num, fadeout_splits, fadeout_amounts)

            not_showing_star_count = (prediction == 121 or prediction == 122) 
            
            #If screenshot didn't have a star counter
            if not_showing_star_count:
                time_without_star_count += max(time_to_screenshot_and_pred, self.time_per_pred)
            
            
            display_handler(star_num, prediction, prediction_prob, time_to_screenshot_and_pred)
                
            #If finished early, put thread in waiting until reaches time_between_predictions
            self.sleep_between_predictions(time_to_screenshot_and_pred)
                
    
    #If has same amount of fadeouts found as fadeout amount needed, then splits
    #Sleeps for split_time amount of time
    def handle_fadeouts(self, fadeouts_found, fadeout_amounts, split_time, sleep_time):
        split_key, _ = self.hotkeys.get_hotkeys()
        
        if fadeouts_found in fadeout_amounts:
            self.split_in_new_thread(split_key, split_time)
        time.sleep(sleep_time)
        
    
    def get_fadeouts(self, current_star_num, fadeout_splits, fadeout_amounts):
        indices = [i for i, x in enumerate(fadeout_splits) if x == current_star_num]
        fadeouts = [fadeout_amounts[index] for index in indices]
        black_fadeouts = [fadeout for fadeout in fadeouts if fadeout > 0]
        white_fadeouts = [abs(fadeout) for fadeout in fadeouts if fadeout < 0]
        return black_fadeouts, white_fadeouts
    
    def take_screenshot_and_resize(self):
        x, y, width, height = self.coordinates.get_coordinates()
        pil_img, screenshot_time = self.screenshot_taker.screenshot_mss(x, y, width, height)
        start_time = time.time()
        pil_img = resize_image(pil_img)
        resize_time = time.time() - start_time
        return pil_img, screenshot_time + resize_time
    
    def sleep_between_predictions(self, time_to_screenshot_and_classify):
        time_to_sleep = self.time_per_pred - time_to_screenshot_and_classify
        if time_to_sleep > 0:
            time.sleep(self.time_per_pred - time_to_screenshot_and_classify)
            
    def split_in_new_thread(self, split_key, delay):
        thread = Thread(target = self.split, args = (split_key, delay))
        thread.start()


    def are_color_dist_close(self, red, green, blue, threshold_dist):
        rg_dist = np.amax(abs(red-green))
        rb_dist = np.amax(abs(red-blue))
        gb_dist = np.amax(abs(green-blue))
        max_dist = max(rg_dist, rb_dist, gb_dist)
        
        if max_dist > threshold_dist:
            return False
        return True
    
    #Returns true if the given PIL image is a black fadeout (fadeout is when game does fadeout animation after collecting a star)
    def img_pixels_meet_threshold(self, star_image, color_threshold):
        
        #grayscale_star_image = star_image.convert('LA') #Converts to grayscale image
        img_np = pil_imgs_to_numpy([star_image])
        flattened_img = img_np.flatten()
        
        num_threshold_pixels = np.sum(flattened_img < color_threshold)
        
        return num_threshold_pixels, len(flattened_img)
    
    def img_in_whitefadeout(self, star_image):
        start_time = time.time()
        consider_nonwhite = 0.80 
        num_nonwhite_pixels, num_pixels = self.img_pixels_meet_threshold(star_image, consider_nonwhite)
        is_whitefadeout = num_nonwhite_pixels < num_pixels * 0.08 #If there's under 8% of pixels aren't white
        pred_time = time.time() - start_time
        return is_whitefadeout, pred_time
    
    def img_in_blackfadeout(self, star_image):
        start_time = time.time()
        consider_gray = 0.08 #If value is lower than this consider it black/fadeout pixel (after converting img into 0 to 1)
        img_np = pil_imgs_to_numpy([star_image])[0] 
        
        red = img_np[:,:,0]
        green = img_np[:,:,1]
        blue = img_np[:,:,2]
        threshold_dist = 0.035
        has_large_color_dist = self.are_color_dist_close(red, green, blue, threshold_dist)
        
        
        num_black_pixels, num_pixels = self.img_pixels_meet_threshold(star_image, consider_gray)
        is_img_blackish = num_black_pixels > num_pixels * 0.98 #If more than 92% of pixels in image are black, then say image is a fadeout image
        
#        print('Is a black image:', str(is_img_blackish))
#        print('Is there distance between colors? ', str(has_large_color_dist))
        
        is_blackfadeout = is_img_blackish and not has_large_color_dist
        pred_time = time.time() - start_time
        return is_blackfadeout, pred_time
        
    #Model is the successfully keras loaded model that will make the predictions
    #star_image is the PIL image that has the star counter
    #Returns tuple, (What star was predicted, the probability of prediction, the time it took)
    def predict_star_number_from_screenshot(self, star_image, model):
        start_time = time.time()
        
        img_np = pil_imgs_to_numpy([star_image])
        nn_output = model.predict(img_np)
        prediction = np.argmax(nn_output)
        prediction_probability = np.max(nn_output)
        
        star_prediction_time = time.time() - start_time
        return prediction, prediction_probability, star_prediction_time