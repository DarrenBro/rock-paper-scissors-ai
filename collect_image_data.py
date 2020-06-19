# Gather your own data images.
# Run command example: python collect_image_data.py rock 200
# Press 's' to start and q to quit.
# Images stored in 'collected_images' dir with label set as 1st argument

import cv2
import os
import sys

image_name = sys.argv[1]
sample_size = int(sys.argv[2])

IMAGE_SAVED_DIR = 'collected_images'
IMAGE_PATH = os.path.join(IMAGE_SAVED_DIR, image_name)

os.mkdir(IMAGE_PATH)

cap = cv2.VideoCapture(0)

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

    if start:
       roi = frame[100:500, 100:500]
       save_path = os.path.join(IMAGE_PATH, '{}.jpg'.format(count + 1))
       cv2.imwrite(save_path, roi)
       count += 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Capturing {}".format(count), (5, 50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Press 's' to start/pause. Press 'q' to quit", frame)

    k = cv2.waitKey(10)
    if k == ord('s'):
        start = True

    if k == ord('q'):
        break

print("\n{} Image(s) saved to {}".format(count, IMAGE_PATH))
cap.release()
cv2.destroyAllWindows()




