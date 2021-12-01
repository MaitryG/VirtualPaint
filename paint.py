import cv2
import numpy as  np

webcam = cv2.VideoCapture(0)
webcam.set(3,1024)           #Width of Video frame
webcam.set(4,1000)           #Height of Video frame
webcam.set(10,150)          #Brightness of video frame

myColors = [[121,78,46,179,238,255],      #PINK
            [48,45,0,89,178,136]]          #GREEN
            # [98,80,69,156,255,250]]         #blue

myColorValues = [[102,0,204],
                 [0,102,0]]
                 # [255,0,0]]        #In BGR

myPoints = []                       # [x,y,colorId]

def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        # cv2.imshow(str(color[0]),mask)
        x,y=getContours(mask)
        cv2.circle(img_result,(x,y),15,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count = count + 1

    return newPoints

def getContours(img):
    x,y,w,h=0,0,0,0
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>500:
            #cv2.drawContours(img_result,cnt,-1,(255,0,0),5)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x , y, w, h = cv2.boundingRect(approx)

    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
            cv2.circle(img_result,(point[0],point[1]),30,myColorValues[point[2]],cv2.FILLED)


while True:
    success,img = webcam.read()
    img_result = img.copy()
    newPoints = findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(newPoints)!=0:
            drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("Video",img_result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

