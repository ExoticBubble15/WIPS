#http://www.kanyezone.com/
import cv2
from PIL import ImageGrab, Image
import numpy as np
import keyboard

def createCapture(boxCords):
    #upper left, bottom right
    img = ImageGrab.grab(bbox=(boxCords[0], boxCords[1], boxCords[2], boxCords[3]))
    img = np.array(img)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def colorFilter(img, rgb, tolerance):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    lowerBound = np.array([b-tolerance, g-tolerance, r-tolerance])
    upperBound = np.array([b+tolerance, g+tolerance, r+tolerance])
    return cv2.inRange(img, lowerBound, upperBound)

def getCenter(img):
    Y, X = np.where(img==[255])
    return ((sum(X)//len(X)), (sum(Y)//len(Y)))

#will add current position to yeCoordsList if still moving in the same direction
def updateCoordsList(pos):
    if len(yeCoordsList)==0 or (len(yeCoordsList)==1 and yeCoordsList[0] != pos):
        yeCoordsList.append(pos)
    else:
        if yeCoordsList[-1] != pos:
            if(yeCoordsList[-1][0]-yeCoordsList[-2][0] > 0 and pos[0]-yeCoordsList[-1][0] > 0) or (yeCoordsList[-1][0]-yeCoordsList[-2][0] < 0 and pos[0]-yeCoordsList[-1][0] < 0): #moving same x direction
                    if(yeCoordsList[-1][1]-yeCoordsList[-2][1] > 0 and pos[1]-yeCoordsList[-1][1] > 0) or (yeCoordsList[-1][1]-yeCoordsList[-2][1] < 0 and pos[1]-yeCoordsList[-1][1] < 0): #moving same y direction
                        yeCoordsList.append(pos)
                        return
        print("direction change")
        yeCoordsList.clear()
        yeCoordsList.append(pos)

#uses line of best fit to generate trajectory
def generateTrajectory():
    xVals = [i[0] for i in yeCoordsList]
    yVals = [i[1] for i in yeCoordsList]
    m, b = np.polyfit(xVals, yVals, 1)

    endPoint = [xVals[-1], yVals[-1]]

    if xVals[-1] > xVals[-2]: #moving right
        endPoint[1] = m*(xVals[-1]+XLEN)+b
    else: #moving left
        endPoint[1] = m*(xVals[-1]-XLEN)+b

    if yVals[-1] > yVals[-2]: #moving down
        endPoint[0] = (yVals[-1]+YLEN-b)/m
    else: #moving up
        endPoint[0] = (yVals[-1]-YLEN-b)/m

    return (int(endPoint[0]), int(endPoint[1]))

PLAYZONECOORDS = [328, 403, 888, 965]
XLEN = PLAYZONECOORDS[2]-PLAYZONECOORDS[0]
YLEN = PLAYZONECOORDS[3]-PLAYZONECOORDS[1]

yeCoordsList = []
while True:
    playZone = createCapture(PLAYZONECOORDS)

    ye = createCapture(PLAYZONECOORDS)
    ye = colorFilter(ye, [142,99,56], 10)
    #tracking ye position
    try:
        yePos = getCenter(ye)
        updateCoordsList(yePos)
        playZone = cv2.line(playZone, yePos, generateTrajectory(), [0,255,0], 2)

        #putting box around ye
        Y, X = np.where(ye==[255])
        playZone = cv2.rectangle(playZone, (min(X),min(Y)), (max(X),max(Y)), [31,95,255], 2)
        # print("noError")
    except Exception as e:
        # print(e)
        pass

    # player = createCapture(PLAYZONECOORDS)
    # player = colorFilter(player, [100,161,252], 20)
    # try:
    #     player = cv2.circle(player, getCenter(player), ((max(Y)-min(Y))//2), [31,95,255], 2)
    # except:
    #     pass

    #trajectory
    # protect = createCapture(PLAYZONECOORDS)
    # protect = colorFilter(protect, [185,144,238], 20)
    # try:
    #     # playZone = cv2.line(playZone, getCenter(ye), getCenter(protect), [0,0,255], 2)
    #     # playZone = cv2.line(playZone, getCenter(player), getCenter(protect), [0,255,0], 2)
    #     playZone = cv2.line(playZone, getCenter(player), getCenter(ye), [31,95,255], 2)
    # except:
    #     pass


    cv2.imshow("", playZone)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if keyboard.is_pressed('enter'):
        print("``````````````")