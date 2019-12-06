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

    def handle(self):
        if self.prediction == 'FIVE':
            pyautogui.press('up')

            # cv2.putText(crop_image, "JUMP", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
        if self.prediction == 'FOUR':
            pyautogui.press('down')
            # pyautogui.press('down')

        if self.prediction == 'ONE':
            pyautogui.press('left')

        if self.prediction == 'TWO':
            pyautogui.press('right')

        else:
            pyautogui.keyUp('down')

