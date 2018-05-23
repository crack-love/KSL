'''
 손가락 예측 모델
 128x128 3channel 76장 * 2(왼/오) sequential 이미지 입력
 CNN + LSTM
'''
import PYTHONPATH
import scripts.dataFormater as df
import scripts.paths as path
import scripts.interfaceUtils as util
import scripts.models as models
import scripts.train as train

## keras import
import keras
from keras.models import Model
from keras.layers import Conv2D, Dense, LSTM, Flatten, Input, CuDNNLSTM, \
Activation, Dropout, BatchNormalization, TimeDistributed

def add_BatchNormal_Activation_Dropout(x):
    x = TimeDistributed(BatchNormalization())(x)
    x = TimeDistributed(Activation('relu'))(x)
    x = TimeDistributed(Dropout(0.3))(x)
    return x    

# input epochs
util.showDivisionSingle()
epochs = int(util.input('How many epochs?'))

# load path
trainDataPath = path.get('TRAIN')
testDataPath = path.get('TEST')
weightPath = path.get('WEIGHT')

# load dataset
util.showProcess('Loading dataset')
dirPath_train = path.get('data') + '\\ConvLSTM_train'
dirPath_test = path.get('data') + '\\ConvLSTM_test'
samplePathList_train = df.ROI_loadAllSamplePaths(dirPath_train)
samplePathList_test = df.ROI_loadAllSamplePaths(dirPath_test)

spointList_train, roiSampleList_train, labelList_train = \
    df.ROI_loadDataList(samplePathList_train, True)
spointList_test, roiSampleList_test, labelList_test = \
    df.ROI_loadDataList(samplePathList_test, True)

# branch 1 (it will be spoint cnn branch)


# branch 2 (roi cnn+lstm branch)
branch2_input = Input(shape=(100, 80, 80, 3), name='B2I')
x = TimeDistributed(Conv2D(filters=16,
                            kernel_size=3,
                            strides=1,
                            padding='same',
                            data_format='channels_last',
                            name='B2C'), name='TD_Conv2D_1')(branch2_input)
x = TimeDistributed(BatchNormalization(), name='TD_Conv2D_1_BN')(x)
x = TimeDistributed(Activation('relu'), name='TD_Conv2D_1_AC')(x)
x = TimeDistributed(Dropout(0.3), name='TD_Conv2D_1_DO')(x)

x = TimeDistributed(Conv2D(filters=16,
                            kernel_size=3,
                            strides=1,
                            padding='same',
                            data_format='channels_last',
                            name='B2C'), name='TD_Conv2D_2')(x)
x = TimeDistributed(BatchNormalization(), name='TD_Conv2D_2_BN')(x)
x = TimeDistributed(Activation('relu'), name='TD_Conv2D_2_AC')(x)
x = TimeDistributed(Dropout(0.3), name='TD_Conv2D_2_DO')(x)

x = TimeDistributed(Flatten(), name='TD_Flatten')(x)
x = TimeDistributed(BatchNormalization(), name='TD_Flatten_BN')(x)
x = TimeDistributed(Activation('relu'), name='TD_Flatten_AC')(x)
x = TimeDistributed(Dropout(0.3), name='TD_Flatten_DO')(x)
x = TimeDistributed(Dense(128), name='TD_Dense_1')(x)
x = TimeDistributed(BatchNormalization(), name='TD_Dense_1_BN')(x)
x = TimeDistributed(Activation('relu'), name='TD_Dense_1_AC')(x)
x = TimeDistributed(Dropout(0.3), name='TD_Dense_1_DO')(x)
x = TimeDistributed(Dense(64), name='TD_Dense_2')(x)
x = TimeDistributed(BatchNormalization(), name='TD_Dense_2_BN')(x)
x = TimeDistributed(Activation('relu'), name='TD_Dense_2_AC')(x)
x = TimeDistributed(Dropout(0.3), name='TD_Dense_2_DO')(x)

x = LSTM(20, dropout=0.3,
             activation='relu',
             name='LSTM_1')(x)

x = Dense(32, name='Dense_1')(x)
x = BatchNormalization(name='Dense_1_BN')(x)
x = Activation('relu', name='Dense_1_AC')(x)
x = Dropout(0.3, name='Dense_1_DO')(x)
predictions = Dense(5, activation='softmax', name='Softmax')(x)

model = Model(inputs=branch2_input, outputs=predictions)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

while (True):
    yes = util.input('load weight? (y/n)')
    if yes=='y':
        model.load_weights(path.get('data') + '\\roiTempModel.h5')
        break
    if yes=='n':
        break

# Merge

# Train
util.showProcess('Train')
model.fit(roiSampleList_train, labelList_train, shuffle=True, epochs=epochs, verbose=1, batch_size=3)

# Prediction
util.showProcess('Prediction')
accuracy = train.calculateAccuracy(roiSampleList_test, labelList_test, model, verbose=1, batch_size=3)
print('Accuracy: ' + str(accuracy))

model.save(path.get('data') + '\\roiTempModel.h5')

#accuracy = train.calculateAccuracy(x_test, y_test, model, 2)
#print('Accuracy : ' + str(accuracy))

# model
#x = keras.layers.concatenate([l1, l2])
#model = Model(inputs=[main_input, auxiliary_input], outputs=[main_output, auxiliary_output])
#model.compile(loss='', optimizer='',
#loss_weights={'main_output': 1., 'aux_output': 0.2})
#model.fit({'main_input': headline_data, 'aux_input': additional_data},
          #{'main_output': labels, 'aux_output': labels},
          #epochs=50, batch_size=32)

'''
# load model input -> cnn -> lstm -> dnn
util.showProcess('Loading model')

model = Sequential()
model.add(Conv2D)

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


# train
util.showProcess('Train Start')
#print('BATCH_SIZE: ' + str(BATCH_SIZE))
#train.train(trainDatas, trainLabels, model, epoch, BATCH_SIZE)

model.fit(X, y, epochs=n_epoch, batch_size=n_batch, verbose=2)
# evaluate
result = model.predict(X, batch_size=n_batch, verbose=0)

# result
print('Evaluate Accuracy')
#accuracy = train.calculateAccuracy(trainDatas, trainLabels, model, 0)
#print("Accuracy TRAIN: " + str(accuracy))
#accuracy = train.calculateAccuracy(testDatas, testLabels, model, 0)
#print("Accuracy TEST: " + str(accuracy))

# save
util.showProcess('Saving Weight')
#models.saveModel(model, weightPath)

print('Complete')

'''