from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Model
from keras.layers import *
from keras.optimizers import Adam
from keras.applications.xception import Xception, preprocess_input
from keras.utils import plot_model # for model description png

DATASET_PATH  = '../data/catvsdog'
IMAGE_SIZE    = (299, 299)
NUM_CLASSES   = 2
BATCH_SIZE    = 8  # try reducing batch size or freeze more layers if your GPU runs out of memory
FREEZE_LAYERS = 2  # freeze the first this many layers for training
NUM_EPOCHS    = 20
WEIGHTS_FINAL = 'model_fine-tuning_xception.h5'

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    #rescale=1./255,
    rotation_range=40,
    shear_range=0.2,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    channel_shift_range=8,
    #vertical_flip=True,
    horizontal_flip=True,
    fill_mode='nearest',
    )

train_batches = train_datagen.flow_from_directory(
    DATASET_PATH + '/train',
    target_size=IMAGE_SIZE,
    interpolation='bicubic',
    class_mode='categorical',
    shuffle=True,
    batch_size=BATCH_SIZE,    
)

test_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
)

test_batches = test_datagen.flow_from_directory(
    DATASET_PATH + '/test',
    target_size=IMAGE_SIZE,
    interpolation='bicubic',
    class_mode='categorical',
    shuffle=False,
    batch_size=BATCH_SIZE,
)

# show class indices
print('****************')
for cls, idx in train_batches.class_indices.items():
    print('Class #{} = {}'.format(idx, cls))
print('****************')

net = Xception(
    include_top=False,
    weights='imagenet',
    input_tensor=None,
    input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3),
    )

x = net.output
#x = Flatten()(x)
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Activation('relu')(x)
x = Dense(1000)(x)
x = BatchNormalization()(x)
x = Activation('relu')(x)
x = Dense(1000)(x)
x = BatchNormalization()(x)
x = Activation('relu')(x)
xo = Dense(NUM_CLASSES, activation='softmax', name='softmax')(x)
model = Model(inputs=net.input, outputs=xo)

plot_model(model, to_file='plot.jpg', show_layer_names=True, show_shapes=True)

i = 0
print(len(model.layers))
for layer in model.layers:
    i += 1
    layer.trainable = False
    if i >= 133:
        layer.trainable = True
    print(str(i) + ': ' + str(layer) + ' ' + str(layer.trainable))

model.compile(
    optimizer=Adam(lr=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
    )

model.fit_generator(
    train_batches,
    steps_per_epoch=train_batches.samples/BATCH_SIZE,
    epochs=NUM_EPOCHS,
    validation_data=test_batches,
    validation_steps=test_batches.samples/BATCH_SIZE,
    #use_multiprocessing=False,

)

model.save_weights(WEIGHTS_FINAL)