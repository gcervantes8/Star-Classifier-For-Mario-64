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

    # name of program it will send key to. Ex. 'LiveSplit'
    splitting_program = 'LiveSplit'

    # This function blocks the calling thread

    # Split key is the key that will be given to the program to split (str)
    # Split_wait_time is number of seconds it should wait until it'll split (float)
    @staticmethod
    def _split_helper(split_key, split_wait_time):

        if not Splitter.wsh:
            print('WSH for splitter not initialized')
            CoInitialize()
            Splitter.wsh = Dispatch("WScript.Shell")

        if split_wait_time > 0:
            time.sleep(split_wait_time)

        active_hwnd = win32gui.GetForegroundWindow()
        Splitter.wsh.AppActivate(Splitter.splitting_program)  # select LiveSplit application
        Splitter.wsh.SendKeys(split_key)
        win32gui.SetForegroundWindow(active_hwnd)
        print('Program:' + Splitter.splitting_program + '\nKey sent:' + split_key)

    # This function splits in a new thread (Does not block calling thread)
    # Split key is the key that will be given to the program to split, should be a str
    # Split_wait_time is float of how long it should wait until it should split
    @staticmethod
    def split(split_key, delay):
        thread = Thread(target=Splitter._split_helper, args=(split_key, delay))
        thread.start()
