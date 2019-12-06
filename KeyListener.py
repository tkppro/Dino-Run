from threading import Thread

import cv2
import numpy as np
import copy
import math
import pyautogui
import time

pyautogui.PAUSE = 0.1
class KeyListener():
    def __init__(self):
        self.prediction = "A"

    def start(self):

        return self

    def handle(self, up, down):
        if self.prediction == 'FIVE':
            pyautogui.press(up)
            print('up')
            pyautogui.keyUp(down)
            # time.sleep(1)

            # cv2.putText(crop_image, "JUMP", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        if self.prediction == 'NONE':
            pyautogui.keyDown(down)
            print('down')
            # pyautogui.press('down')
        else:
            pyautogui.keyUp(down)
