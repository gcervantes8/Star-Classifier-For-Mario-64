# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""
from PIL import Image, ImageGrab

import win32gui
import win32ui
import win32con

#win32 interface is the fastest, mss is next, and pil is the slowest

import mss
import mss.tools
import time

class ScreenshotTaker():
    
    #sct is mss instance, should be created, only need to be created once and can be reused. Used for mss screenshotting
    sct = None
    
    #Screenshots using mss library. (faster than screnshotting using PIL if same mss instance is used)
    
    #Top and left are coordinates of the top-left of the window where you want the screenshot
    #Returns 2-tuple of the Pil image and time it took to make screenshot: (img, screenshot_time)
    def screenshot_mss(self, top, left, width, height):
        start_time = time.time()
        if self.sct == None:
            self.sct = mss.mss()
        
        # The screen part to capture
        monitor = {'top': top, 'left': left, 'width': width, 'height': height}
    
        # Grab the data
        sct_img = self.sct.grab(monitor)
    
        # Create the Image, converts to PIL, probably not needed for speed, but simplifies crop and resize
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        screenshot_time = time.time() - start_time
        return img, screenshot_time
    
    #Screenshots using PIL library
    def screenshot_pil(self, x, y, width, height):
        full_img = ImageGrab.grab(bbox=(x, y, x+width, y+height))
        return full_img


    #Has problem finding Amarec program, finds the windows with 'AmaRecTV', but a black screenshot
    #Is supposed to be able to create fast screenshots
    def fast_screenshot(self, window_name, save_name, w, h):
        hwnd = win32gui.FindWindow(None, window_name)
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
        dataBitMap.SaveBitmapFile(cDC, save_name)
        #Free ResourcesS
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())