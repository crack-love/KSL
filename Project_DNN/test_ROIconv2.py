'''
 손가락 예측 모델
 CNN + LSTM
'''
import keras
from keras.models import Model
from keras.layers import Conv2D, Dense, LSTM, Flatten, Input, CuDNNLSTM, \
Activation, Dropout, BatchNormalization, TimeDistributed, MaxPool2D
from keras import optimizers

import PYTHONPATH
import scripts.paths as path
import scripts.dataFormater as df
import scripts.dataPloter as dp
import scripts.interfaceUtils as util
import scripts.models as models
import scripts.train as train
import scripts.defines as define

util.showProcess('Loading TF Session')
import tensorflow as tf
sess = tf.Session()
from keras import backend as K
K.set_session(sess)


def add_BatchNormal_Activation_Dropout_TD(x, percent):
    mainlayerName = str(x.name).split('/')[0]
    #x = TimeDistributed(BatchNormalization(momentum=0.01), name=str(mainlayerName + '_BN'))(x)
    x = TimeDistributed(Activation('relu'), name=str(mainlayerName + '_AC'))(x)
    x = TimeDistributed(Dropout(percent), name=str(mainlayerName + '_DO'))(x)
    return x    

def add_BatchNormal_Activation_Dropout(x, percent):
    mainlayerName = str(x.name).split('/')[0]
    #x = BatchNormalization(momentum=0.01, name=str(mainlayerName + '_BN'))(x)
    x = Activation('relu', name=str(mainlayerName + '_AC'))(x)
    x = Dropout(percent, name=str(mainlayerName + '_DO'))(x)
    return x  

import numpy as np
import random
def shuffleDataset(d1, d2, d3):
    if len(d1) != len(d2) or len(d2) != len(d3):
        raise Exception("Lengths don't match")
    indexes = list(range(len(d1)))
    random.shuffle(indexes)
    d1_shuffled = [d1[i] for i in indexes]    
    d2_shuffled = [d2[i] for i in indexes]
    d3_shuffled = [d3[i] for i in indexes]
    return np.array(d1_shuffled), np.array(d2_shuffled), np.array(d3_shuffled)

# config
configs = {}
configs['epochs'] = 30
configs['b1_dropout'] = 0.5
configs['b2_dropout'] = 0.05
configs['m1_dropout'] = 0.0
configs['b1_batch_size'] = 15
configs['b2_batch_size'] = 12
configs['m1_batch_size'] = 12
configs['b2_learningRate'] = 0.00008
print(configs)

# input
epochs = int(util.input('How many epochs?'))
b2_dropout = float(util.input('Branch2 dropout? (recomend < 0.05)'))
isTrainM1 = int(util.input('Is Train M1? (1 to yes)'))
isLoadWeight = int(util.input('load weight? (1 to yes)'))
configs['epochs'] = epochs
configs['b2_dropout'] = b2_dropout

# load dataset
util.showProcess('Loading dataset')
dirPath_train = path.get('data') + '\\ConvLSTM_train'
dirPath_test = path.get('data') + '\\ConvLSTM_test'
samplePathList_train = df.ROI_loadAllSamplePaths(dirPath_train)
samplePathList_test = df.ROI_loadAllSamplePaths(dirPath_test)

print('Loading Train Data ...')
spointList_train, roiSampleList_train, labelList_train = \
    df.ROI_loadDataList(samplePathList_train, False)
print('Loading Test Data ...')
spointList_test, roiSampleList_test, labelList_test = \
    df.ROI_loadDataList(samplePathList_test, False)

# Plot
#dp.plotSpointDataList(path.get('data') + "\\ConvLSTM_train", 2, True, True)

# shufle dataset
'''
spointList_train, roiSampleList_train, labelList_train = \
    shuffleDataset(spointList_train, roiSampleList_train, labelList_train)'''
'''spointList_test, roiSampleList_test, labelList_test = \
    shuffleDataset(spointList_test, roiSampleList_test, labelList_test)'''

# branch 1 (spoint cnn branch)
b1_dropout = configs.get('b1_dropout')
branch1_input = Input(shape=(150, 74, 1), name='B1_Input')
b1 = Conv2D(filters=16,
           kernel_size=(1, 3),
           strides=(1, 1), 
           data_format="channels_last",
           name = 'B1_Conv2D_1')(branch1_input)
