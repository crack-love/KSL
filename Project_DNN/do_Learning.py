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
import scripts.dataFormater as df
import scripts.dataPloter as dp
import scripts.models as models
import scripts.train as train
import scripts.defines as define
from scripts.Path import Path

import tensorflow as tf
from keras import backend as K
util.showProcess('Loading TF Session')
sess = tf.Session()
K.set_session(sess)

#initialize
Path.ifNoDirThanMakeDir('img')
Path.ifNoDirThanMakeDir('weight')

# configs
epochs = util.inputInt('How many epochs?')
b1_batch_size = 15 # GPU 메모리 부족으로 Batch_size에 한계 있음
b2_batch_size = 15
m1_batch_size = 15
isLoadWeight = util.inputInt('Load weight? (1 to yes)')
overwrite = True

# load dataset
util.showProcess('Loading dataset')
dirPath_train = Path.get('train')
dirPath_test = Path.get('test')

print('Loading Train Samples : ')
spointList_train, roiSampleList_train, labelList_train = \
    df.ROI_loadDataListAll(dirPath_train, isShow=False, isShuffle=True)
print('Loading Test Samples : ')
spointList_test, roiSampleList_test, labelList_test = \
    df.ROI_loadDataListAll(dirPath_test, isShow=False, isShuffle=False)

# write data plot graph
dp.plotSpointDataList(dirPath_train, 2, 2, False, Path.get('img') + '\\d_graph')
dp.plotSpointDataList(dirPath_train, 2, 2, True, Path.get('img') + '\\d_image')

# make model, b1/b2는 구조 print용
util.showProcess('Model Generating')
b1 = models.Model_B1()
util.showProcess('B1')
b1.summary()
b2 = models.Model_B2()
util.showProcess('B2')
b2.summary()
m1 = models.Model_M1()
#util.showProcess('M1')
#m1.summary()

# plot to file
models.saveModelDescription(b1, Path.get('img'), False)
models.saveModelDescription(b2, Path.get('img'), False)
models.saveModelDescription(m1, Path.get('img'), False)

# Load Weight
if isLoadWeight == 1:
    util.showProcess('Loading Weight')
    models.loadWeight(m1, Path.get('weight'))

# Train
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
util.showProcess('Test M1')
accuracy = train.calculateAccuracy([spointList_test, roiSampleList_test],
                                   labelList_test,
                                   len(labelList_test),
                                   m1, verbose=1,
                                   batch_size=1)
print('Accuracy: ' + str(accuracy))

# Write Weight
if overwrite:
    util.showProcess('Saving Weight')
    models.saveWeight(m1, Path.get('weight'))

sess.close()
