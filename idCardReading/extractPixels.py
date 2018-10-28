import cv2
import numpy as np

def setBrihtness(image,toBrihtness):
   gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

   brihtness = 0
   for column in gray:
      for row in column:
            brihtness += row
   brihtness = brihtness / gray.size / 255


   hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

   # print(brihtness) 

   changeToBrihtness = (brihtness - toBrihtness) * 255       

   if(changeToBrihtness < 0):
      changeToBrihtness *= -1
      hsv[:,:,2] += int(changeToBrihtness)
   else:
      hsv[:,:,2] -= int(changeToBrihtness)
            
   image = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

   return image

def extract_pixels(image,brihtness = 0.7):

      # image = cv2.resize(image, (1024,768))
    image = setBrihtness(image,brihtness)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    

    lower = np.array([0,0,0])  #-- Lower range --
    upper = np.array([115,255,165])  #-- Upper range --
    
    mask = cv2.inRange(hsv, lower, upper)

    return mask

