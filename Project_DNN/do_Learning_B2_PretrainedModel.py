'''
손가락 예측 모델
CNN + LSTM

# Structure of data directory
/train
        /label0
        /label1
                /sample0
                /sample1
                        /sequence1.jpg
                        /sequence2.jpg
                        ...
                        /sequence74.jpg
                        /Spoints.txt
                /sample2
                ...
                /sampleN
        /label2
        /label3
        ...
        /labelM
'''

import scripts.interfaceUtils as util
util.showProcess('Start Program')

import PYTHONPATH
import scripts.dataFormater as df
import scripts.dataPloter as dp
import scripts.models as models
import scripts.train as train
import scripts.defines as define
from scripts.Path import Path
'''
import tensorflow as tf
from keras import backend as K
util.showProcess('Loading TF Session')
sess = tf.Session()
K.set_session(sess)
'''
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Model
from keras.layers import *
from keras.optimizers import Adam
from keras.applications.xception import Xception, preprocess_input
from keras.utils import plot_model # for model description png
from keras.preprocessing import image # image.load_img
import matplotlib.pyplot as plt # plt.imshow
from PIL import Image

import os

DATASET_PATH_TRAIN = '../data/ConvLSTM/train'
DATASET_PATH_TEST = '../data/ConvLSTM/test'
IMAGE_SIZE    = (299, 299)
NUM_CLASSES   = 2
BATCH_SIZE    = 5
FREEZE_LAYERS = 132
NUM_EPOCHS    = util.inputInt('How many epochs?')
WEIGHTS_FINAL = 'CL_fine_tune.h5'
isLoadWeight = util.inputInt('Load weight? (1 to yes)')
overwirte = True

train_imgGen = ImageDataGenerator(
    #preprocessing_function=preprocess_input,
    rescale=1./255,
    rotation_range=35,
    shear_range=15,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    channel_shift_range=10,
    vertical_flip=False,
    horizontal_flip=False,
    fill_mode='nearest'
)
    
test_imgGen = ImageDataGenerator(
    rescale = 1./255
)

train_batchIter = df.generator_multiple(
    train_imgGen,
    DATASET_PATH_TRAIN,
    IMAGE_SIZE,
    BATCH_SIZE
)

test_batchIter = df.generator_multiple(
    test_imgGen,
    DATASET_PATH_TEST,
    IMAGE_SIZE,
    BATCH_SIZE
)

util.showProcess('Class indices')
for cls, idx in train_batchIter.class_indices.items():
    print('Class #{} = {}'.format(idx, cls))

# write data plot graph
dp.plotSpointDataList(dirPath_train, 1, 1, False, Path.get('img') + '\\d_graph')
dp.plotSpointDataList(dirPath_train, 1, 1, True, Path.get('img') + '\\d_image')

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

util.showProcess('Evaluate M1 Batch_Size_1')
score, acc = m1.evaluate([spointList_train, roiSampleList_train],
                         [labelList_train],
                         batch_size=1)
print('Test score:', score)
print('Test accuracy:', acc)

util.showProcess('Evaluate M1 Batch_Size')
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
'''