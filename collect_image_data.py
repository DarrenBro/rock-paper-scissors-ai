# Gather your own data images.
# Run command example: python collect_image_data.py rock 200
# Press 's' to start and q to quit.
# Images stored in 'collected_images' dir with label set as 1st argument

import cv2
import os
import sys

image_name = sys.argv[1]
data_size = int(sys.argv[2])

IMAGE_SAVED_DIR = 'collected_images'
IMAGE_PATH = os.path.join(IMAGE_SAVED_DIR, image_name)
os.mkdir(IMAGE_PATH)

cap = cv2.VideoCapture(0)
start = False
image_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    if image_count == data_size:
        break

    # (image, (x1, y1), (x2, y2), colour, thickness)
    # Makes a square by difference of 350-150 = 650-450
    cv2.rectangle(frame, (350, 150), (650, 450), (0, 0, 0))

    if start:
        roi = frame[150:450, 350:650]
        save_path = os.path.join(IMAGE_PATH, '{}.jpg'.format(image_count + 1))
        cv2.imwrite(save_path, roi)
        image_count += 1

    text_font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Press 's' to save images", (350, 500), text_font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Image count =  {}".format(image_count), (350, 530), text_font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Press 's' to start/pause.    Press 'q' to quit", frame)

    k = cv2.waitKey(10)
    if k == ord('s'):
        start = True

    if k == ord('q'):
        break

print("\n{} Image(s) saved to {}".format(image_count, IMAGE_PATH))
cap.release()
cv2.destroyAllWindows()
