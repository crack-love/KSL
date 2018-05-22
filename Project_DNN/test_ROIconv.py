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

import keras
from keras.models import Model
from keras.layers import Conv2D, Dense, LSTM, Flatten, Input, \
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

spointData, imageList, labelOneHot = \
    df.ROI_loadSingleDataFromDir(path.get('data') + "\\0_안녕하세요\\2018-05-20_184707_kyg", True)

'''
x_train, y_train = df.ROI_loadSingleImages(path.get('data') + '\\SingleImage_train', True)
x_test, y_test = df.ROI_loadSingleImages(path.get('data') + '\\SingleImage_test', True)
'''
# branch 1 (it will be spoint cnn branch)
#branch1 = Sequential()

# branch 2 (roi cnn+lstm branch)
branch2_input = Input(shape=(76, 128, 128, 3), name='B2I') # 76 sequence
x = TimeDistributed(Dropout(0.2))(branch2_input)
for i in range(2): # 필터 개수를 늘리면 GPU 메모리 부족..
    x = TimeDistributed(Conv2D(filters=16,
               kernel_size=3,
               strides=1,
               padding='same',
               data_format='channels_last', name='B2C_' + str(i)))(x)
    x = add_BatchNormal_Activation_Dropout(x)

#flatten? here?

# branch 2 lstm
# The input to an LSTM layer must have samples of shape (nb_timesteps, nb_features).
#x = LSTM(2, )(x)

x = TimeDistributed(Flatten())(x)
x = TimeDistributed(Dense(256))(x)
x = add_BatchNormal_Activation_Dropout(x)
x = TimeDistributed(Dense(128))(x)
x = add_BatchNormal_Activation_Dropout(x)

predictions = TimeDistributed(Dense(2, activation='softmax'))(x)

model = Model(inputs=branch2_input, outputs=predictions)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

model.fit(imageList, labelOneHot, epochs=epochs, verbose=1, batch_size=20)

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