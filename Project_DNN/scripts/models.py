import os

from keras.models import Model
from keras.layers import *
from keras.optimizers import RMSprop, Adam
from keras.utils import plot_model # for model description png
from keras.losses import *
from keras.activations import relu
from keras.applications.xception import Xception, preprocess_input
from keras.applications.inception_v3 import InceptionV3

import interfaceUtils as utils
import defines as define

def _add_BN_ReLU_DO_TD(x, doPercent):
    mainlayerName = str(x.name).split('/')[0]
    x = TimeDistributed(BatchNormalization(), name=mainlayerName + '_BN')(x)
    x = TimeDistributed(Activation('relu'), name=mainlayerName + '_ReLU')(x)
    #x = TimeDistributed(Dropout(doPercent), name=mainlayerName + '_DO')(x)
    return x

def _add_BN_ReLU_SpDO_TD(x, doPercent):
    mainlayerName = str(x.name).split('/')[0]
    x = TimeDistributed(BatchNormalization(), name=mainlayerName + '_BN')(x)
    x = TimeDistributed(Activation('relu'), name=mainlayerName + '_ReLU')(x)
    #x = TimeDistributed(Dropout(doPercent), name=mainlayerName + '_SpDO')(x)
    return x

def _add_BN_ReLU_DO(x, doPercent):
    mainlayerName = str(x.name).split('/')[0]
    x = BatchNormalization(name=mainlayerName + '_BN')(x)
    x = Activation('relu', name=mainlayerName + '_ReLU')(x)
    #x = Dropout(doPercent, name=mainlayerName + '_DO')(x)
    return x

def _add_BN_ReLU_SpDO(x, doPercent):
    mainlayerName = str(x.name).split('/')[0]
    x = BatchNormalization(name=mainlayerName + '_BN')(x)
    x = Activation('relu', name=mainlayerName + '_ReLU')(x)
    #x = SpatialDropout2D(doPercent, name=mainlayerName + '_SpDO')(x)
    return x

def Layer_B1():
    '''
    branch 1 (spoint cnn branch)
    '''
    b1_dropout = 0.4

    b1_input = Input(shape=(150, 74, 1), name='B1_Input')
    #b1 = _add_BN_ReLU_DO(b1, b1_dropout)
    b1 = Conv2D(filters=16,
            kernel_size=(3, 1),
            strides=(1, 1), 
            data_format="channels_last",
            padding = 'same',
            name = 'B1C1')(b1_input)
    b1 = _add_BN_ReLU_SpDO(b1, b1_dropout)
    b1 = MaxPool2D(pool_size=(2, 1))(b1)
    b1 = Conv2D(filters=18,
            kernel_size=(3, 1),
            strides=(1, 1), 
            padding = 'same',
            name = 'B1C2')(b1)
    b1 = _add_BN_ReLU_SpDO(b1, b1_dropout)
    b1 = MaxPool2D(pool_size=(2, 1))(b1)
    b1 = Conv2D(filters=20,
            kernel_size=(5, 1),
            strides=(2, 1),
            padding = 'same',
            name = 'B1C3')(b1)
    b1 = _add_BN_ReLU_SpDO(b1, b1_dropout)
    b1 = Flatten(name='B1F1')(b1)
    b1 = Dense(128, name='B1D1')(b1)
    b1 = _add_BN_ReLU_DO(b1, b1_dropout)
    b1 = Dense(128, name='B1D2')(b1)
    b1 = _add_BN_ReLU_DO(b1, b1_dropout)
    b1 = Dense(128, name='B1D3')(b1)
    b1 = _add_BN_ReLU_DO(b1, b1_dropout)
    b1_output = b1

    return b1_input, b1_output

