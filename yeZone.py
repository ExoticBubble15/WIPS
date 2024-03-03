#http://www.kanyezone.com/
import cv2
from PIL import ImageGrab, Image
import numpy as np

def createCapture(boxCords):
    #upper left, bottom right
    img = ImageGrab.grab(bbox=(boxCords[0], boxCords[1], boxCords[2], boxCords[3]))
    img = np.array(img)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def colorFilter(img, rgb, tolerance):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    lowerBound = np.array([b-tolerance,g-tolerance,r-tolerance])
    upperBound = np.array([b+tolerance,g+tolerance,r+tolerance])
    return cv2.inRange(img, lowerBound, upperBound)

PLAYZONECOORDS = [328,403,888,965]

while True:
    playZone = createCapture(PLAYZONECOORDS)

    ye = createCapture(PLAYZONECOORDS)
    ye = colorFilter(ye,[142,99,56],35)
    try:
        Y,X = np.where(ye==[255])
        ye = cv2.rectangle(ye,(min(X),min(Y)),(max(X),max(Y)),[31,95,255],2)
    except:
        pass

    player = createCapture(PLAYZONECOORDS)
    player = colorFilter(player,[100,161,252],20)
    try:
        Y,X = np.where(player==[255])
        xAvg = sum(X)//len(X)
        yAvg = sum(Y)//len(X)
        player = cv2.circle(player,(xAvg, yAvg),(max(Y)-min(Y))//2,[31,95,255],2)
    except:
        pass    

    cv2.imshow("", ye)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
