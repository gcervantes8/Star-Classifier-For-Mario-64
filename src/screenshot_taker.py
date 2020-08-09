# -*- coding: utf-8 -*-
"""

@author: Gerardo Cervantes
"""

from src.windows_screenshot import WindowsScreenshot
from src.general_screenshot import GeneralScreenshot

import os

# win32 library is the fastest (need to select window), mss is next, and pil is the slowest


class ScreenshotTaker:

    screenshot_instance = None

    def __init__(self):
        if os.name == 'nt':
            self.screenshot_instance = WindowsScreenshot()
        else:
            self.screenshot_instance = GeneralScreenshot()

    def get_windows_and_monitors_names(self):
        return self.screenshot_instance.get_windows_and_monitors_names()

    def select_window(self, window_name):
        return self.screenshot_instance.select_window(window_name)

    def screenshot_all_window(self):
        return self.screenshot_instance.screenshot_all_window()

    def screenshot(self, x, y, width, height):
        return self.screenshot_instance.screenshot(x, y, width, height)
