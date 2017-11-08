# Filename: amstelhaege.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Plots potential residential area Amstelhaege.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Declare elements of house in class.
class House:

    def __init__(self, width, height, freespace, value, valueUpdate):
        self.width = width
        self.height = height
        self.freespace = freespace
        self.value = value
        self.valueUpdate = valueUpdate

    def area(self):
        return self.width * self.height

    def addFreespace(self, meter):
        self.meter = meter
        self.freespace += meter
        self.value = round(self.value * self.valueUpdate ** int(meter), 2)

    def totalWidth(self):
        return self.width + self.freespace * 2

    def totalHeight(self):
        return self.height + self.freespace * 2


# Declaration of different houseTypes.
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


# Plots the houses per type of house.
def plotHouses(amountOfHouses, houseType, areaWidth, areaHeight, color):

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


plotHouses(amountOfMaisons, maison, areaWidth, areaHeight, "red")
plotHouses(amountOfBungalows, bungalow, areaWidth, areaHeight, "orange")
plotHouses(amountOfFamilyHouses, familyHouse, areaWidth, areaHeight, "yellow")

# Plot Amstelheage area.
plt.show()
