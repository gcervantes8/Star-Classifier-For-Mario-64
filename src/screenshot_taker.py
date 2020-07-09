# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""
from PIL import Image

from mss import mss
import time

# win32 library is the fastest (need to select window), mss is next, and pil is the slowest


class ScreenshotTaker:
    
    # sct is mss screenshot instance, only need to be created once and can be reused
    sct = None
    
    # Top and left are coordinates of the top-left of the window where you want the screenshot
    # Returns 2-tuple of the Pil image and time it took to make screenshot: (img, screenshot_time)
    def screenshot_mss(self, x, y, width, height):
        start_time = time.time()
        if not ScreenshotTaker.sct:
            ScreenshotTaker.sct = mss()

        monitor = {'top': y, 'left': x, 'width': width, 'height': height}

        sct_img = ScreenshotTaker.sct.grab(monitor)
    
        # Create the Image, converts to PIL, probably not needed for speed, but simplifies crop and resize
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        screenshot_time = time.time() - start_time
        return img, screenshot_time
