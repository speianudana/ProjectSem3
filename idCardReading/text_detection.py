# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
from operator import itemgetter
from pygame import Rect

rW = 1
rH = 1

def changedWithRatioBox(box):	
	startX = int(box[0] * rW * 0.8) 
	startY = int(box[1] * rH * 1) 
	endX = int(box[2] * rW * 1.5) 
	endY = int(box[3] * rH * 1.1) 

	return (startX , startY , endX , endY)


def fromPointToRect(box):
	# pass
	return Rect(box[0],box[1],box[2] - box[0],box[3] - box[1])

def fromRectToPoints(rect):
	# pass
	return Rect(rect[0],rect[1],rect[2] + rect[0],rect[3] + rect[1])


def combine_all_rect(boxes):
	combinedBoxes = []

	foundIntersection = False
	ind = 0
	for i in range(0,len(boxes) - 1):
		box1 =	fromPointToRect(boxes[i])
		box2 = fromPointToRect(boxes[i + 1])
		ind += 1
		if box1.colliderect(box2) and not foundIntersection:
			foundIntersection = True
			newRect = box1.union(box2)
			boxCordinates = fromRectToPoints(newRect)

			combinedBoxes.append(boxCordinates)
			i += 2
			ind += 1
			break	
		else:
			combinedBoxes.append(fromRectToPoints(box1))

	for i in range(ind,len(boxes)):
		# print(i)
		combinedBoxes.append(boxes[i])
	# print(len(combinedBoxes))
	# print(counterSinceLastCombination)
	# combinedBoxes.append(boxes[len(boxes) - 1])
	
	return combinedBoxes, foundIntersection


def findTextLabels(image,neuralNetworkData = "frozen_east_text_detection.pb",minConfidence = 0.99,width = 352, height = 320):
	
	orig = image.copy()
	(H, W) = image.shape[:2]

	# set the new width and height and then determine the ratio in change
	# for both the width and height
	(newW, newH) = (width, height)
	global rW
	rW = W / float(newW)
	global rH
	rH = H / float(newH)


	# resize the image and grab the new image dimensions
	image = cv2.resize(image, (newW, newH))
	(H, W) = image.shape[:2]

	# define the two output layer names for the EAST detector model that
	# we are interested -- the first is the output probabilities and the
	# second can be used to derive the bounding box coordinates of text
	layerNames = [
		"feature_fusion/Conv_7/Sigmoid",
		"feature_fusion/concat_3"]

	# load the pre-trained EAST text detector
	print("[INFO] loading EAST text detector...")
	net = cv2.dnn.readNet(neuralNetworkData)

	# construct a blob from the image and then perform a forward pass of
	# the model to obtain the two output layer sets
	blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
		(123.68, 116.78, 103.94), swapRB=True, crop=False)
	start = time.time()
	net.setInput(blob)
	(scores, geometry) = net.forward(layerNames)
	end = time.time()

	# show timing information on text prediction
	print("[INFO] text detection took {:.6f} seconds".format(end - start))

	# grab the number of rows and columns from the scores volume, then
	# initialize our set of bounding box rectangles and corresponding
	# confidence scores
	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []

	# loop over the number of rows
	for y in range(0, numRows):
		# extract the scores (probabilities), followed by the geometrical
		# data used to derive potential bounding box coordinates that
		# surround text
		scoresData = scores[0, 0, y]
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]

		# loop over the number of columns
		for x in range(0, numCols):
			# if our score does not have sufficient probability, ignore it
			if scoresData[x] < minConfidence:
				continue

			# compute the offset factor as our resulting feature maps will
			# be 4x smaller than the input image
			(offsetX, offsetY) = (x * 4.0, y * 4.0)

			# extract the rotation angle for the prediction and then
			# compute the sin and cosine
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)

			# use the geometry volume to derive the width and height of
			# the bounding box
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]

			# compute both the starting and ending (x, y)-coordinates for
			# the text prediction bounding box
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			startX = int(endX - w)
			startY = int(endY - h)

			# add the bounding box coordinates and probability score to
			# our respective lists
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[x])

	# apply non-maxima suppression to suppress weak, overlapping bounding
	# boxes
	boxes = non_max_suppression(np.array(rects), probs=confidences)


	# loop over the bounding boxes

	lastStX , lastStY , lastEndX , lastEndY = (0 , 0 , 0 , 0)
	sortedBoxes = sorted(boxes,key=itemgetter(1))
	changedWithRatioBoxes = []

	for box in sortedBoxes:
		changedWithRatioBoxes.append(changedWithRatioBox(box))

	foundIntersection = True
	combinedBoxes = changedWithRatioBoxes

	while foundIntersection:
		combinedBoxes,foundIntersection = combine_all_rect(combinedBoxes)

		if(not foundIntersection):
			break


	for (startX, startY, endX, endY) in combinedBoxes:
		# scale the bounding box coordinates based on the respective
		cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
		

	# show the output image
	cv2.imshow("Text Detection", orig)
	cv2.waitKey(0)

	return combinedBoxes

image = cv2.imread("images/passport1.jpg")

# labels = findTextLabels(image)

# for label in labels:
	# print(label)
# load the input image and grab the image dimensions
