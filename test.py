import argparse
import cv2
import pyautogui
import copy
import numpy as np
from VideoGet import VideoGet
from VideoShow import VideoShow
from FingerDetection import *
from KeyListener import *

x0, y0, width = 300, 180, 300
x1, y1 = 0, 0
font = cv2.FONT_HERSHEY_SIMPLEX
fx, fy, fh = 10, 50, 45

def handDetect(frame, prediction, x, y):
    """
    Add iterations per second text to lower-left corner of a frame.
    """
    cv2.putText(frame, '%s' % (prediction), (x+10,y+50), font, 1.0, (245, 210, 65), 2, 1)
    return prediction



def binaryMask(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7,7), 3)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    ret, new = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return new

def normalizeFrame(frame, x, y):

    roi = frame[y:y + width, x:x + width]
    roi = binaryMask(roi)

    img = np.float32(roi) / 255.
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)

    return img

def drawDetectionArea(frame, x, y, width, color):
    cv2.rectangle(frame, (x, y), (x + width - 1, y + width - 1), color, 12)
    return frame

def main():
    finger_detect = FingerDetection().start()
    key_listener = KeyListener().start()
    video_getter = VideoGet(0).start()
    video_shower = VideoShow(video_getter.frame).start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = cv2.flip(frame, 1)
        img = normalizeFrame(frame, x0, y0)
        frame = drawDetectionArea(frame,x0,y0,width,(0,255,0))
        cv2.putText(frame, "NONE = NONE, ONE = LEFT", (0, 80), font, 1.0, (0, 0, 255), 2, 1)
        cv2.putText(frame, "TWO = RIGHT, DOWN = FOUR", (0, 120), font, 1.0,
                    (0, 0, 255), 2, 1)
        cv2.putText(frame, "UP = FIVE", (0, 160), font, 1.0,
                    (0, 0, 255), 2, 1)
        finger_detect.frame = img
        prediction = handDetect(frame, finger_detect.detect(),x0,y0)

        # if prediction == "NONE" or prediction == "FIVE":
        key_listener.prediction = prediction
        key_listener.handle()

        video_shower.frame = frame

if __name__ == "__main__":
    main()