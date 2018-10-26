#Gerardo Cervantes

import numpy as np

path.insert(0, '../')

#Keras Library for neural networks
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten, Dropout
from keras import regularizers
from keras import optimizers
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization

from load_images import get_images
from sklearn.model_selection import train_test_split

from plot_performance import plot_loss, plot_accuracy



#import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1' #uncomment to use CPU version of tensorflow


def add_nn_Layers(model):
	
    reg = 0.0001
#    dropout = 0.1
    model.add(Conv2D(32, (3, 3), input_shape=(40, 67, 3), activation = 'relu', kernel_initializer='he_uniform')) #200, 350 ; #30, 52
#    model.add(Dropout(dropout))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
#
    model.add(Conv2D(32, (3, 3), activation = 'relu', kernel_initializer='he_uniform'))
#    model.add(Dropout(dropout))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
#    
#
    model.add(Conv2D(16, (3, 3), activation = 'relu', kernel_initializer='he_uniform'))
#    model.add(Dropout(dropout))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

	
    model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors

    model.add(Dense(128, activation = 'relu', kernel_initializer='he_uniform', kernel_regularizer=regularizers.l2(reg)))
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
                  optimizer=optimizers.Nadam(lr=0.0006),
                  metrics=['accuracy'])
    
    nEpochs = 30
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
    train_images_path = r'E:\MarioStarClassifier\train_images'
    test_images_path = r'E:\MarioStarClassifier\Mario_64_train_images' #None if you want to split images from train between train and test
    n_imgs = 300
    test_train_split = 0.15
    
    save_model_name = '../models/Model' + n_imgs
    x_train, y_train = get_images(train_images_path, n_imgs)
    print('Done storing the images')
    print('Converting to numpy lists')
    x_train = np.array(x_train).astype(np.float32)
    y_train = np.array(y_train).astype(np.int32)
    print('Done to converting train to numpy float32')
    
    x_train, y_train = unison_shuffled_copies(x_train, y_train)
    print('Done shuffling train')
    
    if test_images_path != None:
        x_test, y_test = get_images(test_images_path, n_imgs)
        
        x_test = np.array(x_test).astype(np.float32)
        y_test = np.array(y_test).astype(np.int32)
        print('Done to converting test to numpy float32')
        x_test, y_test = unison_shuffled_copies(x_test, y_test)
        print('Done shuffling test')
    else:
        #Splits training data to test and train data
        x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size = test_train_split) 
    
    classifyMarioStar(x_train, y_train, x_test, y_test, save_model_name)


