# Star-Classifier-For-Mario-64
From an image of the Super Mario 64 game, the neural network will classify how many stars you currently have.

## Benefits

More precise timing than manually splitting.  

Less work for the speedrunner.

Get split times live or from existing video.

Makes splitting at each star viable.


## To run

Requirements:
* Python 3.6
* Tensorflow library (or any other backend library like Theano, testing was done on Tensorflow)
* Keras library


## High level functions


src/train_model.py -  This module is used to train the neural network model. Directory where data is stored needs to be given.


src/load_NN.py -  This module loads an existing model and uses it to split at given star numbers. Coordinates for where to screenshot the game need to be given.


## Data


### Data Information

Data is cropped and resized while getting data for training.  Original image is stored as a screenshot of the whole game, when retrieving the images used for training the screenshot of the whole game is cropped to only the star number.

Image that is fed to neural network is cropped image of the star number of the game that's in the top-right corner.  Image of the data directory structure is of the screenshot of the game.


![Sample image of game from player Siglemic](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/sample_data_siglemic_1.jpg)


![Sample image of game from player Cheese05](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/sample_data_cheese05_1.jpg)


![Sample image of game from player Xiah](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/sample_data_xiah_1.jpg)


![Sample image of game from player ZDeztroyerz](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/sample_data_zdeztroyerz_1.png)




### Data gathering

Data was manually gathered by downloading videos of speedrunners and putting it in the correct folder depending on how many stars they had.

Benefits of gathering data from speedrunning videos is that you know the star amount from a video can only go up, which means you can find the point when they got the star and the point right before they got the next star and you can use all of for data for 1 star.  Assuming the images from video are ordered, this makes for fast image gathering.


Downside of gathering images from speedrunning videos is that many images are very similar to each.  This means validation data is less reliable for checking performance because it might have gotten similar training data (Possibly the next frame of the video).
This can be mitigated by gathering testing data from a separate video rather than splitting training data into train and validation data.  This was not done, instead testing live was done.

### Data labels

Output is a one-hot encoding of how many stars you have.
This is from 0 to 120, as the maximum amount of stars you can get in the game is 120, and the least is 0.  
There was 2 more binary targets added as 121 and 122.  121 is a black screen and 122 is a white screen.

### Data directory structure


```
.
+-- mario64_images
|   +-- 0
|   |	+-- Images from Player1
|   |   |	+-- img1.png
|   |   |	+-- img2.png
|   |   |	+-- img3.png
|   |	+-- Images from Player2
|   |   |	+-- img1.jpg
|   |   |	+-- img2.jpg
|   |   |	+-- img300.jpg
|   +-- 1
|   |	+-- Images from Player20
|   |   |	+-- img100.png
|   +-- 2
|   +-- 3
|   +-- 4
...
|   +-- 120


```

Image names don't matter as long as they are in the correct directory, and they are followed by the .jpg extension or .png.  More extensions could be added to the code besides png or jpg, but they haven't been added as they haven't been tested.

Star numbers go up to 120 because there is that many stars in the game, optionally you can go up to star 122 so that you can represent white and black screens as 121 and 122



This directory structure for the data was chosen so that players could be separated.  
Separating images from different players is done so that we can take an equal amount of images from each player, the alternative is to have all the images in one directory and choosing 
images for training randomly.  The benefits gained from separating players is if one player has many more images of the game, then we don't want their images to be chosen most of the time for training.  
Choosing images from different players to give to the neural network improves the robustness of the neural network because it will learn from different video settings.

## Challenges/Problems


### Data Challenges/Problems

[[https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/jpg_img_with_internet_problems_cheese05.jpg|alt=Sample image of star counter from player Cheese05 in jpg format when they had internet problems]]

Image compression - JPG and PNG
Images were sometimes taken from video streaming platform, when their internet is bad, the image can be pixelated and not useful for training.
Players can use a wide variety of video settings to record gameplay.

### Learning from background of images

Due to the data being gathered being from videos of speedrunners.  The neural network learn started learning what stage you were at and making a prediction based on that.

For example, most Mario 64 videos do stars 96 through 103 in a stage called Snowman's Land, the neural network learned that if the background next to the star number is filled with white snow, then it is most likely one of the stars 96 to 103.

This is likely happened because of lack of different data, and it might have been difficult to classify the number because different video formats were used so it classified based on the background and was still getting decent results with it.

This was fixed by data generation, and an increase in data.

### Screenshot modifications from f.lux

In testing I found that the application can misclassify if you are using an application like f.lux which changes colors on the screen.  This tool will usually still work despite f.lux, but if the settings are really high, then it will no longer work.


### Data Modifications/Preprocessing


![Generated image of star counter](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/generated_preview_1.jpeg)


![Generated image of star counter](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/generated_preview_2.jpeg)


![Generated image of star counter](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/generated_preview_3.jpeg)


![Generated image of star counter](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/generated_preview_4.jpeg)


![Generated image of star counter](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64/tree/master/github_sample_images/generated_preview_5.jpeg)




Benefit of preprocessing is it makes the neural network more robust
Preprocessing and data generation help with:

Improving accuracy when coordinates of screenshot given are slightly wrong.

Improving accuracy of images from S-video, RCA, and RGB video formats.





## Real time challenges (live/online tool) 

To be able to be use this tool in real time, it needs to have a low delay between getting a star, and identifying that you got a new star.

Initial testing showed that most of the running time was in taking a screenshot.

### Fast screenshot tools tested

* PIL library - The PIL library is used for most of the preprocessing steps, so it would be convenient to use this format.
* MSS library - Was found to be faster than using the PIL library, this is the current method used because it is faster than using the PIL library even if you convert to PIL format after taking the screenshot.
* win32 API - To use this, you have to specify the program name that you want to take the screenshot of, it found the program name but when taking the screenshot the screenshot came out to be a black screen, this is supposed to be faster, so if a speedup is needed then looking more into this API could be helpful.

### Current Application Speed


Super Mario 64 runs in 29.97 frames per second (NTSC), the program is able to screenshot and classify how many stars you have in slightly less than a frame.

If there is a need for a speedup, then there are several options.  Get a faster screenshot library, this will have the most impact in speed.  Additionally you could make a smaller neural network model.


### Batch normalization, weight initialization, and x_train modification

Batch normalization, weight initialization (he uniform), and changing x_train so that the values are from 0 to 1 were all done to improve the model.

They greatly helped in lowering the amount of time needed for the neural network to get good results.

## Model I found success with
* 3 Convolution hidden layers with 32, 32, and 16 convolutions per layer.
* Max pooling after every convolution hidden layer
* 1 Dense hidden layer with 128 units after convolution and pooling layers
* Relu was used for all the hidden layers
* Softmax was used for the output layer
* Batch normalization was used after every hidden layer
* he uniform weight initialization
* Regularization of 0.0001
* Loss function: Categorical Cross entropy
* Optimizer: Nadam, learning rate of 0.0006


### Results

In the final version of the model, it didn't take very long for it to classify with an accuracy of over 99%.  The model provided on Github was trained even after it reached over 99% accuracy.
The model provided was trained much longer and was stopped when validation loss would no longer decrease.

The application works well when running in real time.  



## Author
Gerardo Cervantes
