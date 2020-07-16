from keras.models import Sequential
from keras.layers import Dropout, Convolution2D, Activation, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from keras_squeezenet import SqueezeNet

import cv2
import numpy as np
import os

IMG_SAVE_PATH = 'collected_images'

# Lets have our label inputs map to index values as that's how the NN will identify them
INPUT_LABELS = {
    "rock": 0,
    "paper": 1,
    "scissors": 2,
    "noise": 3
}

LABELS_COUNT = len(INPUT_LABELS)


# Map label value to index
def map_label_to_index(index):
    return INPUT_LABELS[index]

# Might need to prepare images if not already handled in collect images
# def prepare_image(image, target):
#     # if the image mode is not RGB, convert it
#     if image.mode != "RGB":
#         image = image.convert("RGB")
#
#     # resize the input image and preprocess it
#     image = image.resize(target)
#     image = img_to_array(image)
#     image = np.expand_dims(image, axis=0)
#     image = imagenet_utils.preprocess_input(image)
#
#     # return the processed image
#     return image


# Pass SqueezeNet Neural Network into Keras Sequential Model
def train_model():
    model = Sequential([
        # image size is 227 x 227 pixels. 3 is for RGB
        # Include_top lets you select if you want the final dense layers or not
        # Dense layers are capable of interpreting found patterns in order to classify: e.g. this image contains rock
        # Set to False as we have labeled what rock data looks like already
        SqueezeNet(input_shape=(300, 300, 3), include_top=False),
        # To prevent over-fitting, 20% dropout rate
        Dropout(0.2),
        # Add this layer to end of Squeeze NN
        Convolution2D(LABELS_COUNT, (1, 1), padding='valid'),
        # Any negative values become 0 and keeps positive values
        # Why? Has become the default activation function for many types of neural networks because a model that uses
        # it is easier to train and often achieves better performance.
        Activation('relu'),
        # Perform classification, calculates average output of each feature map in previous layer
        # i.e data reduction layer, prepares model for Activation('softmax')
        GlobalAveragePooling2D(),
        # softmax give probabilities of each hand sign
        # 4 image class (problem), 'softmax' handles multi-class, anything more than 2
        Activation('softmax')
    ])
    return model


# load images from the directory
dataset = []
for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join(IMG_SAVE_PATH, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        # to make sure no hidden files get in our way
        if item.startswith("."):
            continue
        img = cv2.imread(os.path.join(path, item))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300, 300))
        dataset.append([img, directory])

# unpack dataset to get into a single array
# image data will be in 'data', labels in 'labels'
# e.g => dataset = [
#     [[image], 'label(rock)']
# ]

data, labels = zip(*dataset)
# map string labels to index values
labels = list(map(map_label_to_index, labels))

# labels: rock,paper,paper,scissors,rock
# example: [1,0,0], [0,1,0], [0,1,0], [0,0,1], [1,0,0]

# one hot encode the labels
labels = np_utils.to_categorical(labels)

# define the model
model = train_model()
model.compile(
    optimizer=Adam(lr=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# start training
model.fit(np.array(data), np.array(labels), epochs=10)

# save the model
model.save("rps-model-2.h5")
