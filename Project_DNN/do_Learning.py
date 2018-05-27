'''
 손가락 예측 모델
 CNN + LSTM
'''
import scripts.interfaceUtils as util
util.showProcess('Start Program')

import keras
from keras.models import Model
from keras.layers import Conv2D, Dense, LSTM, Flatten, Input, \
                         Activation, Dropout, TimeDistributed, MaxPool2D

import PYTHONPATH
import scripts.paths as path
import scripts.dataFormater as df
import scripts.dataPloter as dp
import scripts.models as models
import scripts.train as train
import scripts.defines as define

import tensorflow as tf
from keras import backend as K
util.showProcess('Loading TF Session')
sess = tf.Session()
K.set_session(sess)

#initialize
path.ifNoDirThanMakeDir('img')
path.ifNoDirThanMakeDir('weight')

# configs
epochs = util.inputInt('How many epochs?')
b1_batch_size = 15 # GPU 메모리 부족으로 Batch_size에 한계 있음
b2_batch_size = 4
m1_batch_size = 4
isLoadWeight = util.inputInt('Load weight? (1 to yes)')
overwrite = True
isGuidenceTrain = util.inputInt('Guidence Train? (1 to yes)')

# load dataset
util.showProcess('Loading dataset')
dirPath_train = path.get('data') + '\\ConvLSTM_train'
dirPath_test = path.get('data') + '\\ConvLSTM_test'

print('Loading Train Data ...')
spointList_train, roiSampleList_train, labelList_train = \
    df.ROI_loadDataListAll(dirPath_train, isShow=False, isShuffle=False)
print('Loading Test Data ...')
spointList_test, roiSampleList_test, labelList_test = \
    df.ROI_loadDataListAll(dirPath_test, isShow=False, isShuffle=False)

# write data plot graph
print('Writing Data Plot Graph ...')
dp.plotSpointDataList(dirPath_train, 2, True, False, True, path.get('img') + '\\d_graph.jpg')
dp.plotSpointDataList(dirPath_train, 2, False, True, True, path.get('img') + '\\d_image.jpg')

# make model
b1 = models.Model_B1()
b2 = models.Model_B2()
m1 = models.Model_M1(b1, b2)

# plot to file
util.showProcess('Saving Model Description')
models.saveModelDescription(b1, path.get('img'), True)
models.saveModelDescription(b2, path.get('img'), True)
models.saveModelDescription(m1, path.get('img'), True)

# Load Weight
if isLoadWeight == 1:
    util.showProcess('Loading Weight')
    models.loadWeight(b1, path.get('weight'))
    models.loadWeight(b2, path.get('weight'))
    models.loadWeight(m1, path.get('weight'))

# Train
if isGuidenceTrain == 1:
    util.showProcess('Train B1')
    b1.fit(spointList_train, labelList_train,
        epochs=int(10),
        verbose=1,
        batch_size=b1_batch_size)
        
    util.showProcess('Train B2')
    b2.fit(roiSampleList_train, labelList_train,
        epochs=int(10),
        verbose=1,
        batch_size=b2_batch_size)

util.showProcess('Train M1')
m1.fit([spointList_train, roiSampleList_train], [labelList_train],
    epochs=int(epochs),
    verbose=1,
    batch_size=m1_batch_size)

util.showProcess('Evaluate M1')
score, acc = m1.evaluate([spointList_train, roiSampleList_train],
                         [labelList_train],
                         batch_size=m1_batch_size)
print('Test score:', score)
print('Test accuracy:', acc)

# Test
util.showProcess('Test b1')
accuracy = train.calculateAccuracy(spointList_test,
                                   labelList_test,
                                   len(labelList_test),
                                   b1, verbose=1,
                                   batch_size=b1_batch_size)
print('Accuracy: ' + str(accuracy))

util.showProcess('Test b2')
accuracy = train.calculateAccuracy(roiSampleList_test,
                                   labelList_test,
                                   len(labelList_test),
                                   b2, verbose=1,
                                   batch_size=b2_batch_size)
print('Accuracy: ' + str(accuracy))

util.showProcess('Test m1')
accuracy = train.calculateAccuracy([spointList_test, roiSampleList_test],
                                   labelList_test,
                                   len(labelList_test),
                                   m1, verbose=1,
                                   batch_size=m1_batch_size)
print('Accuracy: ' + str(accuracy))

# Write Weight
if overwrite:
    util.showProcess('Saving Weight')
    models.saveWeight(b1, path.get('weight'))
    models.saveWeight(b2, path.get('weight'))
    models.saveWeight(m1, path.get('weight'))

sess.close()