"""

@author: Gerardo Cervantes
"""
#Star grab to fade out is ~4.07 seconds
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

def is_white_black_img(prediction):
    return prediction == 121 or prediction == 122

#Should be called after star number just changed and wants to split at fadeout
def split(split_key, split_wait_time):
    pythoncom.CoInitialize()

    time.sleep(split_wait_time)
    print('split')
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.AppActivate("LiveSplit") # select livesplit application
    wsh.SendKeys(split_key)
    
#Has problem finding amarec, finds the windows with 'AmaRecTV', but a black screenshot
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
def screenshot_pil(x, y, w, h):
    full_img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
    return full_img
    
#Screenshots using mss
def fast_screenshot_mss(sct, top, left, width, height):
    
    # The screen part to capture
    monitor = {'top': top, 'left': left, 'width': width, 'height': height}

    # Grab the data
    sct_img = sct.grab(monitor)

    # Create the Image, converts to PIL, probably not needed for speed, but simplifies crop and resize
    img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    return img
        

if __name__ == "__main__":
    model = loadNeuralNetworkModel('High_acc_model_205_imgs_30epochs')
    
    #Sets coordinates to screenshot for pil, should be set to cover the game screen
    x, y, w, h = 61, 82, 615, 449
    
    #Star we are in, always start at 0, start af -1 if you would like for it to split
    #after the first instance of star number appearing
    current_star_number = -1
    
    #Amount of predictions of the next star, is reset when star number is changed
    consecutive_frames = 0
    
    #Keeps track of run time it took until it found enough predictions to move onto next star
    prediction_run_time = 0
    
    #Threshold of how many times it should read the game to be in the next star
    #before it splits
    next_star_threshold = 2
    
    #Constant
    fadeout_time = 4.07
    
    
    
    #Star numbers where it will split
    splits = [0, 10,13,17,19,24,30,34,39,42,48,52,58,62,69]
    #Stars where it should split immediately after grabbing the star
    non_fadeout_splits = [0, 13, 69]
    #split key used to split
    split_key = '{PGUP}'
       
    #Counter is amount of times it has screenshotted
    i = 0
    
    #Used for screenshotting, created once then used multiple times to screenshot
    sct = mss.mss()
    
    while current_star_number < np.max(np.array(splits)):
    
        start_time = time.time()
        
    #    full_img = ImageGrab.grab(bbox=(x, y, x+w, y+h)) #Alternative
        full_img = fast_screenshot_mss(sct, y, x, w, h)
        star_image = crop_and_resize_image(full_img)
        img_np = pil_imgs_to_numpy([star_image])
        
        nn_output = model.predict(img_np)
        prediction = np.argmax(nn_output)
        prediction_probability = np.max(nn_output)
    
        i += 1
        print(str(i) + ' prediction: ' + str(prediction) + 
              ' prediction prob: ' + str(prediction_probability) + ' time: ' + str(time.time() - start_time))
        
        #If the prediction was not the star_number we are supposed to be in
        if not (prediction == current_star_number):
            
            next_star = current_star_number + 1
            #If we predicted that it would be the next star, and is high probability prediction 
            if prediction == next_star and prediction_probability > 0.85:
                
                
                consecutive_frames += 1
                prediction_run_time += time.time() - start_time
                #If we have seen the next star multiple times, then likely the star was collected
                if consecutive_frames >= next_star_threshold:
                    #Moves onto next star
                    current_star_number += 1
                    #SPLIT if this is a star we are supposed to split in
                    if current_star_number in splits:
                        if current_star_number in non_fadeout_splits:
                            split_wait_time = 0
                        else:    
                            split_wait_time = fadeout_time-prediction_run_time
                            
                        thread = Thread(target = split, args = (split_key, split_wait_time))
                        thread.start()
                    #0.5 second delay 
                    time.sleep(0.5)
                    consecutive_frames = 0
                    prediction_run_time = 0
            else:
                #Enters here if it misclassified an image
    #            full_img.save(r'E:\misclassified/'+ str(current_star_number) + '/' + str(i) + '.png')
                print('Possible missclassification')
    #            full_img.save(r'E:\wb/' + str(i) + '.png')
                
    
    
