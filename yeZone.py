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

#adds current position to position arrays if moving in same direction, resets otherwise
def updateCoords(pos):
    if len(yeXCoords) == 0 or (len(yeXCoords) == 1 and yeXCoords[0] != pos[0]):
        addCoords(pos)
    else:
        if yeXCoords[-1] != pos[0]:
            if (yeXCoords[-1]-yeXCoords[-2] > 0 and pos[0]-yeXCoords[-1] > 0) or (yeXCoords[-1]-yeXCoords[-2] < 0 and pos[0]-yeXCoords[-1] < 0): #moving same x direction
                if (yeYCoords[-1]-yeYCoords[-2] > 0 and pos[1]-yeYCoords[-1] > 0) or (yeYCoords[-1]-yeYCoords[-2] < 0 and pos[1]-yeYCoords[-1] < 0): #moving same y direction
                    addCoords(pos)
                    # printCoords()
                    return
        # print("DIRECTION CHANGE")
        yeXCoords.clear()
        yeYCoords.clear()
        addCoords(pos)
    # printCoords()
        
def addCoords(pos):
    yeXCoords.append(pos[0])
    yeYCoords.append(pos[1])

def printCoords():
    print(f'{[(yeXCoords[i],yeYCoords[i]) for i in range(len(yeXCoords))]}\n')

#uses line of best fit to generate trajectory
def generateTrajectory():
    m, b = np.polyfit(yeXCoords, yeYCoords, 1)

    endPoint = [yeXCoords[-1], yeYCoords[-1]]
    if yeXCoords[-1] > yeXCoords[-2]: #moving right
        endPoint[0] = PLAYZONECOORDS[2]+PLAYZONECOORDS[0]
    else: #moving left
        endPoint[0] = 0
    endPoint[1] = m*endPoint[0]+b

    return (int(endPoint[0]), int(endPoint[1]))

PLAYZONECOORDS = [328, 403, 888, 965]
XLEN = PLAYZONECOORDS[2]-PLAYZONECOORDS[0]
YLEN = PLAYZONECOORDS[3]-PLAYZONECOORDS[1]

yeXCoords, yeYCoords = [], []
while True:
    playZone = createCapture(PLAYZONECOORDS)

    ye = createCapture(PLAYZONECOORDS)
    ye = colorFilter(ye, [142,99,56], 10)
    #tracking ye position
    try:
        yePos = getCenter(ye)
        updateCoords(yePos)
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