# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 22:24:01 2017

@author: Gerardo Cervantes
"""

import mss
import mss.tools
from load_NN import fast_screenshot_mss
from PIL import ImageGrab

#preview_image(604,133,695,187)
def preview_image_mss(x, y, width, height):
    sct = mss.mss()
    full_img = fast_screenshot_mss(sct, y, x, width, height)
    full_img.show()
    


def preview_image_pil(x, y, width, height):
    img = ImageGrab.grab(bbox=(x, y, width, height))
    img.show()
    