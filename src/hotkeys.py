# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 16:13:21 2018

@author: Gerardo Cervantes
"""


class Hotkeys:
    
    split_key = '{PGUP}'
    reset_key = '{PGDN}'
     
    def __init__(self):
        pass
    
    def set_split_key(self, split_key):
        self.split_key = split_key
        
    def set_reset_key(self, reset_key):
        self.reset_key = reset_key
        
    def get_hotkeys(self):
        return self.split_key, self.reset_key
    
    def get_split_key(self):
        return self.split_key
    
    def get_reset_key(self):
        return self.reset_key
