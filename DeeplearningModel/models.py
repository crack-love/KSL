from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D


def sl_model(weights_path=None):
    model = Sequential()
    model.add(ZeroPadding2D((1, 1), input_shape=(256, 24, 2)))
    model.add(Conv2D(16, (3, 1), activation="relu"))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(16, (3, 1), activation="relu"))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), data_format="channels_first"))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(32, (3, 1), activation="relu"))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(32, (3, 1), activation="relu"))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), data_format="channels_first"))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    # sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    if weights_path:
        model.load_weights(weights_path)

    return model


def sl_model_for_new_data(weights_path=None):
    model = Sequential()
    model.add(ZeroPadding2D((1, 1), input_shape=(76, 38, 2)))
    model.add(Conv2D(16, (3, 1), activation="relu"))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(16, (3, 1), activation="relu"))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), data_format="channels_first"))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(32, (3, 1), activation="relu"))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(32, (3, 1), activation="relu"))
    model.add(MaxPooling2D((2, 2), strides=(2, 2), data_format="channels_first"))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4, activation='softmax'))

    # sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    if weights_path:
        model.load_weights(weights_path)

    return model