from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
import os, sys
import dataFormater
#from keras.utils import plot_model

def getCurrentModel():
    return model_kyg()

def model_kyg(weights_path=None): # weights_path 
    #model.add(ZeroPadding2D(padding=(1, 1), input_shape=(76, 76, 1, )))
    #model.add(MaxPooling2D((2, 2), strides=(2, 2), data_format="channels_first"))

    # input format ::: (samples, rows, cols, channels)
    # * 76 76 1
    model = Sequential()
    model.add(Conv2D(filters=16, kernel_size=(1, 3), strides=(1, 1), data_format="channels_last", activation="relu", input_shape=(76, 76, 1)))
    model.add(Conv2D(filters=16, kernel_size=(1, 3), strides=(1, 1), data_format="channels_last", activation="relu"))
    model.add(Conv2D(filters=16, kernel_size=(1, 3), strides=(1, 1), data_format="channels_last", activation="relu"))
    model.add(Conv2D(filters=16, kernel_size=(1, 3), strides=(1, 1), data_format="channels_last", activation="relu"))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(dataFormater.LABEL_SIZE, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) #loss ?

    if weights_path:
        model.load_weights(weights_path)

    # SAVE MODEL ARCHITECTURE .PNG
    #plot_model(model, to_file='model.png', show_shapes=True)

    return model

def loadModel(modelArchitecture, weightPath):
    if os.path.exists(weightPath):
       modelArchitecture.load_weights(weightPath)

    return modelArchitecture

def saveModel(model, path):
    model.save_weights(path)