b1 = add_BatchNormal_Activation_Dropout(b1, b1_dropout)
b1 = Conv2D(filters=16,
           kernel_size=(1, 3),
           strides=(1, 1), 
           name = 'B1_Conv2D_2')(b1)
b1 = add_BatchNormal_Activation_Dropout(b1, b1_dropout)
b1 = Conv2D(filters=16,
           kernel_size=(1, 3),
           strides=(1, 1), 
           name = 'B1_Conv2D_3')(b1)
b1 = add_BatchNormal_Activation_Dropout(b1, b1_dropout)
b1 = Flatten(name='B1_Flatten')(b1)
b1 = add_BatchNormal_Activation_Dropout(b1, b1_dropout)
b1 = Dense(256, name='B1_Dense_1')(b1)
b1 = add_BatchNormal_Activation_Dropout(b1, b1_dropout)
b1 = Dense(256, name='B1_Dense_2')(b1)
b1 = add_BatchNormal_Activation_Dropout(b1, b1_dropout)
branch1_output = Dense(define.LABEL_SIZE, activation='softmax', name='B1_Output')(b1)
# output activation을 relu로 했을 때 발산/소실하다가 softmax로 하니까 정상 예측한다.

# branch 2 (roi cnn+lstm branch)
b2_dropout = configs.get('b2_dropout')
branch2_input = Input(shape=(90, 100, 100, 3), name='B2_Input')
b2 = TimeDistributed(Dropout(0.0))(branch2_input)
b2 = TimeDistributed(Conv2D(filters=32,
                            kernel_size=5,
                            strides=1,
                            padding='same',
                            data_format='channels_last',
                            activation='relu',
                            ), name='B2_Conv2D_1')(b2)
b2 = TimeDistributed(MaxPool2D())(b2)
b2 = TimeDistributed(Dropout(b2_dropout))(b2)
b2 = TimeDistributed(Conv2D(filters=32,
                            kernel_size=5,
                            strides=1,
                            padding='same',
                            activation='relu',), name='B2_Conv2D_2')(b2)
b2 = TimeDistributed(MaxPool2D())(b2)
b2 = TimeDistributed(Dropout(b2_dropout))(b2)
b2 = TimeDistributed(Conv2D(filters=32,
                            kernel_size=5,
                            strides=1,
                            padding='same',
                            activation='relu',), name='B2_Conv2D_3')(b2)
b2 = TimeDistributed(MaxPool2D())(b2)
b2 = TimeDistributed(Dropout(b2_dropout))(b2)
b2 = TimeDistributed(Flatten())(b2)
b2 = TimeDistributed(Dropout(b2_dropout))(b2)
b2 = TimeDistributed(Dense(512, activation='relu'))(b2)
b2 = TimeDistributed(Dropout(b2_dropout))(b2)
b2 = TimeDistributed(Dense(512, activation='relu'))(b2)
b2 = TimeDistributed(Dropout(b2_dropout))(b2)
b2 = LSTM(512, dropout=b2_dropout, name='B2_LSTM_1')(b2)
b2 = Dropout(b2_dropout)(b2)
b2 = Dense(256, activation='relu')(b2)
b2 = Dropout(b2_dropout)(b2)
b2 = Dense(256, activation='relu')(b2)
b2 = Dropout(b2_dropout)(b2)
branch2_output = Dense(define.LABEL_SIZE, activation='softmax', name='B2_Output')(b2)

# Merge 1
#model.compile(loss_weights={'main_output': 1., 'aux_output': 0.2})
#m1_dropout = configs.get('m1_dropout')
x = keras.layers.Add()([branch2_output, branch1_output])
x = Dense(128, activation='relu')(x)
x = Dense(128, activation='relu')(x)
merge1_output = Dense(define.LABEL_SIZE, activation='softmax', name='M1_Output')(x)

# Model compile
b1_model = Model(branch1_input, branch1_output)
b1_model.name = 'KYG_Spoint1'
b1_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

rms = optimizers.RMSprop(lr=configs.get('b2_learningRate')) # lr 중요
b2_model = Model(branch2_input, branch2_output)
b2_model.name = 'KYG_HROI1'
b2_model.compile(optimizer=rms, loss='categorical_crossentropy', metrics=['accuracy'])

