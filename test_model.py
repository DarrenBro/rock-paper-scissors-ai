# for loading already trained model into memory
from keras.models import load_model
# for loading images into memory
import cv2
import numpy as np
import sys

file_path = sys.argv[1]

INPUT_LABELS = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "background"
}


def map_index_to_label(index):
    return INPUT_LABELS[index]


# Change for your model name
model = load_model("example-rps-model-1.h5")

# prepare the image the same way it was in train_model
img = cv2.imread(file_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (300, 300))

# predict the move made
prediction = model.predict(np.array([img]))
move_index = np.argmax(prediction[0])
move_label = map_index_to_label(move_index)

print("Predicted the image is: {}".format(move_label))
