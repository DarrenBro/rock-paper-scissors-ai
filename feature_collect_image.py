# Gather your own data images.
# Run command example: python collect_image_data.py rock 200
# Press 's' to start/pause and q to quit.
# Images stored in 'collected_images' dir with label set as 1st argument
import numpy as np
import cv2
import os
import sys
image_name = sys.argv[1]
sample_size = int(sys.argv[2])
IMAGE_SAVED_DIR = 'collected_images'
IMAGE_PATH = os.path.join(IMAGE_SAVED_DIR, image_name)
os.makedirs(IMAGE_PATH, exist_ok=True)
cap = cv2.VideoCapture(0)
lower = np.array([0, 34, 56], dtype="uint8")
upper = np.array([20, 255, 255], dtype="uint8")
start = False
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    if count == sample_size:
        break
    # image, then pt1, pt2, colour, thickness
    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
    # build skin mask
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skin_mask = cv2.inRange(hsv_frame, lower, upper)
    # mask manipulation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    skin_mask = cv2.erode(skin_mask, kernel, iterations=2)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=1)
    # add blur to mask to reduce noise
    skin_mask = cv2.GaussianBlur(skin_mask, (7, 7), 0)
    # create skin-only frame
    skin_frame = cv2.bitwise_and(frame, frame, mask=skin_mask)
    if start:
        roi = skin_mask[100:500, 100:500]
        save_path = os.path.join(IMAGE_PATH, '{}.jpg'.format(count + 1))
        cv2.imwrite(save_path, roi)
        count += 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(skin_mask, "Capturing {}".format(count), (5, 50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Press 's' to start/pause. Press 'q' to quit", skin_frame)
    k = cv2.waitKey(10)
    if k == ord('s'):
        start = True
    if k == ord('q'):
        break
print("\n{} Image(s) saved to {}".format(count, IMAGE_PATH))
cap.release()
cv2.destroyAllWindows()