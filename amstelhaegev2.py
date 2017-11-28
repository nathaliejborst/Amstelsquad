# Filename: amstelhaege.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Plots potential residential area Amstelhaege.

import numpy as np
import matplotlib.pyplot as plt
import classes as cl
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
np.random.seed(3)


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
amountOWater = 1
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

        for house in houses:
            p2 = Polygon(house.corners(house.x, house.y))
            s2 = Polygon(house.spacecorners(house.x, house.y))

            # Check if house intersects.
            intersect = Intersect(p1, p2, s1, s2)

            if intersect is True:
                break
    if intersect is False:
    #  Add placed house to list of houses.
        houses.append(houseType)


placeFirstMaison(cl.House(width=11, height=10.5, freespace=6, value=610000,
           valueUpdate=1.06))

# Place water
water = cl.House(width=144, height=40, freespace=0, value=0, valueUpdate=0, color='blue')
placeHouse(water)

# Place maisons
for maisons in range(amountOfMaisons):
    maison = cl.House(width=11, height=10.5, freespace=6, value=610000,
               valueUpdate=0.06, color='red')
    placeHouse(maison)

# Place bungalows
for bungalows in range (amountOfBungalows):
    bungalow = cl.House(width=10, height=7.5, freespace=3, value=399000,
                 valueUpdate=0.04, color='orange')
    placeHouse(bungalow)

# Place familyhouses
for familyHouses in range(amountOfFamilyHouses):
    familyHouse = cl.House(width=8, height=8, freespace=2, value=285000,
                        valueUpdate=0.03, color='yellow')
    placeHouse(familyHouse)

grid = cl.Grid(houses)
valueTotal = 0

# Plots and prints grid.
def PlotHouses():
    for house in houses:
        area.add_patch(plt.Polygon(house.corners(house.x, house.y), color=house.color))
        area.add_patch(plt.Polygon(house.spacecorners(house.x, house.y), fill=False))
        area.add_patch(plt.Polygon(house.extraFreeSpaceCorners(house.x, house.y), fill=False, edgecolor='green'))

    plt.show()

# Returns the minimum distance of the nearest house and the positon in houses[] of that house
def straightDistance(min_h, max_h, min_i, max_i):
    # Checks distance in x or y coordinates, returns false if x or y coordinates don't match.
    if((min_h - max_i) >= 0):
        distance = min_h - max_i
        return distance
    if ((min_i - max_h) >= 0):
        distance = min_i - max_h
        return distance
    else:
        return False

def GetDistance(h):

    distances = []

    Xmin_h = houses[h].Xmin(houses[h].x)
    Xmax_h = houses[h].Xmax(houses[h].x)
    Ymin_h = houses[h].Ymin(houses[h].y)
    Ymax_h = houses[h].Ymax(houses[h].y)

    i = 0
    for house in houses:

        Xmin_i = house.Xmin(house.x)
        Xmax_i = house.Xmax(house.x)
        Ymin_i = house.Ymin(house.y)
        Ymax_i = house.Ymax(house.y)

        # Get distance in y and x coordinates to other house (returns false if x or y coordinates match)
        distance_x = straightDistance(Xmin_h, Xmax_h, Xmin_i, Xmax_i)
        distance_y = straightDistance(Ymin_h, Ymax_h, Ymin_i, Ymax_i)

        # Check if y coordinates match
        if((distance_x is not False) and (distance_y is False)):
            distance = distance_x

            dictValues = {'distance': distance, 'x': distance_x, 'y': distance_y}
            distances.append(dictValues)

        # Check if y coordinates match
        elif((distance_x is False) and (distance_y) is not False):
            distance = distance_y

            dictValues = {'distance': distance, 'x': distance_x, 'y': distance_y}
            distances.append(dictValues)

        # x and y coordinates don't match so use Pythagoras to calculate distance
        elif((distance_x is not False) and (distance_y is not False)):
            # Pythagoras
            distance = round(math.sqrt(pow(distance_x, 2) + pow(distance_y, 2)), 4)

            dictValues = {'distance': distance, 'x': distance_x, 'y': distance_y}
            distances.append(dictValues)

        # Set distance to itself to 0:
        elif((distance_x is False) and (distance_y is False)):
            distance = 0

            dictValues = {'distance': distance, 'x': distance_x, 'y': distance_y}
            distances.append(dictValues)

        i += 1

    return distances

def getMinimum(distances = []):
    minimum = 1000
    place = 0
    for i in range(len(distances)):
        if distances[i]['distance'] < minimum and distances[i]['distance'] > 0:
            minimum = distances[i]['distance']
            place = i
    return minimum, place


# Add extrafreespace for every house.
for h in range(len(houses)):
    # Add list of distance to other houses to class instance
    houses[h].distanceToOthers = GetDistance(h)


    # Get minimum distance and nr of that house in the houses[]-list
    minimumDistance, position = getMinimum(houses[h].distanceToOthers)
    decimalPointsOfMinimum = str(minimumDistance)[::-1].find('.')

    # If minimum has more than 2 decimalpoints, then distance if calculated using Pythagoras
    if (decimalPointsOfMinimum > 2):

        houses[h].distanceToOthers[position]['x']

        # Get straight distance on x-axis and y-axis
        distance_x = straightDistance(houses[h].Xmin(houses[h].x), houses[h].Xmax(houses[h].x), houses[position].Xmin(houses[position].x), houses[position].Xmax(houses[position].x))
        distance_y = straightDistance(houses[h].Ymin(houses[h].x), houses[h].Ymax(houses[h].x), houses[position].Ymin(houses[position].x), houses[position].Ymax(houses[position].x))

        # take the smallest distance as largest possible freespace
        if houses[h].distanceToOthers[position]['x'] < houses[h].distanceToOthers[position]['y']:
            houses[h].extraFreespace = houses[h].distanceToOthers[position]['y']

        else:
            houses[h].extraFreespace = houses[h].distanceToOthers[position]['x']

    else:
        houses[h].extraFreespace = minimumDistance


print("Total value: {}".format(round(grid.totalValue(grid.housesList), 2)))
print("Total runtime: {}".format(datetime.now() - startTime))

PlotHouses()
