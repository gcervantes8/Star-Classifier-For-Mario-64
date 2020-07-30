# -*- coding: utf-8 -*-
"""
Created July 27, 2020
@author: Gerardo Cervantes
"""

from PIL import Image
from mss import mss
import time

from src.screenshot_interface import PlatformScreenshot


class GeneralScreenshot(PlatformScreenshot):

    # sct is mss screenshot instance, can be reused
    sct = None

    # Index of monitor that was selected
    selected_monitor_index = None

    def __init__(self):
        self.sct = mss()

    def get_windows_and_monitors_names(self):
        monitor_names = []
        n_monitors = len(self.sct.monitors)
        for i in range(n_monitors):
            monitor_names.append('Monitor ' + str(i+1))
        return monitor_names

    def select_window(self, window_name):
        # Includes the last 2 digits or a space
        monitor_num_in_str = window_name[-3:-1]
        self.selected_monitor_index = int(monitor_num_in_str) - 1

    def screenshot_all_window(self):
        monitor_selected = self._find_monitor()
        # If no monitor was selected
        if monitor_selected is None:
            return None
        width = monitor_selected['width']
        height = monitor_selected['height']
        return self.screenshot_mss(0, 0, width, height)

    def screenshot(self, x, y, width, height):
        monitor_selected = self._find_monitor()
        # If no monitor was selected
        if monitor_selected is None:
            return None

        monitor_selected = self.sct.monitors[self.selected_monitor_index]
        monitor_x = monitor_selected['left'] + x
        monitor_y = monitor_selected['top'] + y
        return self.screenshot_mss(monitor_x, monitor_y, width, height)

    # Return None if no monitor was selected
    def _find_monitor(self):
        if self.selected_monitor_index is not None:
            monitor_selected = self.sct.monitors[self.selected_monitor_index]
            return monitor_selected
        return None

    # Top and left are coordinates of the top-left of the window where you want the screenshot
    # Returns 2-tuple of the Pil image and time it took to make screenshot: (img, screenshot_time)
    def screenshot_mss(self, x, y, width, height):
        if not self.sct:
            self.sct = mss()

        monitor = {'top': y, 'left': x, 'width': width, 'height': height}

        sct_img = self.sct.grab(monitor)

        # Create the Image, converts to PIL, probably not needed for speed, but simplifies crop and resize
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        return img


