import cv2 
from pytesseract import image_to_string

image = cv2.imread("passport1.png")

small = cv2.resize(image, (1000,800))
# width , height = small.shape[:2]
# print(width)
# print(height)
# cv2.imshow("test1",small)
# cv2.waitKey(0)

idnp_img = small[120:160,0:400]
bloodType_img = small[200:240,0:400]
locationCity_img = small[290:350,0:400]
locationStreet1_img = small[340:390,0:350]
locationStreet2_img = small[340:390,350:700]
dateOfRegistration_img = small[450:500,0:400]

# new_img = small[0:600,0:400]
idnp = image_to_string(idnp_img,lang="ron")
bloodType  = image_to_string(bloodType_img)
locationCity = image_to_string(locationCity_img,lang="ron")
locationStreet = (image_to_string(locationStreet1_img,lang="ron") + image_to_string(locationStreet2_img,lang="ron"))

print("IDNP : " + idnp)
print("Blood Type : " + bloodType)
print("Location city : " + locationCity)
print("Location street : " + locationStreet)

# print(image_to_string(small,lang="ron"))
cv2.imshow("test",bloodType_img)
cv2.waitKey(0)