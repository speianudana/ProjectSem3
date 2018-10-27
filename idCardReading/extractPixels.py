import cv2
import numpy as np


def extract_pixels(image):
    # TO DO : Test different situation and select best values for any situation 
    lower_red = np.array([0,0,0])
    upper_red = np.array([115,255,150])

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_red , upper_red)
    # res = cv2.bitwise_and(frame,frame, mask = mask)


    # cv2.imshow('start',image)
    # cv2.imshow('mask',mask)
    # cv2.imwrite('img-in.png',mask)
    # cv2.waitKey(0)

    return mask