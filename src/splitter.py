# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:10:50 2019

@author: Gerardo Cervantes
"""

from win32com.client import Dispatch
from pythoncom import CoInitialize
import time
from threading import Thread

#This function blocks the calling thread
#program_name is the name of the program that will send the key to. Ex. 'LiveSplit'
#Split key is the key that will be given to the program to split, should be a str
#Split_wait_time is float of how long it should wait until it should split
def _split_helper(program_name, split_key, split_wait_time):
    CoInitialize()

    if split_wait_time > 0:
        time.sleep(split_wait_time)
        
    wsh = Dispatch("WScript.Shell")
    wsh.AppActivate(program_name) # select livesplit application
    wsh.SendKeys(split_key)
    
#This function splits in a new thread (Does not block calling thread)
#program_name is the name of the program that will send the key to. Ex. 'LiveSplit'
#Split key is the key that will be given to the program to split, should be a str
#Split_wait_time is float of how long it should wait until it should split
def split(program_name, split_key, delay):
    thread = Thread(target = _split_helper, args = (program_name, split_key, delay))
    thread.start()

