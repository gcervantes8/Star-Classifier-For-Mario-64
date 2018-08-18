# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 

@author: Gerardo Cervantes
"""

import json
from route import Route
import os

class RouteFileHandler():
    
    def write_json_route(self, file_name, name, fadeout_splits, fadeout_amounts, immediate_splits, starting_star_number):
        dictionary = {}
        dictionary['name'] = name
        dictionary['fadeout_splits'] = fadeout_splits
        dictionary['fadeout_amounts'] = fadeout_amounts
        dictionary['immediate_splits'] = immediate_splits
        dictionary['starting_star_number'] = starting_star_number
        
        
        with open(file_name, "w") as write_file:
            json.dump(dictionary, write_file)
    
    def parse_json_route(self, route_file_path):
        with open(route_file_path, "r") as read_file:
            dictionary = json.load(read_file)
        
        name = dictionary['name']
        fadeout_splits = dictionary['fadeout_splits']
        fadeout_amounts = dictionary['fadeout_amounts']
        immediate_splits = dictionary['immediate_splits']
        starting_star_number = dictionary['starting_star_number']
        
        route = Route(name, fadeout_splits, fadeout_amounts, immediate_splits, starting_star_number)
        return route
        
    def get_routes_from_directory(self, dir_path):
        routes = []
        for filename in os.listdir(dir_path):
            if filename.endswith(".route"): 
                route_file_path = os.path.join(dir_path, filename)
                route = self.parse_json_route(route_file_path)
                routes.append(route)
        return routes
                

def route_70_star():
    file_name = '70_star_pro_route.route'
    name = '70 star - pro'
    fadeout_splits = [10,13,17,19,24,30,34,39,42,48,52,58,62,69]
    fadeout_amounts = [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] 
    
    #Stars where it should split immediately after grabbing the star
    immediate_splits = [0]
    starting_star_number = 0
    
    return file_name, name, fadeout_splits, fadeout_amounts, immediate_splits, starting_star_number

def route_16_nonlblj_star():
    file_name = '16_star_nonlblj_route.route'
    name = '16 star no lblj'
    fadeout_splits = [1, 6, 8, 9, 11,12,15]
    fadeout_amounts = [1, 1, 1, 2, 1, 1, 1] 
    
    #Stars where it should split immediately after grabbing the star
    immediate_splits = [0]
    starting_star_number = 0
    
    return file_name, name, fadeout_splits, fadeout_amounts, immediate_splits, starting_star_number

if __name__ == "__main__":
    route_handler = RouteFileHandler()
    
    file_name, name, fadeout_splits, fadeout_amounts, immediate_splits, starting_star_number = route_16_nonlblj_star()
    
    route_handler.write_json_route(file_name, name, fadeout_splits, fadeout_amounts, immediate_splits, starting_star_number)
    
    
