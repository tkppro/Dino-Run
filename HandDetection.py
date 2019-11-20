from threading import Thread
import cv2
import numpy as np
import pyautogui
import math

class HandDetection():
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, crop_image=None):
        self.crop_image = crop_image
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            print("detect: ", self.crop_image)
            blur = cv2.GaussianBlur(self.crop_image, (3, 3), 0)
            # Change color-space from BGR -> HSV
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

            # Create a binary image with where white will be skin colors and rest is black
            mask2 = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 255, 255]))

            # Kernel for morphological transformation
            kernel = np.ones((5, 5))

            # Apply morphological transformations to filter out the background noise
            dilation = cv2.dilate(mask2, kernel, iterations=1)
            erosion = cv2.erode(dilation, kernel, iterations=1)

            # Apply Gaussian Blur and Threshold
            filtered = cv2.GaussianBlur(erosion, (3, 3), 0)
            ret, thresh = cv2.threshold(filtered, 127, 255, 0)

            # Find contours
            contours, image = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            try:
                # Find contour with maximum area
                contour = max(contours, key=lambda x: cv2.contourArea(x))

                # Create bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)
                # cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)

                # Find convex hull
                hull = cv2.convexHull(contour)

                # Draw contour
                drawing = np.zeros(self.crop_image.shape, np.uint8)
                cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
                cv2.drawContours(drawing, [hull], -1, (0, 0, 255), 0)

                # Fi convexity defects
                hull = cv2.convexHull(contour, returnPoints=False)
                defects = cv2.convexityDefects(contour, hull)

                # Use cosine rule to find angle of the far point from the start and end point i.e. the convex points (the finger
                # tips) for all defects

                count_defects = 0
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(contour[s][0])
                    end = tuple(contour[e][0])
                    far = tuple(contour[f][0])

                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

                    # if angle >= 90 draw a circle at the far point
                    if angle <= 90:
                        count_defects += 1
                        cv2.circle(self.crop_image, far, 1, [0, 0, 255], -1)

                    cv2.line(self.crop_image, start, end, [0, 255, 0], 2)
                # Press SPACE if condition is match
                print("count defect: ", count_defects)
                # if count_defects >= 4:
                #     pyautogui.press('up')
                #     pyautogui.keyUp('down')
                #     cv2.putText(frame, "JUMP", (1000, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
                # if count_defects >= 1 and count_defects < 2:
                #     pyautogui.keyDown('down')
                #     # pyautogui.press('down')
                #     cv2.putText(frame, "DOWN", (1000, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)
            except:
                pass

    def stop(self):
        self.stopped = True

    def handle(self,crop_image):
        print("Test",crop_image)
        # cv2.imread("Video", crop_image)
        # Apply Gaussian blur
        # blur = cv2.GaussianBlur(crop_image, (3, 3), 0)
        cv2.imshow("Image", crop_image)

        if cv2.waitKey(1) == ord("q"):
            self.stopped = True



