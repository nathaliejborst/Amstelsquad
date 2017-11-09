# Filename: amstelhaege.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Plots potential residential area Amstelhaege.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Declare elements of house in class.
class House:

    def __init__(self, width, height, freespace, value, valueUpdate, x=0, y=0):
        self.width = width
        self.height = height
        self.freespace = freespace
        self.value = value
        self.valueUpdate = valueUpdate
        self.x = x
        self.y = y

    def area(self):
        return self.width * self.height

    def corners(self, x, y):
        bottomLeft = [x, y]
        upperLeft = [x, (y + self.height)]
        upperRight = [(x + self.width), (y + self.height)]
        bottomRight = [(x + self.width), y]
        return {'bottomLeft': bottomLeft, 'upperLeft': upperLeft,
                'upperRight': upperRight, 'bottomRight': bottomRight}

    def addFreespace(self, meter):
        self.meter = meter
        self.freespace += meter
        self.value = round(self.value * self.valueUpdate ** int(meter), 2)

    def totalWidth(self):
        return self.width + self.freespace * 2

    def totalHeight(self):
        return self.height + self.freespace * 2


# Start of creating a class for the grid (doesn't do anything yet)
class Grid:

    def __init__(self, bottomRight, bottomLeft, upperLeft, upperRight):
        self.bottomRight = bottomRight
        self.bottomLeft = bottomLeft
        self.upperLeft = upperLeft
        self.upperRight = upperRight


# Declaration of different housetypes.
maison = House(width=11, height=10.5, freespace=6, value=610000,
               valueUpdate=1.06)

bungalow = House(width=10, height=7.5, freespace=3, value=399000,
                 valueUpdate=1.04)

familyHouse = House(width=8, height=8, freespace=2, value=285000,
                    valueUpdate=1.03)


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
areaVariant = 1
amountOfMaisons = 3 * areaVariant
amountOfBungalows = 5 * areaVariant
amountOfFamilyHouses = 12 * areaVariant

coordinatesList = []


# Plots the houses per type of house.
def plotHouses(amountOfHouses, houseType, color):

    for i in range(amountOfHouses):
        # Choose random x and y coordinates.
        x = np.random.randint(low=houseType.freespace, high=areaWidth -
                              houseType.freespace - houseType.width)

        y = np.random.randint(low=houseType.freespace,
                              high=areaHeight - houseType.freespace -
                              houseType.height)

        # Add bungalow to area.
        area.add_patch(patches.Rectangle((x, y),
                                         width=houseType.width,
                                         height=houseType.height,
                                         angle=0.0, linewidth=1,
                                         edgecolor="black",
                                         facecolor=color))

        # Add freespace around bungalow.
        area.add_patch(patches.FancyBboxPatch((x - houseType.freespace,
                                              y - houseType.freespace),
                                              width=houseType.totalWidth(),
                                              height=houseType.totalHeight(),
                                              boxstyle='round, pad=0,\
                                              rounding_size=0',
                                              edgecolor='black',
                                              fill=False))

        # Checks if cornerpoint intersects with house to be placed
        # for i in range(len(coordinatesList)):
        #     if ((x > coordinatesList[i]['bottomLeft'][0] and x < coordinatesList[i]['bottomRight'][0]) and (y > coordinatesList[i]['bottomLeft'][1] and y < coordinatesList[i]['upperLeft'][1])):
        #         print("intersect")
        #
        # print(len(coordinatesList))

        # Create tuple of all coordinates of houses
        coordinatesList.append(houseType.corners(x, y))


plotHouses(amountOfMaisons, maison, "red")
plotHouses(amountOfBungalows, bungalow, "orange")
plotHouses(amountOfFamilyHouses, familyHouse, "yellow")

# Plot Amstelheage area.
plt.show()
