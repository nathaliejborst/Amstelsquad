import numpy as np
import math

areaVariant = 1

class Grid:
    def __init__(self, housesList = [], waterBodiesList = []):
        self.housesList = housesList
        self.waterBodiesList = waterBodiesList
        self.areaWidth = 180
        self.areaHeight = 160
        self.value = 0

    def totalValue(self):
        value = 0
        for house in self.housesList:
            value += house.value
            value += (house.extraFreespace - house.freespace) * house.valueUpdate * house.value
        self.value = value
        return self.value

# Declare elements of house in class.
class House():
    def __init__(self, width, height, freespace, value, valueUpdate, x=0, y=0, color=None, distanceToOthers = [], extraFreespace=0):
        self.width = width
        self.height = height
        self.freespace = freespace
        self.value = value
        self.valueUpdate = valueUpdate
        self.x = x
        self.y = y
        self.Xmin = self.x
        self.Xmax = self.x + self.width
        self.Ymin = self.y
        self.Ymax = self.y + self.height
        self.color = color
        self.distanceToOthers = [None] * (areaVariant * 20)
        self.extraFreespace = extraFreespace
        self.status = 'not placed'
        self.position = None
        self.positionNearestHouse = None

    def area(self):
        return self.width * self.height

    def Xmint(self):
        return self.x
    def Xmaxt(self):
        return self.x + self.width
    def Ymint(self):
        return self.y
    def Ymaxt(self):
        return self.y + self.height

    # def Xmin(self, x):
    #     return x
    # def Xmax(self, x):
    #     return (x + self.width)
    # def Ymin(self, y):
    #     return y
    # def Ymax(self, y):
    #     return (y + self.height)

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
        # Adjusts freespace if the bottom side of the freespace crosses the left border of the grid (x < 0).
        if x - self.extraFreespace < 0:
            self.extraFreespace = x
        # CAdjusts freespace if the right side of the freespace crosses the right border of the grid (x > 180).
        if x + self.width +  self.extraFreespace > 180:
            self.extraFreespace = 180 - x - self.width
        # Adjusts freespace if the left side of the freespace crosses the bottom of the grid (y < 0).
        if y - self.extraFreespace < 0:
            self.extraFreespace = y
        # Adjusts freespace if the top side of the freespace crosses the bottom border of the grid (y > 160).
        if y + self.height + self.extraFreespace > 160:
            self.extraFreespace = 160 - y - self.height

        # Adjust corners of freespace to the new value because of the limitations of the border of the grid.
        leftX = x - self.extraFreespace
        rightX = x + self.width + self.extraFreespace
        bottomY = y - self.extraFreespace
        upperY = y + self.height + self.extraFreespace

        # Initialize arrays of corner coordinates.
        bottomLeft = [leftX, bottomY]
        upperLeft = [leftX, upperY]
        upperRight = [rightX, upperY]
        bottomRight = [rightX, bottomY]

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

class Water:
    def __init__(self):
        self.totalSurface = 5670
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.color = 'blue'
        self.surface = (self.width * self.height)

    def corners(self, x, y):
        bottomLeft = [x, y]
        upperLeft = [x, (y + self.height)]
        upperRight = [(x + self.width), (y + self.height)]
        bottomRight = [(x + self.width), y]

        return [bottomLeft, upperLeft, upperRight, bottomRight]

    def Xmin(self, x):
        return x
    def Xmax(self, x):
        return (x + self.width)
    def Ymin(self, y):
        return y
    def Ymax(self, y):
        return (y + self.height)
