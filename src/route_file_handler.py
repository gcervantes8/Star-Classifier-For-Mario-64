# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 

@author: Gerardo Cervantes
"""

import json
from src.route import Route

class RouteFileHandler():
    
   #Route description
   
   #Game name - is the name of the game
   #Route name - is the name of the route
   #Splits - are the splits it will split at, after enough fadeouts are encountered, then splits
   #Fadeout counts - The number of fadeouts
                     #Turn number to negative to split at a white fadeout
  
    #Returns Route object given a path to a .route file in JSON format
    #Returns None if route couldn't be parsed
    def parse_json_route(self, route_file_path):
        with open(route_file_path, "r") as read_file:
            route_dict = json.load(read_file)
        game_name = self._read_key(route_dict, 'Game name')
        route_name = self._read_key(route_dict, 'Route name')
        splits = self._read_key(route_dict, 'Splits')
        fade_nums = self._read_key(route_dict, 'Fadeout counts')
        
        #Converts json input (string) to a list of integers
        try:
            splits = [int(s) for s in splits.split(',')]
        except ValueError:
            splits = None
        try:
            fade_nums = [int(s) for s in fade_nums.split(',')]
        except ValueError:
            fade_nums = None
            
#        is_ordered = self._read_key(route_dict, 'Ordered')
        
        if splits == None or fade_nums == None: 
            return None
        route = Route(game_name, route_name, splits, fade_nums)
        return route
    
    def _read_key(self, dictionary, key):
        try:
            return dictionary[key]
        except KeyError:
            print('Could not find in route' + key)
        return None
    
    #Finds files ending with .route extension and creates a route object from files
    #Returns a list of Route objects that are initialized
    def get_routes_from_directory(self, dir_path):
        routes = []
        from os import listdir
        from os import path
        for filename in listdir(dir_path):
            if filename.endswith(".route"): 
                route_file_path = path.join(dir_path, filename)
                route = self.parse_json_route(route_file_path)
                if route != None:
                    routes.append(route)
        return routes
        
    def write_json_route(self, file_name, game_name, route_name, splits, fade_nums):
        route_dict = {}
        route_dict['Game name'] = game_name
        route_dict['Route name'] = route_name
#        route_dict['Splits'] = splits
        route_dict['Splits'] = ','.join(str(e) for e in splits)
        route_dict['Fadeout counts'] = ','.join(str(e) for e in fade_nums)
#        route_dict['Fadeout counts'] = fade_nums
#        route_dict['Ordered'] = is_ordered
#        route_dict.write(simplejson.dumps(simplejson.loads(output), indent=4, sort_keys=True))
        
        
        with open(file_name, "w") as write_file:
            json.dump(route_dict, write_file, indent = 4)
  
                
#Used to create a 70 star route file
def route_70_star():
    file_name = '70_star_pro.route'
    game_name = 'Super Mario 64'
    route_name = '70 star - pro'
    splits = [0, 10,13,17,19,24,30,34,39,42,48,52,58,62,69]
    fade_nums = [0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] 
    
    return file_name, game_name, route_name, splits, fade_nums

def route_16_nonlblj_star():
    file_name = '16_star_nonlblj.route'
    game_name = 'Super Mario 64'
    route_name = '16 star - no lblj'
    splits = [0, 1, 6, 8, 9, 11,12,15]
    fade_nums = [0, 1, 1, 1, 2, 1, 1, 1] 
    
    return file_name, game_name, route_name, splits, fade_nums

def route_16_star_pro():
    file_name = '16_star_pro.route'
    game_name = 'Super Mario 64'
    route_name = '16 star - Pro'
    splits = [0, 0, 1, 4, 7, 11, 15, 15, 16, 16, 16]
    fade_nums = [0, 2, 2, 1, 1, 1, 1, -1, 1, 3, 4] 
    
    return file_name, game_name, route_name, splits, fade_nums

if __name__ == "__main__":
    route_handler = RouteFileHandler()
    
#    file_name, game_name, route_name, splits, fade_nums = route_16_nonlblj_star()
    file_name, game_name, route_name, splits, fade_nums = route_16_star_pro()
#    file_name, game_name, route_name, splits, fade_nums = route_70_star()
    
    route_handler.write_json_route(file_name, game_name, route_name, splits, fade_nums)
