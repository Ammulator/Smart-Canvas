import cv2
import os
import numpy as np
import HandTrackingModule as htm
import time

#################
brushThickness=15
eraserThickness=50
############
#Header Image 
folderPath="Header1"
myList=os.listdir(folderPath)
print(myList)
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

header=overlayList[0]
drawColor=(255,0,255)

#Side Image
folderPath1="Sider"
myList1=os.listdir(folderPath1)
print(myList1)
overlayList1=[]
for imgP in myList1:
    image1=cv2.imread(f'{folderPath1}/{imgP}')
    overlayList1.append(image1)
print(len(overlayList1))

sider=overlayList1[2]



cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=htm.handDetector(detectionCon=0.85)
xp,yp=0,0

#numpy to draw canvas and it will have 0 to 255 values
imgCanvas=np.zeros((720,1280,3),np.uint8)



while True:
    #Import Image
    success,img=cap.read()
    img=cv2.flip(img,1)
 
    #Find Hand Landmarks
    img=detector.findHands(img)
    lmList,bb=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList)


        #Tip of Index and Middle Fingers
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]


        #Check Which Fingers are Up
        fingers=detector.fingersUp()
        #print(fingers)


        #If Selection mode - 2 fingers are up 
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            print("Selection Mode")
            #Checking For Click Color check
            if y1<167:
                if 148<x1<312:
                    header=overlayList[0]
                    drawColor=(255,0,255)
                elif 368<x1<517:
                    header=overlayList[1]
                    drawColor=(0,255,0)
                elif 554<x1<703:
                    header=overlayList[2]
                    drawColor=(0,0,255)
                elif 741<x1<890:
                    header=overlayList[3]
                    drawColor=(255,0,0)
                elif 946<x1<1142 and y1<147:
                    header=overlayList[4]
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

            if (0<y1<570) and (1180<x1<1280):
                if 121<y1<174:
                    sider=overlayList1[0]
                    brushThickness=25
                elif 219<y1<272:
                    sider=overlayList1[1]
                    brushThickness=20
                elif 315<y1<368:
                    sider=overlayList1[2]
                    brushThickness=15
                elif 387<y1<440:
                    sider=overlayList1[3]
                    brushThickness=10
                elif 483<y1<526:
                    sider=overlayList1[4]
                    brushThickness=5


        #If Drawing mode - Index is Up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),brushThickness,drawColor,cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

            xp,yp=x1,y1
        if all (x >= 1 for x in fingers):
            imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    #We Convert our gray image into inverse image with black area.
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)

    #Setting Header Image
    img[0:167,100:1180]=header

    #Setting Sider Image
    img[0:570,1180:1280]=sider

   # img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image",img)
    cv2.imshow("Canvas",imgCanvas)
    cv2.waitKey(1)

