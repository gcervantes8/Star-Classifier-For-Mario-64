# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 20:17:09 2018

@author: Gerardo Cervantes
"""

#A display function for the star classifier
def print_progress_information(star, prediction, probability, time):
    print('Star: ' + star + ' Prediction: ' + str(prediction) + ' Probability: ' + 
                  "{0:.2f}".format(probability) + ' Time: ' + "{0:.3f}".format(time))