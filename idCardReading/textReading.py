import os
import cv2 
from pytesseract import image_to_string
from text_detection import findTextLabels
from extractPixels import extract_pixels

small = cv2.imread("images/combined" + '.png')

# small = cv2.resize(image, (1024,768))

blackTextImage = extract_pixels(small)
# cv2.imshow("test",blackTextImage)
# cv2.waitKey(0)
labels = findTextLabels(small,width=480,height=352)

idnp_img = small[labels[0][1]:labels[0][3],labels[0][0] - 50:labels[0][2]]
#increase label
bloodType_img = small[labels[1][1]:labels[1][3],labels[1][0]:labels[1][2]]
locationCity_img = small[labels[2][1]:labels[2][3],labels[2][0]:labels[2][2]]
# locationStreet1_img = small[350:400,0:350]
# locationStreet2_img = small[350:400,350:700]
dateOfRegistration_img = small[labels[3][1]:labels[3][3],labels[3][0]:labels[3][2]]

idnp = image_to_string(idnp_img,lang="rus")
bloodType  = image_to_string(bloodType_img)
locationCity = image_to_string(locationCity_img)

# locationStreet = (image_to_string(locationStreet1_img,lang="ron") + image_to_string(locationStreet2_img,lang="ron"))
dateOfRegistration = (image_to_string(dateOfRegistration_img))

print("IDNP : " + idnp)
print("Blood Type : " + bloodType)
print("Location city : " + locationCity)
# print("Location street : " + locationStreet)
print("Date of registration : " + dateOfRegistration)

# idnp,bloodType,locationCity,locationStreet, dateOfRegistration


