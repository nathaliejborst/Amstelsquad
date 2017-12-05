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
import GridExporterImporter as gei

startTime = datetime.now()

# Fixing random state for reproducibility
# np.random.seed(2)

# Create instance of the grid
grid = cl.Grid()

# Declare possible area variants by setting matching amount of housetypes
# Choose area variant by changing areaVariant to 1, 2 or 3.
areaVariant = 1
amountOWater = 1
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
    # waterBodies.append(water)

# water = cl.Water()
# water.width = 144
# water.height = 40
# water.x = 18
# water.y = 60
# waterBodies.append(water)

pai.placeFirstMaison(cl.House(width=11, height=10.5, freespace=6, value=610000,
           valueUpdate=0.06), grid)

# Place bungalows
for bungalows in range(amountOfBungalows):
    bungalow = cl.House(width=10, height=7.5, freespace=3, value=399000,
                 valueUpdate=0.04, color='orange')
    # Tries to place house at the waterside, else places it random in the grid (no priority: call pai.placeHouse() instead)
    pai.placeHouseWithWatersidePriority(bungalow, grid)

# Place maisons
for maisons in range(amountOfMaisons):
    maison = cl.House(width=11, height=10.5, freespace=6, value=610000,
               valueUpdate=0.06, color='red')
    # Tries to place house at the waterside, else places it random in the grid (no priority: call pai.placeHouse() instead)
    pai.placeHouseWithWatersidePriority(maison, grid)

# Place familyhouses
for familyHouses in range(amountOfFamilyHouses):
    familyHouse = cl.House(width=8, height=8, freespace=2, value=285000,
                        valueUpdate=0.03, color='yellow')
    # Tries to place house at the waterside, else places it random in the grid (no priority: call pai.placeHouse() instead)
    pai.placeHouseWithWatersidePriority(familyHouse, grid)

#
md.addExtraFreespaceToAllHouse(grid)

print("Total value: {}".format(round(grid.totalValue(), 2)))
print("Total runtime: {}".format(datetime.now() - startTime))

vs.PlotHouses(grid)
grid.totalValue()



# for house in grid.housesList:
#     pai.moveHouse(house, grid)
#     grid.totalValue()
#     if house.position % 5 is 0:
#         vs.PlotHouses(grid)
#         print(grid.value)

repositionHouse = 2
repeatHillclimber = 2

temp_value = grid.value
for i in range(repeatHillclimber):
    print(i)
    for house in grid.housesList:
        for i in range(repositionHouse):            # Store x and y coordinates in temporary values if algrorithm can't find a better position to increase value
            temp_x = house.x
            temp_y = house.y
            pai.moveHouse(house, grid)              # Moves house and adjusts freespace for all houses
            if grid.totalValue() >= temp_value:
                temp_value = grid.totalValue()
            else:                                   # Doesn't move house if value didn't increase so gives it back it's old coordinates
                house.x = temp_x
                house.y = temp_y
                grid.value = temp_value             # Adjust new highest value in grid
                md.adjustFreespace(grid)            # Adjusts freespace for all houses
        print(grid.value)
        print()

gei.writeToFile(grid.value)

vs.PlotHouses(grid)
