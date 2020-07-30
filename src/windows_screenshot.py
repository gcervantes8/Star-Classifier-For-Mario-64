# -*- coding: utf-8 -*-
"""
Created July 27, 2020
@author: Gerardo Cervantes
"""

from src.screenshot_interface import PlatformScreenshot
from src.general_screenshot import GeneralScreenshot
import win32api
import win32gui
import win32ui
import pywintypes
from ctypes import windll
from PIL import Image


class WindowsScreenshot(PlatformScreenshot):
    blacklisted_windows = ['', 'Program Manager', 'Microsoft Store', 'Settings', 'Alarms & Clock', 'Calculator',
                           'Photos', 'Star Classifier', 'File Explorer', 'Microsoft Text Input Application']
    selected_hwnd = None

    # Used for capturing monitor
    mss_screenshot = None

    def __init__(self):
        self.mss_screenshot = GeneralScreenshot()

    def _get_windows_list(self):
        windows_list = []

        def enum_windows_callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title not in WindowsScreenshot.blacklisted_windows:
                    windows_list.append(window_title)
        win32gui.EnumWindows(enum_windows_callback, None)
        return windows_list

    def get_windows_and_monitors_names(self):
        return self._get_windows_list() + self._get_monitor_names()

    # Returns list of given monitor names
    def _get_monitor_names(self):
        monitor_list = win32api.EnumDisplayMonitors()
        monitor_names = []
        for i, monitor in enumerate(monitor_list):
            monitor_name = 'Monitor ' + str(i + 1)
            monitor_names.append(monitor_name)
        return monitor_names

    def select_window(self, window_name):
        if 'Monitor ' in window_name:
            print(window_name)
            self.selected_hwnd = window_name
            print('Found monitor')
        else:
            self.selected_hwnd = win32gui.FindWindow(None, window_name)
            print('A window was selected! Selected window: ')
            print(self.selected_hwnd)

    def screenshot_all_window(self):
        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # left, top, right, bot = win32gui.GetClientRect(hwnd) # GetWindowRect
        print('Screenshot will be taken! Selected window: ')
        print(self.selected_hwnd)
        # If is monitor
        if 'Monitor ' in str(self.selected_hwnd):
            monitor_list = win32api.EnumDisplayMonitors()
            monitor_index = int(self.selected_hwnd[-1:])
            monitor = monitor_list[monitor_index - 1]
            x1, y1, x2, y2, = monitor[2]  # 3rd item in 3-tuple returned by monitor_list
            width = x2 - x1
            height = y2 - y1
            return self.mss_screenshot.screenshot_mss(x1, y1, width, height)
        else:
            try:
                left, top, right, bottom = win32gui.GetClientRect(self.selected_hwnd)
            except pywintypes.error:
                print('Image not found')
                return None
            width = right - left
            height = bottom - top
            return self.screenshot(left, top, width, height)

    # https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
    def screenshot(self, x, y, width, height):

        hwnd_dc = win32gui.GetWindowDC(self.selected_hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, width, height)

        save_dc.SelectObject(save_bit_map)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        result = windll.user32.PrintWindow(self.selected_hwnd, save_dc.GetSafeHdc(), 1)  # Client
        # result = windll.user32.PrintWindow(self.selected_hwnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = save_bit_map.GetInfo()
        bmpstr = save_bit_map.GetBitmapBits(True)

        pil_img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(save_bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.selected_hwnd, hwnd_dc)
        return pil_img


if __name__ == "__main__":
    import time
    s = time.time()
    win_screenshots = WindowsScreenshot()
    windows = win_screenshots.get_windows_and_monitors_names()
    print(windows)
    select_window = windows[2]
    print(select_window)
    win_screenshots.select_window(select_window)
    im = win_screenshots.screenshot_all_window()
    print(time.time() - s)
    print(im)
    im.show()