def Model_B2_FT(inputShape):
    '''
    branch 2 (Fine tune mode)
    '''
    '''
    FREEZE_LAYERS = 5
    
    net = InceptionV3(
        include_top=False,
        weights='imagenet',
        input_tensor=None,
        input_shape=inputShape,

    )
    '''
    '''
    net = Xception(
        include_top=False,
        weights='imagenet',
        input_tensor=None,
        input_shape=inputShape,
    )
    '''
    '''
    plot_model(net, 'lastFTModel.png')
    print('FTModel ploted')
    
    '''
    xi = Input(shape=(35,)+inputShape) #1
    #x = TimeDistributed(net)(xi) #2
    
    x = TimeDistributed(Conv2D(
            filters=16,
            kernel_size=(3, 3),
            strides=(1, 1), 
            data_format="channels_last",
            padding = 'same'))(xi)
    x = TimeDistributed(MaxPool2D())(x)
    x = TimeDistributed(BatchNormalization())(x) #4
    x = TimeDistributed(Activation('relu'))(x)
    x = TimeDistributed(Conv2D(
            filters=16,
            kernel_size=(3, 3),
            strides=(1, 1), 
            data_format="channels_last",
            padding = 'same'))(x)
    x = TimeDistributed(MaxPool2D())(x)
    x = TimeDistributed(BatchNormalization())(x) #4
    x = TimeDistributed(Activation('relu'))(x)
    x = TimeDistributed(Conv2D(
            filters=16,
            kernel_size=(3, 3),
            strides=(1, 1), 
            data_format="channels_last",
            padding = 'same'))(x)
    x = TimeDistributed(MaxPool2D())(x)
    x = TimeDistributed(BatchNormalization())(x) #4
    x = TimeDistributed(Activation('relu'))(x)
    x = TimeDistributed(BatchNormalization())(x) #4
    x = TimeDistributed(Conv2D(
            filters=1,
            kernel_size=(1, 1),
            strides=(1, 1), 
            data_format="channels_last",
            padding = 'same'))(x)
    x = TimeDistributed(Flatten())(x) #4
    x = BatchNormalization()(x)
    x = Activation('relu')(x) #5
    x = LSTM(128, return_sequences=True)(x) # 유닛크기늘려보자 3중R망은어떨가?
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = LSTM(128, return_sequences=False)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dense(128)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dense(128)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    xo = Dense(define.LABEL_SIZE, activation='softmax', name='softmax')(x)
    model = Model(inputs=xi, outputs=xo)
    model.name = 'Model_B2_FT'
    '''
    i = 0
    print(len(model.layers))
    for layer in model.layers:
        i += 1
        if i <= FREEZE_LAYERS:
            layer.trainable = False
        else:
            layer.trainable = True
        print(str(i) + ': ' + str(layer) + ' ' + str(layer.trainable))
    '''
    model.compile(
        optimizer=Adam(lr=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
        )
    model.summary()
    return model

def Layer_B2():    
    '''
    branch 2 (roi cnn+lstm branch)
    '''
    b2_dropout = 0.00

    b2_input = Input(shape=(70, 80, 80, 1), name='B2_Input')
    b2 = TimeDistributed(Conv2D(filters=32,
                                kernel_size=5,
                                strides=2,
                                padding='same',
                                data_format='channels_last'),
                                name='B2C1')(b2_input)
    b2 = _add_BN_ReLU_SpDO_TD(b2, b2_dropout)
    #b2 = TimeDistributed(MaxPool2D(), name='B2C1_MP')(b2)
    b2 = TimeDistributed(Conv2D(filters=32,
                                kernel_size=5,
                                strides=2,
                                padding='same'),
                                name='B2C2')(b2)
    b2 = _add_BN_ReLU_SpDO_TD(b2, b2_dropout)
    #b2 = TimeDistributed(MaxPool2D(), name='B2C2_MP')(b2)
    b2 = TimeDistributed(Conv2D(filters=64,
                                kernel_size=3,
                                strides=1,
                                padding='same',
                                activation='relu'),
                                name='B2C3')(b2)
    b2 = _add_BN_ReLU_SpDO_TD(b2, b2_dropout)
    #b2 = TimeDistributed(MaxPool2D(), name='B2C2_MP')(b2)
    b2 = TimeDistributed(Conv2D(filters=64,
                                kernel_size=3,
                                strides=1,
                                padding='same',
                                activation='relu'),
                                name='B2C4')(b2)
    b2 = _add_BN_ReLU_SpDO_TD(b2, b2_dropout)
    b2 = TimeDistributed(Flatten(), name="B2F1")(b2)
    b2 = TimeDistributed(Dense(256), name="B2D1")(b2)
    b2 = _add_BN_ReLU_DO_TD(b2, b2_dropout)
    b2 = TimeDistributed(Dense(256), name="B2D2")(b2)
    b2 = _add_BN_ReLU_DO_TD(b2, b2_dropout)
    b2 = TimeDistributed(Dense(256), name="B2D3")(b2)
    b2 = _add_BN_ReLU_DO_TD(b2, b2_dropout)
    b2 = LSTM(512, name='B2R3')(b2)    
    b2 = BatchNormalization()(b2)
    b2 = Dense(256, name='B2D4')(b2)
    b2 = _add_BN_ReLU_DO(b2, b2_dropout)
    b2 = Dense(256, name='B2D5')(b2)
    b2 = _add_BN_ReLU_DO(b2, b2_dropout)
    b2 = Dense(256, name='B2D6')(b2)
    b2 = _add_BN_ReLU_DO(b2, b2_dropout)
    
    b2_output = b2
    
    return b2_input, b2_output

def Model_B1():
    i, o = Layer_B1()
    model = Model(i, o)
    model.name = 'B1'
    return model

def Model_B2():
    i, o = Layer_B2()
    model = Model(i, o)
    model.name = 'B2'
    return model

def Model_M1():
    '''
    Merge 1 (b1 + b2)
    # comment
      lr=1e-4로 최소 epoch 60번은 돌려야 2,3을 구분할 수 있더라
    '''
    m1_dropout = 0.0
    m1_learningRate = 1e-3
    #decay_rate = m1_learningRate / 20 # lr/epoches
    #relu_alpha = 0.1

    b1i, b1o = Layer_B1()
    b2i, b2o = Layer_B2()

    x = Concatenate(name='M1M1')([b1o, b2o])
    x = BatchNormalization()(x)
    x = Dense(512, name='M1D1')(x)
    x = _add_BN_ReLU_DO(x, m1_dropout)
    x = Dense(512, name='M1D2')(x)
    x = _add_BN_ReLU_DO(x, m1_dropout)
    x = Dense(512, name='M1D3')(x)
    x = _add_BN_ReLU_DO(x, m1_dropout)
    
    x = Dense(define.LABEL_SIZE, name='M1D4')(x)
    x = BatchNormalization(name='M1D4_BN')(x)
    x = Softmax(name='Softmax')(x)
    m1o = x
    
    optimizer = Adam(lr=m1_learningRate)

    # model.compile(loss_weights={'main_output': 1., 'aux_output': 0.2})
    model = Model(inputs=[b1i, b2i], outputs=[m1o])
    model.name = 'M1'
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model

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
    plot_model(model, to_file=path, show_layer_names=True, show_shapes=True)
    if isShow:
        print(model.name + ' done')