import cv2
import numpy as np
import tensorflow as tf
import os

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
