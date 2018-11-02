import cv2
import numpy as np

def setBrightness(image,toBrightness):
   gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

   brightness = 0
   for column in gray:
      for row in column:
            brightness += row
   brightness = brightness / gray.size / 255


   hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

   # print(brightness) 

   changeToBrightness = (brightness - toBrightness) * 255       

   if(changeToBrightness < 0):
      changeToBrightness *= -1
      hsv[:,:,2] += int(changeToBrightness)
   else:
      hsv[:,:,2] -= int(changeToBrightness)
            
   image = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

   return image

def extract_pixels(image,brightness = 0.6):

#     image = setBrightness(image,brightness)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    

    lower = np.array([0,0,0])  #-- Lower range --
    upper = np.array([255,255,130])  #-- Upper range --
    
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(image, image, mask=mask)

    return mask

# image = cv2.imread("images/passport.jpg")

# new_img = extract_pixels(image)

# cv2.imshow("dsadas",new_img)
# cv2.waitKey(0)
# cv2.imwrite("extractedPixels.jpg",new_img)