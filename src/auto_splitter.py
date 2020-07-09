"""

@author: Gerardo Cervantes
"""

# Mario 64 (U) NTSC - First star counter appearance is 49.27 seconds into the run

from src.load_images import resize_image
from src.screenshot_taker import ScreenshotTaker
from src.print_progress import print_progress_information
from src.splitter import Splitter
from src.image_detection import is_white_img, is_black_img
from src.image_classifier import classify, _load_nn_model

import time


class AutoSplitter:
    
    # Default model
    model_path = 'models/sm64Model7.hdf5'
    
    splitting_program = 'LiveSplit'
    
    # Keys it will use to split or reset, of type src.hotkeys
    hotkeys = None
    
    # Coordinates where it will take the screenshots, of type src.coordinates
    coordinates = None
    
    # Specify frames of in game time (29.97fps) it will wait before making another prediction
    error_frames = 2
    game_fps = 29.97
    time_per_pred = error_frames * (1/game_fps)
    splitter = Splitter()
    autoreset_toggle = True
    
    _screenshot_taker = ScreenshotTaker()

    # For a split to happen, the prediction has to be higher than the threshold (between 0 and 1)
    split_threshold = 0.7
    # For a reset to happen, the prediction has to be higher than the threshold (between 0 and 1)
    reset_threshold = 0.95

    def __init__(self):
        self.is_running = False
        
    # Stops the classifier
    def stop(self):
        self.is_running = False
    
    # Blocks calling thread until classification process finishes
    # Route is an object from route class in route.py
    # display_handler is an optional arg, its a function to display progress, by default prints to console
    # start_fn is an optional arg, start_fn is a function that is ran after the model started
    # Returns true if successfully finished
    def start(self, route, display_handler=print_progress_information, start_fn=None):
        # If is already running, don't run again
        if self.is_running:
            return
        
        self.is_running = True
        
        x, y, width, height = self.coordinates.get_coordinates()
        split_key, reset_key = self.hotkeys.get_hotkeys()
        
        print('Model path: ', self.model_path)
        print('Coordinates\nx', x, 'y', y, 'width', width, 'height', height)
        print('Split key', split_key, 'Reset key', reset_key)
        
        # Loads neural network model used to make predictions
        model = _load_nn_model(self.model_path)
        
        print('Model loaded')
        split_nums, fadeout_nums = route.get_category_split_info()
#        is_ordered = False
        
        is_black_fadeout, is_white_fadeout = False, False
        
        # star_fn given is parameters is called before starting classifier (tells gui classification started)
        if start_fn != None:
            start_fn()
            
        is_finished = split_nums == [] or fadeout_nums == []
        if not is_finished:
            aim_split = split_nums.pop(0) # Split classifier should look for, if -1 then should look for fadeouts
            aim_fadeout = fadeout_nums.pop(0)
        
        reset_split = aim_split
        pred = -1  # Initial prediction to display
            
        passed_first_class = False # Used for resetting
        print('About to run')
        while self.is_running and not is_finished:
            
            pil_img, run_time = self.take_screenshot_and_resize()
            
            # Default values when doing a rapid split
            split_delay = 0
            sleep_time = 0  # After splitting
            
            is_looking_to_classify = aim_split != -1
            # If not looking for fadeouts
            if is_looking_to_classify:
                pred, pred_prob, pred_time = classify(pil_img, model)
                run_time += pred_time
                if pred == aim_split and pred_prob >= self.split_threshold:
                    aim_split = -1
                if pred != reset_split and pred != aim_split and aim_split != -1 and pred != 121 and pred_prob >= self.split_threshold:
                    passed_first_class = True
                
            # Else is looking for fadeouts
            else:
                pred_prob, pred = -1, -1
                if aim_fadeout > 0:
                    is_black_fadeout, time_black_fadeout = is_black_img(pil_img)
                    run_time += time_black_fadeout
                    if is_black_fadeout:
                        aim_fadeout -= 1
                        split_delay = 0.45
                        sleep_time = 3.1
                    
                elif aim_fadeout < 0:
                    is_white_fadeout, time_white_fadeout = is_white_img(pil_img)
                    run_time += time_white_fadeout
                    if is_white_fadeout:                        
                        aim_fadeout += 1
                        split_delay = 0.15
                        sleep_time = 8
                        
            display_handler(aim_split, aim_fadeout, pred_prob, pred)

            is_split = aim_fadeout == 0 and aim_split == -1
                        
            if is_split:
                self.splitter.split(split_key, split_delay)
                time.sleep(sleep_time)
                run_time += sleep_time
                is_finished = split_nums == [] or fadeout_nums == []
                if not is_finished:
                    # Split classifier should look for, if -1 then should look for fadeouts
                    aim_split = split_nums.pop(0) 
                    aim_fadeout = fadeout_nums.pop(0)
            else:
                if is_white_fadeout or is_black_fadeout:
                    time.sleep(sleep_time)
                    run_time += sleep_time
                    is_black_fadeout, is_white_fadeout = False, False
                elif self.autoreset_toggle and passed_first_class:
                    if not is_looking_to_classify:
                        pred, pred_prob, pred_time = classify(pil_img, model)
                        run_time += pred_time
                    
                    if pred == reset_split and pred_prob >= self.reset_threshold:
                        split_nums, fadeout_nums = route.get_category_split_info()
                        aim_split = split_nums.pop(0) 
                        aim_fadeout = fadeout_nums.pop(0)
                        passed_first_class = False
                        self.splitter.split(reset_key, 0)
                        print('reset')
                        time.sleep(0.03)
            # If finished early, put thread in waiting until self.time_per_pred has elapsed
            self._sleep_between_predictions(run_time)
        self.is_running = False
        return True
        
    def take_screenshot_and_resize(self):
        x, y, width, height = self.coordinates.get_coordinates()
        pil_img, screenshot_time = AutoSplitter._screenshot_taker.screenshot_mss(x, y, width, height)
        start_time = time.time()
        pil_img = resize_image(pil_img)
        resize_time = time.time() - start_time
        return pil_img, screenshot_time + resize_time

    def _sleep_between_predictions(self, time_to_screenshot_and_classify):
        time_to_sleep = self.time_per_pred - time_to_screenshot_and_classify
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
