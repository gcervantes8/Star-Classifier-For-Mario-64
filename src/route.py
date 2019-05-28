# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 10:31:36 2018

@author: Gerardo Cervantes
"""

class Route():
    
    game = 'Unknown game'
    name = 'Invalid route'
    splits = [] 
    fadeout_nums = []
        
    #Create route object, default values are kept if given items are None
    #If fade_nums is empty or smaller than splits, fills with values to make it split immediately
    def __init__(self, game_name, route_name, splits, fade_nums):
        if game_name != None:
            self.game = game_name
        if route_name != None:
            self.name = route_name
        
        #Append fade_nums with 0's (split immediately) if not same size as splits
        diff = len(splits) - len(fade_nums)
        if diff > 0:
            fade_nums = fade_nums + ([0] * diff )
            
        if splits != None:
            self.splits = splits
        if fade_nums != None:
            self.fadeout_nums = fade_nums
#        if is_ordered != None:
#            self.is_ordered = is_ordered
        
    def get_game(self):
        return self.game
        
    def get_name(self):
        return self.name
    
    def get_category_split_info(self):        
        return self.splits.copy(), self.fadeout_nums.copy()