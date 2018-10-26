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
            print('Directory structure did not match, folders have incorrect names')
            continue
            
        create_directory = directory[0] + '/' + dir_name
        if not os.path.exists(create_directory):
            os.makedirs(create_directory)
            
if __name__ == "__main__":
    
    #This will prepare the directory for training by adding directories
    path_to_prepare = r'E:\MarioStarClassifier\test_images'
    stars = 120
    create_main_directory(path_to_prepare, stars)
    create_subdirectory(path_to_prepare, 'ZDez_120_1-46-19')

