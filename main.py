##
## Todo
##  Make boxes sizes dynamic based on total coverage
##  change the centre point of the boxes based on the content they cover
##  stuff

from PIL import Image, ImageDraw
import time

projStart = time.perf_counter()

im = Image.open('avaire-512x512.png') # Can be many different formats.
firstPixels = im.load()

im = Image.open('changed.png') # Can be many different formats.
secondPixels = im.load()

draw = ImageDraw.Draw(im) 
def drawLine(first, second, colour = (0, 255, 0, 255)):
    draw.line((first[0], first[1], second[0], second[1]), fill=colour)

def drawBox(first, second, colour = (0, 255, 0, 255)):
    #print(first[0] - second[0])
    #print(first[1] - second[1])
    # second[1] top
    # first[1] bottom


    bottomRight = (first[0], second[1])
    bottomLeft =  (second[0], second[1])


    topLeft = (second[0], first[1])
    topRight  =  (first[0], first[1])
    
    #im.show()
    drawLine(topLeft, topRight, colour=(0, 0, 255, 255)) # bottom
    drawLine(bottomLeft, bottomRight, colour=(0, 0, 255, 255)) # top

    drawLine(topLeft, bottomLeft, colour=(0, 0, 255, 255)) # left
    drawLine(topRight, bottomRight, colour=(0, 0, 255, 255)) # right
    
    

#print (im.size)  # Get the width and hight of the image for iterating over
#print(im.size)
#print(im.size[0])
#print(im.size[1])
#print (firstPixels[im.size[0] - 1,im.size[1] - 1])  # Get the RGBA Value of the a pixel of an image
#firstPixels[im.size[0] - 1,im.size[1] - 1] = (1, 1, 1, 1)  # Set the RGBA Value of the image (tuple)
#im.save('alive_parrot.png')  # Save the modified pixels as .png

RED_OUT_COLOUR = (255, 0, 0, 255)

_x = im.size[0]
_y = im.size[1]

print(_x, _y)

top_left = [0, 0]
top_right = [0, 0]
bottom_left = [0, 0]
bottom_right = [0, 0]

i = 0

def pythag(thing, printE = False):
    final = 0
    cnt = 0
    for i in thing:
        cnt += 1
        final += (i / 255)
    final /= cnt
    #if(printE and final < 0):
    #    print("less than")
    return final

def calcSimilarity(colour1, colour2, printE = False):
    cnt = 0
    stuff = [0] * 4
    for i in colour1:
        stuff[cnt] += abs(colour1[cnt] - colour2[cnt])
        cnt += 1

    #if(printE):
    #    print(colour1, " + ", colour2)
    #    print((stuff[0], stuff[1], stuff[2], stuff[3]))
    #    print(pythag([stuff[0], stuff[1], stuff[2], stuff[3]]))

    return 1 - pythag([stuff[0], stuff[1], stuff[2], stuff[3]])

def calcDifference(colour1, colour2, printE = False):
    return 1 - calcSimilarity(colour1, colour2, printE = False)
#both = calcSimilarity((223, 110, 51, 255), (76, 33, 11, 255), True)
#print(" - Similarity", both)
#input()

boxes = [
    #[
       # (0, 150),    # top left
       # (120, 250)  # bottom right
    ##]
]

def distanceBetween2Points_s(point1, point2):
    #print(point1, point2)
    return distanceBetween2Points(point1[0], point1[1], point2[0], point2[1])

def distanceBetween2Points(x1, y1, x2, y2):
    result= ((((x2 - x1 )**2) + ((y2-y1)**2) )**0.5)

    #print("distance between",(x1,x2),"and",(y1,y2),"is : ",result)
    return result

def calculateAreaTriangle(firstPoint, secondPoint, thirdPoint):
    a = distanceBetween2Points_s(firstPoint, secondPoint)
    b = distanceBetween2Points_s(firstPoint, thirdPoint)
    c = distanceBetween2Points_s(thirdPoint, secondPoint)
    #print(a)
    s = (a + b + c) / 2  
  
    # calculate the area  
    area = (s*(s-a)*(s-b)*(s-c)) ** 0.5  
    return area

