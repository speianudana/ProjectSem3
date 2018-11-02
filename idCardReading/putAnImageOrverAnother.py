import cv2
import numpy as np
from extractPixels import extract_pixels

background = cv2.imread("images/passport.jpg")
background = cv2.resize(background, (1024,768))
# cv2.imwrite("images/passportTest.jpg",background)
overlay = cv2.imread("images/02_black.png")
overlay = cv2.resize(overlay, (1024,768))

added_image = cv2.addWeighted(background,1,overlay,1,0)

hsv = cv2.cvtColor(added_image,cv2.COLOR_BGR2HSV)

hsv[:,:,1] = 0

added_image = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

out = extract_pixels(added_image)

cv2.imwrite('images/combined.png', out)
# cv2.imshow("seturated",added_image)
# cv2.imshow("contrasted",added_image)
# cv2.waitKey(0)
