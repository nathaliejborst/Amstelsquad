# Filename: amstelhaege.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Plots potential residential area Amstelhaege.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon
import math
from datetime import datetime

startTime = datetime.now()

global areaVariant
global amountOWater
global amountOfMaisons
global amountOfBungalows
global amountOfFamilyHouses

# Fixing random state for reproducibility
# np.random.seed(0)

# Doesn't work yet
class Grid:
    def __init__(self, housesList = []):
        self.housesList = housesList

    def totalValue(self, housesList):
        value = 0
        for i in range(len(housesList)):
            value += housesList[i].value
            value += ((housesList[i].extraFreespace - housesList[i].freespace) * housesList[i].valueUpdate) * housesList[i].value
            return value


# Declare elements of house in class.
class House:

    def __init__(self, width, height, freespace, value, valueUpdate, x=0, y=0, color=None, distanceToOthers = [], extraFreespace=0):
        self.width = width
        self.height = height
        self.freespace = freespace
        self.value = value
        self.valueUpdate = valueUpdate
        self.x = x
        self.y = y
        self.color = color
        self.distanceToOthers = distanceToOthers
        self.extraFreespace = extraFreespace

    def area(self):
        return self.width * self.height

    def Xmin(self, x):
        return x
    def Xmax(self, x):
        return (x + self.width)
    def Ymin(self, y):
        return y
    def Ymax(self, y):
        return (y + self.height)

    def corners(self, x, y):
        bottomLeft = [x, y]
        upperLeft = [x, (y + self.height)]
        upperRight = [(x + self.width), (y + self.height)]
        bottomRight = [(x + self.width), y]
        return [bottomLeft, upperLeft, upperRight, bottomRight]

    def spacecorners(self, x, y):
        bottomLeft = [x - self.freespace, y - self.freespace]
        upperLeft = [x - self.freespace, (y + self.height + self.freespace)]
        upperRight = [(x + self.width + self.freespace), (y + self.height + self.freespace)]
        bottomRight = [(x + self.width + self.freespace), y - self.freespace]
        return [bottomLeft, upperLeft, upperRight, bottomRight]

    def extraFreeSpaceCorners(self, x, y):
        bottomLeft = [x - self.freespace - self.extraFreespace, y - self.freespace - self.extraFreespace]
        upperLeft = [x - self.freespace  - self.extraFreespace, (y + self.height + self.freespace + self.extraFreespace)]
        upperRight = [(x + self.width + self.freespace + self.extraFreespace), (y + self.height + self.freespace + self.extraFreespace)]
        bottomRight = [(x + self.width + self.freespace + self.extraFreespace), y - self.freespace  - self.extraFreespace]
        return [bottomLeft, upperLeft, upperRight, bottomRight]


    def addFreespace(self, meter):
        self.meter = meter
        self.freespace += meter
        self.value = round(self.value * self.valueUpdate ** int(meter), 2)
        return self.freespace, self.value

    def totalWidth(self):
        return self.width + self.freespace * 2

    def totalHeight(self):
        return self.height + self.freespace * 2

# List of every house placed on the grid
houses = []

# Declare restrictions for Amstelheage area.
areaWidth = 180
areaHeight = 160
fig, area = plt.subplots()
area.set_xlim(xmin=0, xmax=areaWidth)
area.set_ylim(ymin=0, ymax=areaHeight)
area.set_aspect('equal', adjustable='box')
area.set_title('Amstelhaege')

# Declare possible area variants by setting matching amount of housetypes
# Choose area variant by changing areaVariant to 1, 2 or 3.
areaVariant = 3
amountOWater = 0
amountOfMaisons = 3 * areaVariant
amountOfBungalows = 5 * areaVariant
amountOfFamilyHouses = 12 * areaVariant

# Returns true if two houses intersect.
def Intersect(p1, p2, s1, s2):
    if p1.intersects(p2) is True or p1.intersects(s2) is True or s1.intersects(p2) is True:
        return True
    else:
        return False

def placeFirstMaison(houseType):
    houseType.x = houseType.freespace
    houseType.y = houseType.freespace

    houses.append(houseType)
    amountOfMaisons = 2

