"""

@author: Gerardo Cervantes
"""
#First star counter appearance is 49.27 seconds into the run (English version of Mario 64 NSTC)

import numpy as np


from load_images import resize_image, pil_imgs_to_numpy

import time
from threading import Thread
from win32com.client import Dispatch
from pythoncom import CoInitialize

from screenshot_taker import ScreenshotTaker
from print_progress import print_progress_information

class StarClassifier():
    
    #Default model
    model_path = 'models/sm64Model3.hdf5'
    
    splitting_program = 'LiveSplit'
    
    hotkeys = None
    coordinates = None
    route_name = ''
    
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
    def check_model_output(self, current_star_number, prediction, prediction_prob, probability_threshold):
        is_high_probabilty = prediction_prob >= probability_threshold
        is_next_star = prediction == current_star_number + 1
        
        return is_high_probabilty and is_next_star
    
    
    #Split and reset keys should be a string from ones specified in https://msdn.microsoft.com/en-us/library/8c6yea83(v=vs.84).aspx
    #x,y, width, and height contain coordinates to screenshot for pil, should be set to cover the game screen
    #Only handles 1 thread doing classification at a time.
    #start_fn called after the model has started making preditions
    def start(self, route, display_handler = print_progress_information, start_fn = None):
        
        self.is_running = True
        
        x, y, width, height = self.coordinates.get_coordinates()
        print('Model')
        print(self.model_path)
        print('Coordinates')
        print('x' , x , 'y', y, 'width', width, 'height', height)
        split_key, _ = self.hotkeys.get_hotkeys()
        print('Split key')
        print(split_key)
        
        #Loads neural network model used to make predictions
        model = self._load_nn_model(self.model_path)
        
        starting_star_number, _, _, _ = route.get_category_splitting_information()
        
        #Star we are in, start at -1 if you would like for it to split when it finds the number 0
        current_star_number = starting_star_number - 1
        
        #The prediction probability needs to be higher than this threshold so that we can be certain of this classification
        probability_threshold = 0.4
        is_fadeout_mode = True
        #Counter is amount of times it has screenshotted and predicted
        n_predictions = 0
        
        screenshot_maker = ScreenshotTaker()
        
        #Specify how many frames of in game time (29.97fps) it should wait before making another prediction
        error_frames = 2
        time_between_predictions = error_frames * (1/29.97) #Convert 29.97 fps to amount of seconds for 1 frame
        #Amount of time it should screenshot and predict before progress is printed/displayed
        iterations_before_display = 20
        
        #Keeps track of how much time has passed since last output display
        display_prediction_time = 0
        
        star_black_fadeouts, star_white_fadeouts = [], []
        star_black_fadeouts_found, star_white_fadeouts_found = 0, 0
        
        if start_fn != None:
            start_fn()
        
        while self.is_running:
            n_predictions += 1
            
            
            pil_img, screenshot_time = screenshot_maker.screenshot_mss(x, y, width, height)
            pil_img = resize_image(pil_img)
            
            is_fadeout_mode = star_black_fadeouts != [] or star_white_fadeouts != []
            if is_fadeout_mode:
                
                if star_black_fadeouts != []:
                    is_in_black_fadeout, star_predict_time = self.img_is_in_blackfadeout(pil_img)
                    if is_in_black_fadeout:
                        print('Found black fadeout')
                        star_black_fadeouts_found += 1
                        if star_black_fadeouts_found in star_black_fadeouts:
                            self.split_in_new_thread(split_key, 0.45)
                            star_black_fadeouts.remove(star_black_fadeouts_found)
                        #Stop until fadeout is finished
                        time.sleep(3.1)
                        
                if star_white_fadeouts != []:
                    is_in_white_fadeout, star_predict_time = self.img_is_in_whitefadeout(pil_img)
                    if is_in_white_fadeout:
                        star_white_fadeouts_found += 1
                        if star_white_fadeouts_found in star_white_fadeouts:
                            self.split_in_new_thread(split_key, 0.15)
                            star_white_fadeouts.remove(star_white_fadeouts_found)
                        #Stop until fadeout is finished
                        time.sleep(8)
                    
            else:
                prediction, prediction_prob, star_predict_time = self.predict_star_number_from_screenshot(pil_img, model)
                #Returns immediate_split, fade_out_split, or don't split
                grabbed_next_star = self.check_model_output(current_star_number, prediction, prediction_prob, probability_threshold)
                if grabbed_next_star:
                    
                    #Moves onto next star because they grabbed another star
                    current_star_number += 1
                    is_immediate_split, is_fadeout_split, star_black_fadeouts, star_white_fadeouts = self.decide_split(current_star_number, route)
                    star_black_fadeouts_found, star_white_fadeouts_found = 0, 0
                    if is_immediate_split:
                        self.split_in_new_thread(split_key, 0)
                
                display_prediction_time += screenshot_time
                display_prediction_time += star_predict_time
                display_handler(current_star_number, prediction, prediction_prob, display_prediction_time/iterations_before_display)
                
            #If finished early, put thread in waiting until reaches time_between_predictions
            if star_predict_time < time_between_predictions:
                if is_fadeout_mode: #Waits less if is in fadeout mode
                    time.sleep( (time_between_predictions/2)-star_predict_time)
                else:
                    time.sleep(time_between_predictions-star_predict_time)
            display_prediction_time = 0
    
    
    #Decides it should split based on the route
    def decide_split(self, current_star_number, route):
        _, immediate_splits, fadeout_splits, fadeout_amounts = route.get_category_splitting_information()
        is_immediate_split = current_star_number in immediate_splits
        is_fadeout_split = current_star_number in fadeout_splits
        if is_fadeout_split:
