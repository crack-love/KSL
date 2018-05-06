from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
import os, sys
import dataFormater
from keras.utils import plot_model
import models as m 

m.getCurrentModel()
plot_model(model, to_file='model.png', show_shapes=True)