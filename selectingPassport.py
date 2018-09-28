import cv2 
image = cv2.imread("myimage.jpg")
small = cv2.resize(image, (1000, 800))  

edged = cv2.Canny(small, 10, 200)
(_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_CCOMP  , cv2.CHAIN_APPROX_TC89_L1  )
# ind = 0
for c in cnts:
	x,y,w,h = cv2.boundingRect(c)
	if w>400 and h>300:
		new_img=small[y:y+h,x:x+w]		
		# ind += 1
		cv2.imwrite(str("passport" + str(ind)) + '.png', new_img)

