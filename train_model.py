import cv2
import numpy as np
import tensorflow as tf
import os

from keras import Sequential
from keras.layers import Dropout, Convolution2D, Activation, GlobalAveragePooling2D
from keras_squeezenet import SqueezeNet

IMG_SAVE_PATH = 'collected_images'

# Lets have our label inputs map to index values as that's how the NN will identify them
INPUT_LABELS = {
    "rock": 0,
    "paper": 1,
    "scissors": 2,
    "background": 3
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
        SqueezeNet(input_shape=(227, 227, 3), include_top=False),
        # To prevent over-fitting, 20% dropout rate
        Dropout(0.2),
        # Add this layer to end of Squeeze NN
        Convolution2D(LABELS_COUNT, (1, 1), padding='valid'),
        Activation('relu'),
        # Perform classification, calculates average output of each feature map in previous layer
        # i.e data reduction layer, prepares model for Activation('softmax')
        GlobalAveragePooling2D(),
        # softmax give probabilities of each hand sign
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
        img = cv2.resize(img, (227, 227))
        dataset.append([img, directory])

data, labels = zip(*dataset)
labels = list(map(map_label_to_index, labels))

















