import cv2
import numpy as np
MIN_MATCH_COUNT=15

def initObjDetection(template):
    global detector 
    detector = cv2.xfeatures2d.SIFT_create()

    global FLANN_INDEX_KDITREE
    FLANN_INDEX_KDITREE = 0

    global flannParam
    flannParam = dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
    global flann
    flann=cv2.FlannBasedMatcher(flannParam,{})

    trainKP,trainDesc=detector.detectAndCompute(template,None)
    return (trainKP,trainDesc)


def objectDetection(QueryImgBGR,training):

    trainKP,trainDesc = training

    QueryImgBGR = cv2.resize(QueryImgBGR,(1024,768))
    QueryImg=cv2.cvtColor(QueryImgBGR,cv2.COLOR_BGR2GRAY)
    queryKP,queryDesc=detector.detectAndCompute(QueryImg,None)
    matches=flann.knnMatch(queryDesc,trainDesc,k=2)

    goodMatch=[]
    for m,n in matches:
        if(m.distance<0.75*n.distance):
            goodMatch.append(m)

    if(len(goodMatch)>MIN_MATCH_COUNT):
        tp=[]
        qp=[]
        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)
        tp,qp=np.float32((tp,qp))
        H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)
        
        h,w = 768,1024

        trainBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
        queryBorder=cv2.perspectiveTransform(trainBorder,H)
        cv2.polylines(QueryImgBGR,[np.int32(queryBorder)],True,(0,255,0),5)
        # print(queryBorder)
        # cv2.imshow('result',QueryImgBGR)
    
    else:
        print("Not Enough match found- {}/{}".format(len(goodMatch),MIN_MATCH_COUNT))
    
    return queryBorder[0], QueryImgBGR

if __name__ == "__main__":
    
    template = cv2.imread("images/passportTest.jpg",0)
    image = cv2.imread("images/passportFromPhone.jpg")
    initObjDetection(template)
     
    points,image = objectedDetection(image,template)
    print(points)
    cv2.imshow('result',image)
    cv2.waitKey(0)