import imutils
import cv2 
from extractPixels import extract_pixels
image = cv2.imread('images/passportFromPhone.jpg')
rotated = imutils.rotate_bound(image,270)
small = cv2.resize(rotated, (1150, 850))  

edged = cv2.Canny(small, 10, 200)

(_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_CCOMP  , cv2.CHAIN_APPROX_TC89_L1  )
ind = 0

for c in cnts:
	x,y,w,h = cv2.boundingRect(c)
	if w>300 and h>200:
		ind += 1
		new_img = small[y:y+h,x:x+w]		
		new_img = extract_pixels(new_img)
		cv2.imwrite("images/passport" + '.jpg', new_img)

		
