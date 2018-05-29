import os

from keras.models import Model
from keras.layers import *
from keras.optimizers import RMSprop, Adam
from keras.utils import plot_model # for model description png

import dataFormater as DFormat
import interfaceUtils as utils

import defines as define

def _add_Activation_Dropout_TD(x, percent):
    mainlayerName = str(x.name).split('/')[0]
    x = TimeDistributed(Activation('relu'), name=str(mainlayerName + '_AC'))(x)
    x = TimeDistributed(Dropout(percent), name=str(mainlayerName + '_DO'))(x)
    return x

def _add_Activation_Dropout(x, percent):
    mainlayerName = str(x.name).split('/')[0]
    x = Activation('relu', name=str(mainlayerName + '_AC'))(x)
    x = Dropout(percent, name=str(mainlayerName + '_DO'))(x)
    return x

def Model_B1():
    '''
    branch 1 (spoint cnn branch)
    '''
    b1_dropout = 0.5
    b1_learningrate = 1e-4

    branch1_input = Input(shape=(150, 74, 1), name='B1_Input')
    b1 = Conv2D(filters=16,
            kernel_size=(1, 10),
            strides=(1, 1), 
            data_format="channels_last",
            name = 'B1_Conv2D_1')(branch1_input)
    b1 = _add_Activation_Dropout(b1, b1_dropout)
    b1 = Conv2D(filters=16,
            kernel_size=(1, 10),
            strides=(1, 1), 
            name = 'B1_Conv2D_2')(b1)
    b1 = _add_Activation_Dropout(b1, b1_dropout)
    b1 = Conv2D(filters=16,
            kernel_size=(1, 10),
            strides=(1, 1), 
            name = 'B1_Conv2D_3')(b1)
    b1 = _add_Activation_Dropout(b1, b1_dropout)
    b1 = Flatten(name='B1_Flatten')(b1)
    b1 = _add_Activation_Dropout(b1, b1_dropout)
    b1 = Dense(256, name='B1_Dense_1')(b1)
    b1 = _add_Activation_Dropout(b1, b1_dropout)
    branch1_output = Dense(define.LABEL_SIZE, activation='softmax', name='B1_Softmax')(b1)
    
    adma = Adam(lr=b1_learningrate)

    b1_model = Model(branch1_input, branch1_output)
    b1_model.name = 'B1'
    b1_model.compile(optimizer=adma, loss='categorical_crossentropy', metrics=['accuracy'])
    
    return b1_model

def Model_B2():    
    '''
    branch 2 (roi cnn+lstm branch)
    '''
    b2_dropout = 0.01
    b2_learningRate = 5e-5

    branch2_input = Input(shape=(90, 100, 100, 3), name='B2_Input')
    b2 = TimeDistributed(Conv2D(filters=32,
                                kernel_size=5,
                                strides=1,
                                padding='same',
                                data_format='channels_last',
                                activation='relu',
                                ), name='B2_Conv2D_1')(branch2_input)
    b2 = TimeDistributed(MaxPool2D(), name='B2_MaxPool2D_1')(b2)
    b2 = _add_Activation_Dropout_TD(b2, b2_dropout)
    b2 = TimeDistributed(Conv2D(filters=32,
                                kernel_size=5,
                                strides=1,
                                padding='same',
                                activation='relu',), name='B2_Conv2D_2')(b2)
    b2 = TimeDistributed(MaxPool2D(), name='B2_MaxPool2D_2')(b2)
    b2 = _add_Activation_Dropout_TD(b2, b2_dropout)
    b2 = TimeDistributed(Conv2D(filters=32,
                                kernel_size=5,
                                strides=1,
                                padding='same',
                                activation='relu',), name='B2_Conv2D_3')(b2)
    b2 = TimeDistributed(MaxPool2D(), name='B2_MaxPool2D_3')(b2)
    b2 = _add_Activation_Dropout_TD(b2, b2_dropout)
    b2 = TimeDistributed(Flatten(), name="B2_Flatten")(b2)
    b2 = TimeDistributed(Dense(512, activation='relu'), name="B2_Dense_1")(b2)
    b2 = TimeDistributed(Dropout(b2_dropout), name="B2_Dense_1_DO")(b2)
    b2 = TimeDistributed(Dense(512, activation='relu'), name="B2_Dense_2")(b2)
    b2 = TimeDistributed(Dropout(b2_dropout), name="B2_Dense_2_DO")(b2)
    b2 = LSTM(512, dropout=b2_dropout, name='B2_LSTM_1')(b2)
    b2 = Dense(256, activation='relu', name='B2_Dense_3')(b2)
    b2 = Dropout(b2_dropout, name='B2_Dense_3_DO')(b2)
    branch2_output = Dense(define.LABEL_SIZE, activation='softmax', name='B2_Softmax')(b2)

    rms = RMSprop(lr=b2_learningRate) # lr 중요

    b2_model = Model(branch2_input, branch2_output)
    b2_model.name = 'B2'
    b2_model.compile(optimizer=rms, loss='categorical_crossentropy', metrics=['accuracy'])
    
    return b2_model

def Model_M1(b1, b2):
    '''
    Merge 1 (b1 + b2)
    '''
    m1_dropout = 0.01
    m1_learningRate = 5e-5
    
    x = Add()([b1.outputs[0], b2.outputs[0]])
    x = Dense(128, activation='relu')(x)
    x = Dropout(m1_dropout)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(m1_dropout)(x)
    merge1_output = Dense(define.LABEL_SIZE, activation='softmax', name='M1_Softmax')(x)

    rms = RMSprop(lr=m1_learningRate) # lr 중요

    # Model compile
    # model.compile(loss_weights={'main_output': 1., 'aux_output': 0.2})
    m1_model = Model(inputs=[b1.inputs[0], b2.inputs[0]], outputs=[merge1_output])
    m1_model.name = 'M1'
    m1_model.compile(optimizer=rms, loss='categorical_crossentropy', metrics=['accuracy'])

    return m1_model

def loadWeight(model, dirPath):
    path = os.path.join(dirPath, model.name + '.h5')

    if os.path.exists(path):
        #print('Loading Architecture: ' + model.name)
        
        model.load_weights(path)
        print('Loading Weight : ' + model.name)

    else:
        utils.showError('Loading Weight Fail : ' + model.name)

    return model

def saveWeight(model, dirPath):
    path = os.path.join(dirPath, model.name + '.h5')
    
    print ('Saving model: ' + model.name)
    print ('Path: ' + path)
    model.save_weights(path)

def saveModelDescription(model, path, isShow):
    path = os.path.join(path, 'md_' + model.name + '.jpg')
    plot_model(model, to_file=path, show_shapes=True)
    if isShow:
        print(model.name + ' done')