def isWithinXY(pointX, pointY, leftX, topY, rightX, bottomY):
    start = time.perf_counter()

    cubeArea = abs((rightX - leftX) * (topY - bottomY))

    topLeft = (leftX, topY)
    bottomRight = (rightX, bottomY)
    bottomLeft =  (leftX, bottomY)
    topRight  =  (rightX, topY)

    total = 0
    total += calculateAreaTriangle(topLeft, bottomLeft, (pointX, pointY))
    total += calculateAreaTriangle(topLeft, topRight, (pointX, pointY))
    total += calculateAreaTriangle(topRight, bottomRight, (pointX, pointY))
    total += calculateAreaTriangle(bottomRight, bottomLeft, (pointX, pointY))

    ##print("Total area:", total)
    #print("Cube area:", cubeArea)

    if(total - 0.01 <= cubeArea):
    #    print("Is within")
        return True
    else:
    #    print("Is not within")
        return False

    drawLine((pointX, pointY), topLeft, (0, 255, 0, 255))
    drawLine((pointX, pointY), bottomRight, (0, 255, 0, 255))

 
    drawLine((pointX, pointY), bottomLeft, (0, 0, 255, 255))
    drawLine((pointX, pointY), topRight, (0, 0, 255, 255))


def isWithinBox(
    pointX, pointY, Box):

    isWithinXY(pointX, pointY, Box[0][0], Box[0][1], Box[1][0], Box[1][1])


#for box in boxes:
#    isWithinBox(60, 200, box)

#for box in boxes:
#    drawBox(box[0], box[1])

#im.show()

#input()

spacing = 100
spacingDiag = 141.42135623730950488016887242097

done = True
highestSim = 0
startBigLogic_Average = 0
for x in range(0, _x - 1):
    start = time.perf_counter()
    for y in range(0, _y - 1):
        similarity = calcSimilarity(firstPixels[x, y], secondPixels[x, y])
        difference = calcDifference(firstPixels[x, y], secondPixels[x, y])

        # same 0 different 1
        if(difference >= 0.1):
            #print(len(boxes))
            startBigLogic = time.perf_counter()

            if(len(boxes) == 0):
                bottomRight = (x - spacing, y + spacing)
                topLeft = (x + spacing, y - spacing)

                if(topLeft[0] < 0):
                    topLeft[0] = 0
                if(topLeft[1] < 0):
                    topLeft[1] = 0
                if(bottomRight[0] < 0):
                    bottomRight = (0, bottomRight[1])
                if(bottomRight[1] < 0):
                    bottomRight[1] = 0
                #im.show()

                boxes.append([ topLeft, bottomRight, (x, y)])

                for box in boxes:
                    #drawLine(box[0], box[1], (255, 0, 255, 255))
                    drawBox(box[0], box[1], (255, 0, 255, 255))
                    #im.show()
            cntBox = 0
            isWithinABox = False
            nearest = 10000
            for box in boxes:
                if(isWithinBox(x, y, box)):
                    isWithinABox = True
                    break
                dist = distanceBetween2Points_s((x, y), box[2])
                if(dist < nearest):
                    nearest = dist
                    if(nearest <= spacingDiag):
                        isWithinABox = True
                        break

                cntBox += 1

            if(isWithinABox == False):
                #print("Not in a box", x, y, len(boxes), "boxes!")
                
                topLeft = (x - spacing, y + spacing)
                bottomRight = (x + spacing, y - spacing)

                if(topLeft[0] < 0):
                    topLeft[0] = 0
                if(bottomRight[1] < 0):
                    bottomRight = (bottomRight[0], 0)
                if(bottomRight[0] < 0):
                    bottomRight[0] = 0
                if(bottomRight[1] < 0):
                    bottomRight[1] = 0
                    
                boxes.append([ topLeft, bottomRight, (x, y)])


            secondPixels[x, y] = RED_OUT_COLOUR
            highestSim = max(highestSim, similarity)
            startBigLogic_Average += time.perf_counter() - startBigLogic
            startBigLogic_Average /= 2

    if(x % 100 == 0):
        print(x)
        print("tim", (time.perf_counter() - start) * 100)
        print("startBigLogic_Average", (startBigLogic_Average * 100))


for box in boxes:
    drawBox(box[0], box[1])

im.show()
print("\n")
print("Took:", (time.perf_counter() - projStart) * 1000, "ms")
print("startBigLogic_Average", (startBigLogic_Average * 100))
print("Done with", len(boxes), "boxes!")
print("highestSim:", highestSim)

im.save('detected.png')  # Save the modified pixels as .png

import webbrowser

webbrowser.open("file:///C:/Users/Conni/Desktop/RandomProject/Motion/detected.png")