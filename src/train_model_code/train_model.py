#Gerardo Cervantes

import numpy as np

#Module in src folder to load images
from sys import path
path.insert(0, '../')

#Keras Library for neural networks
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten, Dropout, advanced_activations
from keras import regularizers
from keras import optimizers
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization

from load_images import get_images
from sklearn.model_selection import train_test_split

from plot_performance import plot_loss, plot_accuracy



import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1' #uncomment to use CPU version of tensorflow


def add_nn_Layers(model):
	
    reg = 0.0001
    dropout = 0.1
    model.add(Conv2D(32, (3, 3), input_shape=(40, 67, 3), kernel_initializer='he_uniform', kernel_regularizer=regularizers.l2(reg))) #200, 350 ; #30, 52
    model.add(Dropout(dropout))
    model.add(advanced_activations.PReLU(weights=None, alpha_initializer='zero'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
#
    model.add(Conv2D(32, (3, 3), kernel_initializer='he_uniform', kernel_regularizer=regularizers.l2(reg)))
    model.add(advanced_activations.PReLU(weights=None, alpha_initializer='zero'))
    model.add(Dropout(dropout))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
#    
#
    model.add(Conv2D(16, (3, 3), kernel_initializer='he_uniform', kernel_regularizer=regularizers.l2(reg)))
    model.add(advanced_activations.PReLU(weights=None, alpha_initializer='zero'))
    model.add(Dropout(dropout))
    model.add(BatchNormalization())
#    model.add(MaxPooling2D(pool_size=(2, 2)))

	
    model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors

    model.add(Dense(256, activation = 'relu', kernel_initializer='he_uniform', kernel_regularizer=regularizers.l2(reg)))
    model.add(advanced_activations.PReLU(weights=None, alpha_initializer='zero'))
    model.add(Dropout(dropout))
    model.add(BatchNormalization())
    
    model.add(Dense(128, kernel_initializer='he_uniform', kernel_regularizer=regularizers.l2(reg)))
    model.add(advanced_activations.PReLU(weights=None, alpha_initializer='zero'))
    model.add(Dropout(dropout))
    model.add(BatchNormalization())

    model.add(Dense(123, activation = 'softmax', kernel_initializer='he_uniform', kernel_regularizer=regularizers.l2(reg))) #Output layer, so 121 since 0 to 120 stars bnoth 0 and 120 inclusive

    return model


#x_train is the training data it will train on
#Kwargs, can be given optional arguments: x_test and y_test.
#If x_test and y_test are given, then it will use them as validation data.
#Returns neural network after it has been trained with the training data
def train_nn(model, batchSize, nEpochs, x_train, y_train, **kwargs):
    if (('x_test' in kwargs) & ('y_test' in kwargs)):
        x_test = kwargs['x_test']
        y_test = kwargs['y_test']
		
        
        history = model.fit(x=x_train, y=y_train, batch_size=batchSize, epochs=nEpochs, verbose=1, callbacks=None, validation_data= (x_test,y_test) )
    else:
        history = model.fit(x=x_train, y=y_train, batch_size=batchSize, epochs=nEpochs, validation_split=10.0, verbose=1, callbacks=None)
    return history

#Saves the neural network model, including the configuration settings and the weights
def save_nn_model(model, fileDir):
    model.save(fileDir)
	
#Loads the neural network model, including the configuration settings and the weights
def load_nn_model(fileDir):
    model = load_model(fileDir)
    return model

#Shuffles x_train and y_train
def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def classifyMarioStar(x_train, y_train, x_test, y_test, save_model_name):
	
    model = Sequential()
    add_nn_Layers(model)
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizers.Nadam(lr=0.0020), #0.0012 before
                  metrics=['accuracy'])
    
    nEpochs = 15
    batchSize = 128
    print('Model summary')
    model.summary()
    
    
    print('Starting training')
    history = train_nn(model, batchSize, nEpochs, x_train, y_train, x_test = x_test, y_test = y_test)
        
    print("Saving Neural Network architecture")
    save_nn_model(model, save_model_name)
    
    plot_loss(history)
    plot_accuracy(history)


if __name__ == "__main__":
    
    main_path = r'E:\MarioStarClassifier/'
    train_players = ['honey14450', 'caivs15818', 'puncayshun_120_13949',
                     'viro14421', 'batora13953',
                     'dwhatever14159', 'mitagi14445',
                     'gohanie14445', 'erumo14949', 'ZDez_120_1-46-19', 'honey14450']
    
    test_players = ['halliinen_14347']
    #r'E:\MarioStarClassifier\train_images'
    #'
#    r'E:\MarioStarClassifier\test_images'
    
    train_images_paths = [os.path.join(main_path, player) for player in train_players]
    test_images_path = [os.path.join(main_path, player) for player in test_players]
    
    
    test_train_split = 0.15
    n_train_imgs = 20 #Number of train images per class
    n_test_imgs = n_train_imgs * test_train_split
    
    save_model_name = '../../models/Model-imgs_perclass' + str(n_train_imgs) + 'epochs15_small_nn'
    x_train, y_train = get_images(train_images_paths, n_train_imgs, True)
    print('Done getting train images')
    
    x_train, y_train = unison_shuffled_copies(x_train, y_train)
    print('Done shuffling train')
    
    if test_images_path != None:
        x_test, y_test = get_images(test_images_path, n_test_imgs, True)
        print('Done getting test images')
        x_test, y_test = unison_shuffled_copies(x_test, y_test)
        print('Done shuffling test')
    else:
        #Splits training data to test and train data
        x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size = test_train_split) 
    
    classifyMarioStar(x_train, y_train, x_test, y_test, save_model_name)


