# Filename: main.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Plots potential residential area Amstelhaege.

# Import packages and own files

from helpers import classes as cl
from datetime import datetime
from helpers import visualize as vs
from helpers import MinimumDistance as md
from helpers import PlaceAndIntersect as pai
from helpers import filewriter as fw
from helpers import algorithms as al
import csv

def userAreaVariantInput():
    while True:
        try:
            areaVariant = int(input("Area variant (nr. between 1 to 3): "))
            print(" 1: Hillclimber")
            print(" 2: Hillclimber combined with swap houses")
            print(" 3: Simulated annealing")
            print(" 4: Combine all")
            chosenAlgorithm = int(input("Choose an algrorithm: "))
            repeatAlgorithm = int(input("How many times repeat the algorithm?: "))
            # if chooseAlgo is 1:
            #     repeatHillclimber = int(input("Repeat hillclimber: "))
            #     repositionHouse =  int(input(" > Reposition 1 house: "))
        except ValueError:
            print("   This is not a whole number.")
            continue
        if areaVariant < 1 or areaVariant > 3 or chosenAlgorithm < 1 or chosenAlgorithm > 4:
            print("   Please enter a number between 1 to 3")
            continue
        # if repeatHillclimber < 1 or repositionHouse < 1:
        #     print("   Please enter a positive number")
        #     continue
        else:
            return areaVariant, chosenAlgorithm, repeatAlgorithm
            break

cl.areaVariant, chosenAlgorithm, repeatAlgorithm = userAreaVariantInput()

# DateTime runner
startTime = datetime.now()

# Fixing random state for reproducibility
# np.random.seed(2)

# Create instance of the grid
grid = cl.Grid()

# Declare water and possible area variants by setting matching amount of housetypes
# Choose area variant by changing areaVariant to 1, 2 or 3.
areaVariant = 1

# Maisons minus 1, because first maison is placed manually
amountOfMaisons = (3 * cl.areaVariant) - 1
amountOfBungalows = 5 * cl.areaVariant
amountOfFamilyHouses = 12 * cl.areaVariant
amountOfWater = 1
totalWaterSurface = 5760

# To test, place bodies of water manually in the grid
width = [144, 100]
height = [40, 10]
x = [18, 80]
y = [20, 120]

for i in range(amountOfWater):
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

# Place first maison
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

# Call to MinimumDistance.py file with grid for add extra freespace
md.addExtraFreespaceToAllHouse(grid)

# Two printstatements for the total value and total runtime
print("Total value: {}".format(round(grid.totalValue(), 2)))
print("Total runtime: {}".format(datetime.now() - startTime))

# The total value of the grid
grid.totalValue()

al.improveValue(grid, chosenAlgorithm, repeatAlgorithm)

# Call to saveValue function in filewriter.py file with grid.value
fw.saveValue(grid.value)