m1_model = Model(inputs=[branch1_input, branch2_input], outputs=[merge1_output])
m1_model.name = 'KYG_Merge1'
m1_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Load Weight
if isLoadWeight == 1:
    b1_model.load_weights(path.get('data') + '\\' + b1_model.name + '.h5')
    b2_model.load_weights(path.get('data') + '\\' + b2_model.name + '.h5')
    m1_model.load_weights(path.get('data') + '\\' + m1_model.name + '.h5')

# Train
# GPU 메모리 부족으로 Batch_size에 한계 있음

util.showProcess('Train b1')
b1_model.summary()
b1_model.fit(spointList_train,
             labelList_train,
             epochs=int(configs.get('epochs')/2),
             verbose=1,
             batch_size=configs.get('b1_batch_size'))

util.showProcess('Train b2')
b2_model.summary()
b2_model.fit(roiSampleList_train,
             labelList_train,
             epochs=int(configs.get('epochs')),
             verbose=1,
             batch_size=configs.get('b2_batch_size'))
'''
if isTrainM1 == 1:
    util.showProcess('Train m1')
    m1_model.summary()
    m1_model.fit({'B1_Input':spointList_train, 'B2_Input':roiSampleList_train},
                [labelList_train, labelList_train, labelList_train],
                epochs=int(epochs),
                verbose=1,
                batch_size=configs.get('m1_batch_size'))
'''
# Evaluate
b1_batch_size = configs.get('b1_batch_size')
b2_batch_size = configs.get('b2_batch_size')
m1_batch_size = configs.get('m1_batch_size')
'''
util.showProcess('Evaluate b1')
score, acc = b1_model.evaluate(spointList_test, labelList_test, batch_size=b1_batch_size)
print('Test score:', score)
print('Test accuracy:', acc)

util.showProcess('Evaluate b2 with train')
score, acc = b2_model.evaluate(roiSampleList_train, labelList_train, batch_size=b2_batch_size)
print('Test score:', score)
print('Test accuracy:', acc)

util.showProcess('Evaluate b2 with test')
m1_model.evaluate([spointList_test, roiSampleList_test], [labelList_test, labelList_test, labelList_test], batch_size=b2_batch_size)
#print('Test score:', score)
#print('Test accuracy:', acc)
'''

# Test
util.showProcess('Test b1')
accuracy = train.calculateAccuracy(spointList_test,
                                   labelList_test,
                                   len(labelList_test),
                                   b1_model, verbose=1,
                                   batch_size=b1_batch_size)
print('Accuracy: ' + str(accuracy))

util.showProcess('Test b2')
accuracy = train.calculateAccuracy(roiSampleList_test,
                                   labelList_test,
                                   len(labelList_test),
                                   b2_model, verbose=1,
                                   batch_size=b2_batch_size)
print('Accuracy: ' + str(accuracy))
'''
util.showProcess('Test m1')
accuracy = train.calculateAccuracy({'B1_Input':spointList_test, 'B2_Input':roiSampleList_test},
                                    labelList_test,
                                    len(labelList_test),
                                    m1_model, verbose=1,
                                    batch_size=m1_batch_size)
print('Accuracy: ' + str(accuracy))

util.showProcess('Test b1 with training data')
accuracy = train.calculateAccuracy(spointList_train,
                                   labelList_train,
                                   len(labelList_train),
                                   b1_model, verbose=1,
                                   batch_size=b1_batch_size)
print('Accuracy: ' + str(accuracy))

util.showProcess('Test b2 with training data')
accuracy = train.calculateAccuracy(roiSampleList_train,
                                   labelList_train,
                                   len(labelList_train),
                                   b2_model, verbose=1,
                                   batch_size=b2_batch_size)
print('Accuracy: ' + str(accuracy))

util.showProcess('Test m1 with training data')
accuracy = train.calculateAccuracy({'B1_Input':spointList_train, 'B2_Input':roiSampleList_train},
                                    labelList_train,
                                    len(labelList_train),
                                    m1_model, verbose=1,
                                    batch_size=m1_batch_size)
print('Accuracy: ' + str(accuracy))
'''
overwrite = True
if overwrite:
    util.showProcess('Saving model')
    b1_model.save(path.get('data') + '\\' + b1_model.name + '.h5')
    print(b1_model.name + ' done')
    b2_model.save(path.get('data') + '\\' + b2_model.name + '.h5')
    print(b2_model.name + ' done')
    m1_model.save(path.get('data') + '\\' + m1_model.name + '.h5')
    print(m1_model.name + ' done')

sess.close()