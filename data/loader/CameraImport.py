import cv2, time
import os
import numpy as np
import time


cap = cv2.VideoCapture(0)
img_counter = 0
directory = os.path.dirname(os.path.realpath(__file__)) + '/cameraimpord/'
if not os.path.exists(directory):
    os.makedirs(directory)

while True:
    ret, frame = cap.read()
    cv2.imshow('video capture frame', frame)

    img_name = "opencv_frame_{}.png".format(img_counter)
    cv2.imwrite(os.path.join(directory, img_name), frame)
    img_counter = img_counter + 1
    time.sleep(2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# cam = cv2.VideoCapture(0)
#
# cv2.namedWindow("test")
#
# img_counter = 0
#
# while True:
#     ret, frame = cam.read()
#     cv2.imshow("test", frame)
#     if not ret:
#         break
#     k = cv2.waitKey(1)
#
#     if k%256 == 27:
#         # ESC pressed
#         print("Escape hit, closing...")
#         break
#     elif k%256 == 32:
#         # SPACE pressed
#         img_name = "opencv_frame_{}.png".format(img_counter)
#         cv2.imwrite(img_name, frame)
#         print("{} written!".format(img_name))
#         img_counter += 1
#
# cam.release()
#
# cv2.destroyAllWindows()