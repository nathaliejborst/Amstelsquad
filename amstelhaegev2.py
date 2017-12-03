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
import visualize as vs
import MinimumDistance as md
import PlaceAndIntersect as pai

startTime = datetime.now()

# Fixing random state for reproducibility
# np.random.seed(2)

# Create instance of the grid
grid = cl.Grid()

# Declare possible area variants by setting matching amount of housetypes
# Choose area variant by changing areaVariant to 1, 2 or 3.
areaVariant = 1
amountOWater = 2
amountOfMaisons = (3 * cl.areaVariant) - 1     # Minus 1, because first maison is placed manually
amountOfBungalows = 5 * cl.areaVariant
amountOfFamilyHouses = 12 * cl.areaVariant
totalWaterSurface = 5760

# To test, place bodies of water manually in the grid
width = [144, 100]
height = [40, 10]
x = [18, 80]
y = [20, 120]

for i in range(amountOWater):
    water = cl.Water()
    water.width = width[i]
    water.height = height[i]
    water.x = x[i]
    water.y = y[i]
    grid.waterBodiesList.append(water)

pai.placeFirstMaison(cl.House(width=11, height=10.5, freespace=6, value=610000,
           valueUpdate=0.06), grid)

# Place maisons
for maisons in range(amountOfMaisons):
    maison = cl.House(width=11, height=10.5, freespace=6, value=610000,
               valueUpdate=0.06, color='red')
    # Tries to place house at the waterside, else places it random in the grid (no priority: call pai.placeHouse() instead)
    pai.placeHouseWithWatersidePriority(maison, grid)

# Place bungalows
for bungalows in range(amountOfBungalows):
    bungalow = cl.House(width=10, height=7.5, freespace=3, value=399000,
                 valueUpdate=0.04, color='orange')
    # Tries to place house at the waterside, else places it random in the grid (no priority: call pai.placeHouse() instead)
    pai.placeHouseWithWatersidePriority(bungalow, grid)

# Place familyhouses
for familyHouses in range(amountOfFamilyHouses):
    familyHouse = cl.House(width=8, height=8, freespace=2, value=285000,
                        valueUpdate=0.03, color='yellow')
    # Tries to place house at the waterside, else places it random in the grid (no priority: call pai.placeHouse() instead)
    pai.placeHouseWithWatersidePriority(familyHouse, grid)

# Adds the extra freespace to all houses after placing them randomly on the grid
md.addExtraFreespaceToAllHouse(grid)

print("Total value: {}".format(round(grid.totalValue(), 2)))
print("Total runtime: {}".format(datetime.now() - startTime))

vs.PlotHouses(grid)

# Moves everyhouse and plots after replacing 5 houses
for house in grid.housesList:
    pai.moveHouse(house, grid)
    grid.totalValue()
    if house.position % 5 is 0:
        vs.PlotHouses(grid)
        print(grid.value)
