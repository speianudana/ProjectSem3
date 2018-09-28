from skimage.measure import compare_ssim
import argparse
import imutils
import cv2

imageA = cv2.imread("passport1.png")
imageA = cv2.resize(imageA,(1000,800))
imageB = cv2.imread("passport2.png")
imageB = cv2.resize(imageB,(1000,800))

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))