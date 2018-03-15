# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 15:36:46 2018

@author: Gerardo Cervantes
"""
import os


#path is the place where the main directory structure will be made
#star_amount should be 120 if doing 120 stars
def create_main_directory(path, star_amount):
	i = 0
	while i <= star_amount:
	
		fullNewPath = path + '/' + str(i)
		if not os.path.exists(fullNewPath):
			os.makedirs(fullNewPath)
	
		i += 1

#Creates directory in every star subfolder directory
#Folder it makes the subdirectory should be an integer
def create_subdirectory(directory_path, dir_name):
    
    for directory in os.walk(directory_path):
        
        _, folder_name = os.path.split(directory[0])
        
        try:
            int(folder_name)
        except ValueError:
            print('Folder name with images should be the star number,'
                + ' no images taken from folder named: ' + folder_name)
            continue;
        
        create_directory = directory[0] + '/' + dir_name
        if not os.path.exists(create_directory):
            os.makedirs(create_directory)
            