def placeHouse(houseType):

    # Declare true at first, because it has to place a house.
    intersect = True

    # Keeps trying to place a house until it does not intersect with another house anymore.
    while intersect is True:

        # Generate random x and y bottom corner coordinates.
        houseType.x = np.random.randint(low=houseType.freespace, high=areaWidth -
                              houseType.freespace - houseType.width)

        houseType.y = np.random.randint(low=houseType.freespace,
                              high=areaHeight - houseType.freespace -
                              houseType.height)


        # Declare corners and free space corners for house to be placed.
        p1 = Polygon(houseType.corners(houseType.x, houseType.y))
        s1 = Polygon(houseType.spacecorners(houseType.x, houseType.y))

        for j in range(len(houses)):
            p2 = Polygon(houses[j].corners(houses[j].x, houses[j].y))
            s2 = Polygon(houses[j].spacecorners(houses[j].x, houses[j].y))

            # Check if house intersects.
            intersect = Intersect(p1, p2, s1, s2)

            if intersect is True:
                break
    if intersect is False:
    #  Add placed house to list of houses.
        houses.append(houseType)


placeFirstMaison(House(width=11, height=10.5, freespace=6, value=610000,
           valueUpdate=1.06))

# Place water
water = House(width=144, height=40, freespace=0, value=0, valueUpdate=0, color='blue')
placeHouse(water)

# Place maisons
for maisons in range(amountOfMaisons):
    maison = House(width=11, height=10.5, freespace=6, value=610000,
               valueUpdate=0.06, color='red')
    placeHouse(maison)

# Place bungalows
for bungalows in range (amountOfBungalows):
    bungalow = House(width=10, height=7.5, freespace=3, value=399000,
                 valueUpdate=0.04, color='orange')
    placeHouse(bungalow)

# Place familyhouses
for familyHouses in range(amountOfFamilyHouses):
    familyHouse = House(width=8, height=8, freespace=2, value=285000,
                        valueUpdate=0.03, color='yellow')
    placeHouse(familyHouse)

grid = Grid(houses)
valueTotal = 0

# Plots and prints grid.
def PlotHouses():
    for house in range(len(houses)):
        area.add_patch(plt.Polygon(houses[house].corners(houses[house].x, houses[house].y), color=houses[house].color))
        area.add_patch(plt.Polygon(houses[house].spacecorners(houses[house].x, houses[house].y), fill=False))
        area.add_patch(plt.Polygon(houses[house].extraFreeSpaceCorners(houses[house].x, houses[house].y), fill=False))

        # Print coordinates list
        # print(houses[house].corners(houses[house].x, houses[house].y))

    plt.show()

def CalculateDistance(h):
    distance_for_h = []

    for i in range(len(houses)):

        Xmin_h = houses[h].Xmin(houses[h].x)
        Xmax_h = houses[h].Xmax(houses[h].x)
        Ymin_h = houses[h].Ymin(houses[h].y)
        Ymax_h = houses[h].Ymax(houses[h].y)

        Xmin_i = houses[i].Xmin(houses[i].x)
        Xmax_i = houses[i].Xmax(houses[i].x)
        Ymin_i = houses[i].Ymin(houses[i].y)
        Ymax_i = houses[i].Ymax(houses[i].y)

        # Returns true if house i has same x coordinates
        def Xmatch(Xmin_h, Xmax_h, Xmin_i, Xmax_i):
            if ((Xmin_i > Xmin_h and Xmin_i <Xmax_h) or (Xmax_i > Xmin_h and Xmax_i < Xmax_h)):
                return True
            else:
                return False

        # Returns true if house i has same y coordinates
        def Ymatch(Ymin_h, Ymax_h, Ymin_i, Ymax_i):
            if ((Ymin_i > Ymin_h and Ymin_i <Ymax_h) or (Ymax_i > Ymin_h and Ymax_i < Ymax_h)):
                return True
            else:
                return False

        # Checks distance between x coordinates or y coordinates of houses.
        def checkDistance(min_h, max_h, min_i, max_i):
            # Checks if house i is to the right (x) or to the top (y) of the house.
            if (min_i - max_h > 0):
                distance = min_i - max_h
                return distance
            # Checks if house i is to the left (x) or to the bottom (y) of the house.
            if (min_h - max_i > 0):
                distance = min_h - max_i
                return distance
            else:
                distance = 0
                return distance

        # Pythagoras, rounds to four decimal points
        def Pythagoras(xDistance, yDistance):
            distance = round(math.sqrt(pow(xDistance, 2) + pow(yDistance, 2)), 4)
            return distance

        # Checks if x coordinates match (distance is then difference in y coordinates)
        if Xmatch(Xmin_h, Xmax_h, Xmin_i, Xmax_i) is True:
            distance = checkDistance(Ymin_h, Ymax_h, Ymin_i, Ymax_i)
            distance_for_h.append(distance)

        # Checks if y coordinates match (distance is then difference in x coordinates)
        if Ymatch(Ymin_h, Ymax_h, Ymin_i, Ymax_i) is True:
            distance = checkDistance(Xmin_h, Xmax_h, Xmin_i, Xmax_i)
            distance_for_h.append(distance)

        # Calculates distance using Pythagoras when x and y coordinates don't match
        if ((Xmatch(Xmin_h, Xmax_h, Xmin_i, Xmax_i) is False) and (Ymatch(Ymin_h, Ymax_h, Ymin_i, Ymax_i) is False)):
            # Calculates distance between y coordinates and x coordinates
            xDistance = checkDistance(Xmin_h, Xmax_h, Xmin_i, Xmax_i)
            yDistance = checkDistance(Ymin_h, Ymax_h, Ymin_i, Ymax_i)

            # Add distance to list
            distance_for_h.append(Pythagoras(xDistance, yDistance))

    # Add list of distances to house instance.
    houses[h].distanceToOthers = distance_for_h

