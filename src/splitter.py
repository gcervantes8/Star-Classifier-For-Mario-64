# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:10:50 2019

@author: Gerardo Cervantes
"""

from win32com.client import Dispatch
from pythoncom import CoInitialize
import time
from threading import Thread
import win32gui

# TODO Capslock and Shift are strange, and can sometimes sends the key 3 times (look into wsh docs)
class Splitter:
    
    wsh = None
    splitting_program = 'LiveSplit'

    def __init__(self):
        CoInitialize()
        self.wsh = Dispatch("WScript.Shell")

    # This function blocks the calling thread
    # program_name is the name of the program that will send the key to. Ex. 'LiveSplit'
    # Split key is the key that will be given to the program to split, should be a str
    # Split_wait_time is float of how long it should wait until it should split
    def _split_helper(self, program_name, split_key, split_wait_time):

        if not self.wsh:
            print('WSH for splitter not initialized')
            CoInitialize()
            self.wsh = Dispatch("WScript.Shell")

        if split_wait_time > 0:
            time.sleep(split_wait_time)

        active_hwnd = win32gui.GetForegroundWindow()
        self.wsh.AppActivate('LiveSplit')  # select LiveSplit application
        self.wsh.SendKeys(split_key)
        win32gui.SetForegroundWindow(active_hwnd)
        print('Program:' + program_name + '\nKey sent:' + split_key)

    # This function splits in a new thread (Does not block calling thread)
    # Split key is the key that will be given to the program to split, should be a str
    # Split_wait_time is float of how long it should wait until it should split
    def split(self, split_key, delay):
        thread = Thread(target=self._split_helper, args=(Splitter.splitting_program, split_key, delay))
        thread.start()
