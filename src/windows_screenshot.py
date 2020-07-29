# -*- coding: utf-8 -*-
"""
Created July 27, 2020
@author: Gerardo Cervantes
"""

from src.screenshot_interface import PlatformScreenshot

import win32api
import win32gui
import win32ui
from ctypes import windll
from PIL import Image


# TODO USE THIS: https://stackoverflow.com/questions/38970354/win32gui-findwindow-not-finding-window
class WindowsScreenshot(PlatformScreenshot):
    blacklisted_windows = ['', 'Program Manager', 'Microsoft Store', 'Settings', 'Alarms & Clock', 'Calculator',
                           'Photos']
    selected_hwnd = None

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
            monitor_id = monitor[0]
            monitor_info = win32api.GetMonitorInfo(monitor_id)
            name = monitor_info['Device']
            monitor_name = 'Monitor ' + str(i + 1) + ' ' + name
            monitor_names.append(monitor_name)
        return monitor_names

    def select_window(self, window_name):
        self.selected_hwnd = win32gui.FindWindow(None, window_name)

    def screenshot_all_window(self):
        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # left, top, right, bot = win32gui.GetClientRect(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(self.selected_hwnd)
        width = right - left
        height = bottom - top
        return self.screenshot(left, top, width, height)

    # https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
    def screenshot(self, x, y, width, height):

        hwndDC = win32gui.GetWindowDC(self.selected_hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(self.selected_hwnd, saveDC.GetSafeHdc(), 0)
        print(result)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.selected_hwnd, hwndDC)
        return im


if __name__ == "__main__":
    import time
    s = time.time()
    win_screenshots = WindowsScreenshot()
    monitors = win_screenshots.get_windows_and_monitors_names()
    print(monitors)
    windows = win_screenshots._get_windows_list()
    print(windows)
    select_window = windows[2]
    print(select_window)
    win_screenshots.select_window(select_window)
    im = win_screenshots.screenshot_all_window()
    print(time.time() - s)
    print(im)
    im.show()


