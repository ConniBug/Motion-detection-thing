import time

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

start = time.perf_counter()

for i in range(0, 1000):
    print(i)
    print(isWithinXY(0, 100, 0, 500, 1231, 2313))