# Caculate distance to other houses and app
for h in range(len(houses)):
    CalculateDistance(h)

# Returns minimum distance to other houses in grid (besides distance to itself = 0).
def FindMinimumDistance(k):
    sortedDistances = sorted(houses[k].distanceToOthers, key=float)
    return sortedDistances

# Get minimum distance to nearest house.
for k in range(len(houses)):
    minimumDistance = FindMinimumDistance(k)[1]
    houses[k].extraFreespace = minimumDistance
    # print(houses[k].extraFreespace)

# print(grid.housesList[0].extraFreespace) > test to see if you can acces house instance from grid (works!)

print("Total value: {}".format(round(grid.totalValue(grid.housesList), 2)))
print("Total runtime: {}".format(datetime.now() - startTime))

def Calculate():
    count = 0
    j = 0
    while j < (len(houses)):
        print("hoi1")
        print(j)
        x = 1 + count
        y = 1 + count

        s1 = Polygon([(houses[j].spacecorners(houses[j].x, houses[j].y)[0][0] - x, houses[j].spacecorners(houses[j].x, houses[j].y)[0][1] - y),
        (houses[j].spacecorners(houses[j].x, houses[j].y)[1][0] + x, houses[j].spacecorners(houses[j].x, houses[j].y)[1][1] - y),
        (houses[j].spacecorners(houses[j].x, houses[j].y)[2][0] + x, houses[j].spacecorners(houses[j].x, houses[j].y)[2][1] + y),
        (houses[j].spacecorners(houses[j].x, houses[j].y)[3][0] - x, houses[j].spacecorners(houses[j].x, houses[j].y)[3][1] + y)])

        print(s1)
        # NIEUWE EXTRA SPACE PLOTTEN

        for k in range(len(houses)):
            p1 = Polygon([(houses[k].corners(houses[k].x, houses[k].y)[0][0], houses[k].corners(houses[k].x, houses[k].y)[0][1]),
            (houses[k].corners(houses[k].x, houses[k].y)[1][0], houses[k].corners(houses[k].x, houses[k].y)[1][1]),
            (houses[k].corners(houses[k].x, houses[k].y)[2][0], houses[k].corners(houses[k].x, houses[k].y)[2][1]),
            (houses[k].corners(houses[k].x, houses[k].y)[3][0], houses[k].corners(houses[k].x, houses[k].y)[3][1])])

            # print("hello1")

            if s1.touches(p1) is True:

                s1 = Polygon([(houses[j].spacecorners(houses[j].x, houses[j].y)[0][0] + x, houses[j].spacecorners(houses[j].x, houses[j].y)[0][1] + y),
                        (houses[j].spacecorners(houses[j].x, houses[j].y)[1][0] - x, houses[j].spacecorners(houses[j].x, houses[j].y)[1][1] + y),
                        (houses[j].spacecorners(houses[j].x, houses[j].y)[2][0] - x, houses[j].spacecorners(houses[j].x, houses[j].y)[2][1] - y),
                        (houses[j].spacecorners(houses[j].x, houses[j].y)[3][0] + x, houses[j].spacecorners(houses[j].x, houses[j].y)[3][1] - y)])

                # SPACE EXTRA WEGHALEN UIT PLOT
                print("hello2")
                count = 0
                j += 1
                break

        else:
            # ALLE KLEINERE SPACES WEGHALEN UIT PLOT
            count += 1  # X EN Y UIT SPACELIST KUNNEN BUITEN BOUNDERIES GAAN
            print("hoi2")
            print(j)




PlotHouses()
