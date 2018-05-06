from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.utils import plot_model # for model description png
import dataFormater as DFormat
import os
import interfaceUtils as utils

def getCurrentModel():
    return model_kyg()

def model_kyg():
    # model.add(ZeroPadding2D(padding=(1, 1), input_shape=(76, 76, 1, )))
    # model.add(MaxPooling2D((2, 2), strides=(2, 2), data_format="channels_first"))
    # 
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
    model.add(Dense(DFormat.LABEL_SIZE, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) #loss ?
    model.name = 'KYG_C4D2'

    return model

def loadModel(weightPath):
    model = getCurrentModel()
    print('Loading Architecture: ' + model.name)
    
    if os.path.exists(weightPath):
       model.load_weights(weightPath)
       print('Loading Weight: ' + weightPath)
    else:
        utils.showError('Loading Weight Fail')

    return model

def saveModel(model, path):
    model.save_weights(path)
    print ('Saving model: ' + model.name)
    print ('Path: ' + path)

def saveModelDescription(model, path):
    plot_model(model, to_file=path, show_shapes=True)