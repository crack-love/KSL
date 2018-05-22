import keras
from keras.layers import Input ,Dense, Dropout, Activation, LSTM
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Reshape
from keras.models import Sequential
from keras.layers.wrappers import TimeDistributed
from keras.layers.pooling import GlobalAveragePooling1D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.models import Model

import numpy as np

timesteps=100
number_of_samples=2500
frame_row=32
frame_col=32
channels=3

nb_epoch=1
batch_size=timesteps

data= np.random.random((number_of_samples, timesteps, frame_row, frame_col, channels))
label=np.random.random((number_of_samples, 1))

X_train=data[0:2000,:]
y_train=label[0:2000]

X_test=data[2000:,:]
y_test=label[2000:,:]

#%%

model=Sequential()

model.add(TimeDistributed(Convolution2D(32, 3, 3, border_mode='same'), input_shape=X_train.shape[1:]))
model.add(TimeDistributed(Activation('relu')))
model.add(TimeDistributed(Convolution2D(32, 3, 3)))
model.add(TimeDistributed(Activation('relu')))
model.add(TimeDistributed(MaxPooling2D(pool_size=(2, 2))))
model.add(TimeDistributed(Dropout(0.25)))

model.add(TimeDistributed(Flatten()))
model.add(TimeDistributed(Dense(512)))
                
                
model.add(TimeDistributed(Dense(35, name="first_dense" )))
        
model.add(LSTM(20, return_sequences=True, name="lstm_layer"))
         
#%%
model.add(TimeDistributed(Dense(1), name="time_distr_dense_one"))
model.add(GlobalAveragePooling1D(name="global_avg"))

#%%

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X_train, y_train,
          batch_size=batch_size,
          nb_epoch=nb_epoch,
          validation_data=(X_test, y_test))

model.layers[0].output.shape
#TensorShape([Dimension(None), Dimension(100), Dimension(32), Dimension(32), Dimension(32)])