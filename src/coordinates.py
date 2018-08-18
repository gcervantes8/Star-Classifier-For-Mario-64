# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 22:44:10 2018

@author: Gerardo Cervantes
"""

class Coordinates():
    
    x = -1
    y = -1
    width = -1
    height = -1
     
    def __init__(self):
        pass
    
    def set_coordinates(self, x, y, width, height):
        
        #Only assign if it's an integer, otherwise keep previous value
        self.x = int(x) if self.is_integer(x) else self.x
        self.y = int(y) if self.is_integer(y) else self.y
        self.width = int(width) if self.is_integer(width) else self.width
        self.height = int(height) if self.is_integer(height) else self.height
        
    def is_integer(self, var):
        try:
            int(var)
            return True
        except (ValueError, TypeError) as e:
            return False
        
    def get_coordinates(self):
        return self.x, self.y, self.width, self.height
