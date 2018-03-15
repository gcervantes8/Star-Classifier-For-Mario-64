# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 09:09:26 2017

@author: ZDeztroyerz
"""

import matplotlib.pyplot as plt

def plot_loss(history):
    plot(history.history['loss'], history.history['val_loss'], 'Model loss', 'epoch', 'loss')
    
def plot_accuracy(history):
    plot(history.history['acc'], history.history['val_acc'], 'Model accuracy', 'epoch', 'accuracy')

def plot(loss_on_train, loss_on_test, titleLabel, xLabel, yLabel):
    plt.plot(loss_on_train)
    plt.plot(loss_on_test)
    plt.title(titleLabel)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    

    
    
    