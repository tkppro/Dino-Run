
# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
from VideoShow import *
from HandDetection import *
import cv2
# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")

cap = cv2.VideoCapture(0)
(grabbed, frame) = cap.read()
video_shower = VideoShow(frame).start()
hand_detection = HandDetection(frame).start()

width = 1366
height = 500

width1 = 500
height2 = 500
# cps = CountsPerSec().start()

# loop over some frames...this time using the threaded stream
while True:
        (grabbed, frame) = cap.read()
        if not grabbed or video_shower.stopped or hand_detection.stopped:
            video_shower.stop()
            hand_detection.stop()
            break
        frame = imutils.resize(frame, width=1500)
        frame = cv2.flip(frame, 1)
        cv2.rectangle(frame, (866, 0), (width, height), (0, 255, 0), 5)
        cv2.rectangle(frame, (0, 0), (width1, height2), (0, 0, 255), 5)
        crop_image = frame[0:height, 866:width]

        # frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        hand_detection.crop_image = crop_image

        # cps.increment()

# stop the timer and display FPS information


# do a bit of cleanup
cap.release()
cv2.destroyAllWindows()
