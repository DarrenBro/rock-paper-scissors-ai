# for loading already trained model into memory
from keras.models import load_model
# for loading images into memory
import cv2
import numpy as np
import sys

file_path = sys.argv[1]

# Reverse of INPUT_LABELS in train_model.py
LABELS_INPUT = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "noise"
}


def map_index_to_label(index):
    return LABELS_INPUT[index]


# Change for your model name
model = load_model("example-rps-model-1.h5")
# model = load_model("rps-model-2.h5")

# Prepare the image the same way it was in train_model
img = cv2.imread(file_path)

# When the image file is read with OpenCV, the order of colors is BGR (blue, green, red)
# But the order of colors is assumed to be RGB (red, green, blue)
# Must convert for numpy to use.
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Match img (image) resolution that was captured and trained under
img = cv2.resize(img, (300, 300))

# Predict the image given
prediction = model.predict(np.array([img]))
# Simply printing the prediction returns below weights against index matching against the labels
# Not very readable but here kept it if interested
# This was the result of test_images/none.jpg (index 3)
# [[3.1004856e-05 2.6356198e-05 1.8926119e-05 9.9992371e-01]]
# print(prediction)

# So return the index of the largest value and map
move_index = np.argmax(prediction[0])
move_label = map_index_to_label(move_index)

print("Predicted the image is: {}".format(move_label))
