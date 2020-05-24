import cv2, time
import os
import numpy as np
import time


# class CameraImporter:
#     def cature(self):
#         cap = cv2.VideoCapture(0)
#         img_counter = 0
#         directory = os.path.dirname(os.path.realpath(__file__)) + '/cameraimpord/'
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#
#         while True:
#             ret, frame = cap.read()
#             cv2.imshow('video capture frame', frame)
#
#             img_name = "opencv_frame_{}.png".format(img_counter)
#             cv2.imwrite(os.path.join(directory, img_name), frame)
#             img_counter = img_counter + 1
#             time.sleep(2)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#
#         cap.release()
#         cv2.destroyAllWindows()