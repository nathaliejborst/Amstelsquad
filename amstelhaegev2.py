# Filename: amstelhaege.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Plots potential residential area Amstelhaege.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon

# Fixing random state for reproducibility
np.random.seed(0)


# Declare elements of house in class.
class House:

    def __init__(self, width, height, freespace, value, valueUpdate, x=0, y=0, color=None):
        self.width = width
        self.height = height
        self.freespace = freespace
        self.value = value
        self.valueUpdate = valueUpdate
        self.x = x
        self.y = y
        self.color = color

    def area(self):
        return self.width * self.height

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


def placeFirstHouse(houseType):
    houseType.x = houseType.freespace
    houseType.y = houseType.freespace

    houses.append(houseType)


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
        # Add placed house to list of houses.
        houses.append(houseType)

placeFirstHouse(House(width=11, height=10.5, freespace=6, value=610000, valueUpdate=1.06))

# Place water
water = House(width=144, height=40, freespace=0, value=0, valueUpdate=0, color='blue')
placeHouse(water)

# Place maisons
for maisons in range(amountOfMaisons):
    maison = House(width=11, height=10.5, freespace=6, value=610000, valueUpdate=1.06, color='red')
    placeHouse(maison)

# Place bungalows
for bungalows in range(amountOfBungalows):
    bungalow = House(width=10, height=7.5, freespace=3, value=399000, valueUpdate=1.04, color='orange')
    placeHouse(bungalow)

# Place familyhouses
for familyHouses in range(amountOfFamilyHouses):
    familyHouse = House(width=8, height=8, freespace=2, value=285000,
                        valueUpdate=1.03, color='yellow')
    placeHouse(familyHouse)

valueTotal = 0

# Plots and prints grid.


def PlotHouses(valueTotal):
    for z in range(len(houses)):
        area.add_patch(plt.Polygon(houses[z].corners(houses[z].x, houses[z].y), color = houses[z].color))
        area.add_patch(plt.Polygon(houses[z].spacecorners(houses[z].x, houses[z].y), fill=False))

        # Print coordinates list
        print(houses[z].corners(houses[z].x, houses[z].y))
        print(houses[z].spacecorners(houses[z].x, houses[z].y))

        # Calculate total value.
        valueTotal += houses[z].value
        print(valueTotal)
    plt.show()


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


PlotHouses(valueTotal)
# Calculate()
# print("hello")
# PlotHouses(valueTotal)
