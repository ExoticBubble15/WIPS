#https://circuitsgame.com/
#https://circuitsgame.com/puzzle49-1/
#https://circuitsgame.com/puzzle45/
import cv2
from PIL import ImageGrab
import numpy as np
import pytesseract

#for correcting ocr readings
VALID = "1234567890qwertyuiopasdfghjklzxcvbnm"
def correct(str):
    str = str.lower()
    ret = ""
    for i in range(len(str)):
        if VALID.find(str[i]) != -1:
            ret += str[i]
    return ret

#node class for representing cells
class Node:
    def __init__(self, text):
        self.text = text
        self.top, self.bot, self.left, self.right = None, None, None, None
    
    def displayNode(self):
        ret = (f'node text: {self.text} | ')
        if self.top != None:
            ret += f'top: {self.top.text}, '
        if self.bot != None:
            ret += f'bot: {self.bot.text}, '
        if self.left != None:
            ret += f'left: {self.left.text}, '
        if self.right != None:
            ret += f'right: {self.right.text}'
        return ret

wordGraph = [["","","",""], ["","","",""], ["","","",""], ["","","",""]]    #creates virtual game board: '~' denotes user inputted space, [y][x] for accessing
def display(prefix, arr):
    print(f'\n{prefix}')
    for i in range(len(arr)):
        print(arr[i])

def colorFilter(img, rgb, tolerance):
    r, g, b = rgb[0], rgb[1], rgb[2]
    lowerBound = np.array([b-tolerance, g-tolerance, r-tolerance])
    upperBound = np.array([b+tolerance, g+tolerance, r+tolerance])
    return cv2.inRange(img, lowerBound, upperBound)

def addHorizEdge(xCount, yCount):
    leftNode = wordGraph[yCount][xCount]
    rightNode = wordGraph[yCount][xCount+1]
    leftNode.right = rightNode
    rightNode.left = leftNode

def addVertEdge(xCount, yCount):
    topNode = wordGraph[yCount][xCount]
    botNode = wordGraph[yCount+1][xCount]
    topNode.bot = botNode
    botNode.top = topNode

BOXCOORDS = [1920/2-315, 1080/2-15, 1920/2+315, 1080/2+325]
YADJ = 20   #adjusting cell view area so ocr works
XSEGMENT, YSEGMENT = (BOXCOORDS[2]-BOXCOORDS[0])/4, (BOXCOORDS[3]-BOXCOORDS[1])/4
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#reading and creating cells
print("READING AND CREATING CELLS")
for yCount in range(4):
    for xCount in range(4):
        img = ImageGrab.grab(bbox=(BOXCOORDS[0]+xCount*XSEGMENT, BOXCOORDS[1]+yCount*YSEGMENT+YADJ, BOXCOORDS[0]+(xCount+1)*XSEGMENT, BOXCOORDS[1]+(yCount+1)*YSEGMENT-YADJ))
        img = np.array(img)
        word = correct(pytesseract.image_to_string(img))
        if len(np.where(img==[0])[0]) != 0: #detecting if area has any black and thus is nonempty
            if word == "":
                word = "~"
            wordGraph[yCount][xCount] = Node(word) 
        print(f'{xCount}, {yCount}: {word}')
        # cv2.imshow("", img)
        # cv2.waitKey(0)

#creating edges
connectSize = 3
#traverses horizontal edges, left to right then top to bot
print("\nCREATING HORIZONTAL EDGES")
for yCount in range(4):
    for xCount in range(3):
        img = ImageGrab.grab(bbox=(BOXCOORDS[0]+(xCount+1)*XSEGMENT-connectSize, BOXCOORDS[1]+yCount*YSEGMENT, BOXCOORDS[0]+(xCount+1)*XSEGMENT+connectSize, BOXCOORDS[1]+(yCount+1)*YSEGMENT))
        img = np.array(img)
        img = colorFilter(img, [0,0,0], 50)
        # cv2.imshow("", img)
        if len(np.where(img==[255])[0]) != 0:
            print(f'horizontal edge at xCount:{xCount}, yCount:{yCount}')
            addHorizEdge(xCount, yCount)
        else:
            print(f'nothing at xCount:{xCount}, yCount:{yCount}')
        # cv2.waitKey(0)
    print("~~~~~~~~")

#traverses vertical edges, top to bot then left to right
print("\nCREATING VERTICAL EDGES")
for xCount in range(4):
    for yCount in range(3):
        img = ImageGrab.grab(bbox=(BOXCOORDS[0]+xCount*XSEGMENT, BOXCOORDS[1]+(yCount+1)*YSEGMENT-connectSize, BOXCOORDS[0]+(xCount+1)*XSEGMENT, BOXCOORDS[1]+(yCount+1)*YSEGMENT+connectSize))
        img = np.array(img)
        img = colorFilter(img, [0,0,0], 50)
        # cv2.imshow("", img)
        if len(np.where(img==[255])[0]) != 0:
            print(f'vertical edge at xCount:{xCount}, yCount:{yCount}')
            addVertEdge(xCount, yCount)
        else:
            print(f'nothing at xCount:{xCount}, yCount:{yCount}')
        # cv2.waitKey(0)
    print("~~~~~~~~")

print("\nNODES")
for row in range(len(wordGraph)):
    for col in range(len(wordGraph[row])):
        str = (f'row {row}, col {col} - ')
        try:
            str += (wordGraph[row][col].displayNode())
        except:
            str += "nothing"
        print(str)