#            index = fadeout_splits.index(current_star_number)
            indices = [i for i, x in enumerate(fadeout_splits) if x == current_star_number]
            fadeouts = [fadeout_amounts[index] for index in indices]
        else:
            fadeouts = []
        black_fadeouts = [fadeout for fadeout in fadeouts if fadeout > 0]
        white_fadeouts = [abs(fadeout) for fadeout in fadeouts if fadeout < 0]
        return is_immediate_split, is_fadeout_split, black_fadeouts, white_fadeouts
                
    def split_in_new_thread(self, split_key, delay):
        thread = Thread(target = self.split, args = (split_key, delay))
        thread.start()
        
    #Returns true if the given PIL image is a black fadeout (fadeout is when game does fadeout animation after collecting a star)
    def img_is_in_fadeout(self, star_image):
        start_time = time.time()
        #grayscale_star_image = star_image.convert('LA') #Converts to grayscale image
        img_np = pil_imgs_to_numpy([star_image])
        flattened_img = img_np.flatten()
        consider_gray = 0.27 #If value is lower than 0.27 consider it black/fadeout pixel (after converting img into 0 to 1)
        
        num_black_pixels = np.sum(flattened_img < consider_gray)
        is_in_fadeout = num_black_pixels > len(flattened_img) * 0.92 #If more than 92% of pixels in image are black, then say image is a fadeout image
        star_prediction_time = time.time() - start_time
        return is_in_fadeout, star_prediction_time
    
    #Returns true if the given PIL image is a black fadeout (fadeout is when game does fadeout animation after collecting a star)
    def img_pixels_meet_threshold(self, star_image, color_threshold):
        
        #grayscale_star_image = star_image.convert('LA') #Converts to grayscale image
        img_np = pil_imgs_to_numpy([star_image])
        flattened_img = img_np.flatten()
        
        num_threshold_pixels = np.sum(flattened_img < color_threshold)
        
        return num_threshold_pixels, len(flattened_img)
    
    def img_is_in_whitefadeout(self, star_image):
        start_time = time.time()
        consider_nonwhite = 0.80 
        num_nonwhite_pixels, num_pixels = self.img_pixels_meet_threshold(star_image, consider_nonwhite)
        is_in_whitefadeout = num_nonwhite_pixels < num_pixels * 0.08 #If there's under 8% of pixels aren't white
        star_prediction_time = time.time() - start_time
        return is_in_whitefadeout, star_prediction_time
    
    def img_is_in_blackfadeout(self, star_image):
        start_time = time.time()
        consider_gray = 0.07 #If value is lower than 0.27 consider it black/fadeout pixel (after converting img into 0 to 1)
        num_black_pixels, num_pixels = self.img_pixels_meet_threshold(star_image, consider_gray)
        is_in_blackfadeout = num_black_pixels > num_pixels * 0.98 #If more than 92% of pixels in image are black, then say image is a fadeout image
        
        star_prediction_time = time.time() - start_time
        return is_in_blackfadeout, star_prediction_time
        
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
    
