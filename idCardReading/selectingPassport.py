import imutils
import cv2 
import numpy as np
from objectDetection import *

def changeToPerspective(image,points):
	# points)
	pts1 = np.float32([points[0],points[3],points[1],points[2]])
	pts2 = np.float32([[0,0],[1024,0],[0,768],[1024,768]])
	M = cv2.getPerspectiveTransform(pts1,pts2)
	new_img = cv2.warpPerspective(small,M,(1024,768))
	return new_img

image = cv2.imread('images/passportFromPhone.jpg')

h,w,_ = image.shape

if h > w:
	rotated = imutils.rotate_bound(image,270)
else:
	rotated = image

small = cv2.resize(rotated, (1024, 768))


typeOfPassport = "buletinBack"
points,_ = objectDetection(small,initObjDetection(cv2.imread("images/buletinBackTemplate.jpg")))

'''
if len(points) <= 0:
	points,_ = objectDetection(small,initObjDetection(cv2.imread("images/buletinFaceTemplate.jpg")))
	typeOfPassport = "buletinBack"
	if len(points) <= 0 :
		points,_ = objectDetection(small,initObjDetection(cv2.imread("images/passportDocument.jpg")))
		typeOfPassport = "buletinBack"
		if len(points) <= 0:
			print("NO PASSPORT OR BULETIN ON PHOTO")
'''
			
small = changeToPerspective(small,points)

# Get rid of pdf417 code
small[0 : int(768 / 3) , int(1024 / 2.2) : 1024] = 0
# new_img[int(h * 2 / 3) : h , 0 : w] = 0

cv2.imwrite("images/passport" + '.jpg', small)

		
