# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 10:31:36 2018

@author: Gerardo Cervantes
"""

class Route():
    
    name = 'Wrong route'
    fadeout_splits = [] 
    fadeout_amounts = []
    immediate_splits = []
    starting_star_number = 0
        
    def __init__(self, name, fadeout_splits, fadeout_amounts, immediate_splits, starting_star_number):
        self.name = name
        self.fadeout_splits = fadeout_splits
        self.fadeout_amounts = fadeout_amounts
        self.immediate_splits = immediate_splits
        self.starting_star_number = starting_star_number
        
    def get_name(self):
        return self.name
    
    def get_category_splitting_information(self):        
        return self.starting_star_number, self.immediate_splits, self.fadeout_splits, self.fadeout_amounts