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

import tensorflow as tf
from keras import backend as K
util.showProcess('Loading TF Session')
sess = tf.Session()
K.set_session(sess)
from keras.preprocessing.image import ImageDataGenerator

DATASET_PATH_TRAIN = '../data/ConvLSTM/train'
DATASET_PATH_TEST = '../data/ConvLSTM/test'
IMAGE_SIZE    = (80, 80)
BATCH_SIZE    = 5
NUM_EPOCHS    = util.inputInt('How many epochs?')
isLoadWeight = util.inputInt('Load weight? (1 to yes)')
overwrite = True
sampleSize_train = len(df.getSamplePathList(DATASET_PATH_TRAIN))
sampleSize_test = len(df.getSamplePathList(DATASET_PATH_TEST))
util.showDivisionSingle()
print('train: ' + str(sampleSize_train))
print('test: ' + str(sampleSize_test))

train_imgGen = ImageDataGenerator(
    #preprocessing_function=preprocess_input,
    #rescale=1./255,
    rotation_range=22,
    shear_range=3,
    zoom_range=0.2,
    width_shift_range=0.18,
    height_shift_range=0.18,
    channel_shift_range=5,
    #vertical_flip=False,
    #horizontal_flip=False,
    fill_mode='nearest'
)
    
test_imgGen = ImageDataGenerator(
    #rescale = 1./255
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
'''
util.showProcess('Class indices')
for cls, idx in train_batchIter.class_indices.items():
    print('Class #{} = {}'.format(idx, cls))
'''
# write data plot graph
dp.plotSpointDataList(Path.get('train'), 2, 2, False, Path.get('img') + '\\d_graph')
dp.plotSpointDataList(Path.get('train'), 2, 2, True, Path.get('img') + '\\d_image')

# make model, b1/b2는 구조 print용
util.showProcess('Model Generating')
model = models.Model_B2_FT(IMAGE_SIZE + (3,))

# plot to file
models.saveModelDescription(model, Path.get('img'), False)

# Load Weight
if isLoadWeight == 1:
    util.showProcess('Loading Weight')
    models.loadWeight(model, Path.get('weight'))

# Train
util.showProcess('Train')
model.fit_generator(
    train_batchIter,
    steps_per_epoch=sampleSize_train/BATCH_SIZE,
    epochs=NUM_EPOCHS,
    validation_data=test_batchIter,
    validation_steps=sampleSize_test/BATCH_SIZE,
    max_queue_size=10,
)

#Predict
util.showProcess('Predict')
array = model.predict_generator(
    test_batchIter,
    steps=sampleSize_test/BATCH_SIZE,
    verbose=1,
)

acc = train.calcurateAcc(array, test_batchIter)
print('acc : ' + str(acc))

# Write Weight
if overwrite:
    util.showProcess('Saving Weight')
    models.saveWeight(model, Path.get('weight'))

sess.close()