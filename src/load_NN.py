"""

@author: Gerardo Cervantes
"""
#Star grab to fade out is ~4.07 seconds - Will change depending on lag, 4.07 is assumed
#First star counter appearance is 50.12 seconds into the run (English version of Mario 64 NSTC)

import numpy as np
from PIL import Image, ImageGrab
#Keras Library to load neural networks
from keras.models import load_model

from load_images import crop_and_resize_image, pil_imgs_to_numpy

import time
from threading import Thread
import win32com.client as comclt
import pythoncom


import win32gui
import win32ui
import win32con

import mss
import mss.tools

#Loads the neural network model, including the configuration settings and the weights
def loadNeuralNetworkModel(fileDir):
	model = load_model(fileDir)
	return model

#Returns true if the prediction classified was a black or white image.
def is_white_black_img(prediction):
    return prediction == 121 or prediction == 122

#Should be called after star number just changed and wants to split at fadeout
#Split key is the key that will be given to livesplit to split, should be a str
#Split_wait_time is float of how long it should wait until it should split
def split(split_key, split_wait_time):
    pythoncom.CoInitialize()

    if split_wait_time > 0:
        time.sleep(split_wait_time)
    print('split')
    wsh = comclt.Dispatch("WScript.Shell")
    wsh.AppActivate('LiveSplit') # select livesplit application
    wsh.SendKeys(split_key)
    
#Has problem finding Amarec program, finds the windows with 'AmaRecTV', but a black screenshot
#Is supposed to be able to create fast screenshots
def fast_screenshot(window_name, save_name, w, h):
    hwnd = win32gui.FindWindow(None, window_name)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, save_name)
#     Free ResourcesS
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    
#Screenshots using PIL library
def screenshot_pil(x, y, width, height):
    full_img = ImageGrab.grab(bbox=(x, y, x+width, y+height))
    return full_img
    
#Screenshots using mss library. (faster than screnshotting using PIL)
#sct is mss instance, should be created, only need to be created once and can be reused
#Top and left are coordinates of the top-left of the window where you want the screenshot
def fast_screenshot_mss(sct, top, left, width, height):
    
    # The screen part to capture
    monitor = {'top': top, 'left': left, 'width': width, 'height': height}

    # Grab the data
    sct_img = sct.grab(monitor)

    # Create the Image, converts to PIL, probably not needed for speed, but simplifies crop and resize
    img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    return img
        
#Split and reset keys should be a string from ones specified in https://msdn.microsoft.com/en-us/library/8c6yea83(v=vs.84).aspx
#x,y, width, and height contain coordinates to screenshot for pil, should be set to cover the game screen
def run_splitter(model_path, starting_star_number, split_key, reset_key, fadeout_splits, immediate_splits, x, y, width, height):

	#Loads neural network model used to make predictions
    model = loadNeuralNetworkModel(model_path)

    #Star we are in, start at -1 if you would like for it to split when it finds the number 0
    current_star_number = starting_star_number - 1
    
    #The prediction probability needs to be higher than this threshold so that we can be certain of this classification
    probability_threshold = 0.85
    
    #Constant, time from star grab to fadeout
    fadeout_time = 4.07
       
    #Counter is amount of times it has screenshotted and predicted
    n_predictions = 0
    
    #Used for screenshotting, created once then used multiple times to screenshot
    sct = mss.mss()
    
    #Specify how many frames of in game time (29.97fps) it should wait before making another prediction
    error_frames = 2
    time_between_predictions = error_frames * (29.97/1000) #Convert 30 fps to frames per millisecond, us that to give us information when to make next prediction
    
    
    #Amount of time it should screenshot and predict before progress is printed/displayed
    iterations_before_display = 20
    
    #Keeps track of how much time has passed since last output display
    display_prediction_time = 0
    while True: #current_star_number < np.max(np.array(fadeout_splits))
        n_predictions += 1
        
        prediction, prediction_prob, star_predict_time = predict_star_number_from_screenshot(model, sct, y, x, width, height)

    
        
        display_prediction_time += star_predict_time
        
        #If prediction probability is low, then ignore the prediction.
        if prediction_prob >= probability_threshold:
            
            #If we predicted that it would be the next star, and is high probability prediction, then a star was likely gotten 
            if prediction == current_star_number + 1:
            
    			
                #Moves onto next star because they grabbed another star
                current_star_number += 1
                
                is_immediate_split = current_star_number in immediate_splits
                is_fade_out_split = current_star_number in fadeout_splits
                
                #SPLIT if this is a star we are supposed to split in
                if is_immediate_split or is_fade_out_split:
                    
                    #Ternary operator, 0 if is an immediate split otherwise, fadeout_time minus time it took to predict
                    time_until_split = 0 if is_immediate_split else (fadeout_time - star_predict_time)
        				#Starts thread to split
                    thread = Thread(target = split, args = (split_key, time_until_split))
                    thread.start()
        
            #If predicted star 0, and we weren't in star 0 before then resets timer and then splits(Comment assumes starting star number is 0)
            elif prediction == starting_star_number and current_star_number != starting_star_number:
                current_star_number = 0
                thread = Thread(target = split, args = (reset_key, 0))
                thread.start()
                thread = Thread(target = split, args = (split_key, 0.1))
                thread.start()
                
            else:
                #If entered here, might have misclassified
                pass

        #If finished early, put thread in waiting until reaches time_between_predictions
        if star_predict_time < time_between_predictions:
            time.sleep(time_between_predictions-star_predict_time)
            
        #Prints progress if reached iterations_before_display
        if  (n_predictions % iterations_before_display) == 0:
            time_per_star = display_prediction_time/iterations_before_display
            print('#' + str(n_predictions) + ' prediction: ' + str(prediction) + ' probability: ' + 
                  "{0:.2f}".format(prediction_prob) + ' time: ' + "{0:.3f}".format(time_per_star))
            display_prediction_time = 0
                
#Model is the successfully keras loaded model that will make the predictions
#sct is the mss instance that will make the screenshot.  Should be None if you want to screenshot using PIL (slower)
#y and x are the coordinates in monitor where it will screenshot
#width and height are how big the screenshot should be
#Returns tuple, (What star was predicted, the probability of prediction, the time it took)
def predict_star_number_from_screenshot(model, sct, y, x, width, height):
    start_time = time.time()

    full_img = fast_screenshot_mss(sct, y, x, width, height)
    if sct == None:
        full_img = ImageGrab.grab(bbox=(x, y, x+width, y+height)) #Alternative
        
    star_image = crop_and_resize_image(full_img)
    img_np = pil_imgs_to_numpy([star_image])
    
    nn_output = model.predict(img_np)
    prediction = np.argmax(nn_output)
    prediction_probability = np.max(nn_output)
    star_prediction_time = time.time() - start_time
    return prediction, prediction_probability, star_prediction_time
