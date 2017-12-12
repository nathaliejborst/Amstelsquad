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
import csv

def userAreaVariantInput():
    while True:
        try:
            areaVariant = int(input("Area variant (nr. between 1 to 3): "))
            print("[1: Hillclimber]")
            chooseAlgo = int(input("Choose an algrorithm: "))
            if chooseAlgo is 1:
                repeatHillclimber = int(input("Repeat hillclimber: "))
                repositionHouse =  int(input(" > Reposition 1 house: "))
        except ValueError:
            print("   This is not a whole number.")
            continue
        if areaVariant < 1 or areaVariant > 3:
            print("   Please enter a number between 1 to 3")
            continue
        if repeatHillclimber < 1 or repositionHouse < 1:
            print("   Please enter a positive number")
            continue
        else:
            return areaVariant, repeatHillclimber, repositionHouse
            break

cl.areaVariant, repeatHillclimber, repositionHouse = userAreaVariantInput()

def writeHousesToFile():
    with open('coordinatesHouses.csv', 'w', newline='') as filewriter:
        fieldnames = ['x', 'y', 'width', 'value']
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        writer.writerow({'value': grid.value})
        for house in grid.housesList:
            writer.writerow({'x': house.x, 'y': house.y, 'width': house.width})

def writeWaterbodiesToFile():
    with open('coordinatesWaterbodies.csv', 'w', newline='') as filewriter:
        fieldnames = ['x', 'y', 'width', 'height']
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        for body in grid.waterBodiesList:
            writer.writerow({'x': body.x, 'y': body.y, 'width': body.width, 'height': body.height})

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
    pai.placeHouse(bungalow, grid)

# Place maisons
for maisons in range(amountOfMaisons):
    maison = cl.House(width=11, height=10.5, freespace=6, value=610000,
                      valueUpdate=0.06, color='red')
    # Tries to place house at the waterside, else places it random in the grid (no priority: call pai.placeHouse() instead)
    pai.placeHouse(maison, grid)

# Place familyhouses
for familyHouses in range(amountOfFamilyHouses):
    familyHouse = cl.House(width=8, height=8, freespace=2, value=285000,
                           valueUpdate=0.03, color='yellow')
    # Tries to place house at the waterside, else places it random in the grid (no priority: call pai.placeHouse() instead)
    pai.placeHouse(familyHouse, grid)

# Call to MinimumDistance.py file with grid for add extra freespace
md.addExtraFreespaceToAllHouse(grid)

# Two printstatements for the total value and total runtime
print("Total value: {}".format(round(grid.totalValue(), 2)))
print("Total runtime: {}".format(datetime.now() - startTime))

# The total value of the grid
grid.totalValue()

# Reposition number of houses per try and repeat number of Hillclimber
repositionHouse = 10
repeatHillclimber = 10

# Hillclimber function
vs.plot_houses(grid)
oldValue = grid.value
for i in range(repeatHillclimber):
    print(i)                                        # Printstatement for number of repeatHillclimber rounds
    for house in grid.housesList:
        for j in range(repositionHouse):            # Store x and y coordinates in temporary values if algrorithm can't find a better position to increase value
            temp_x = house.x
            temp_y = house.y
            pai.moveHouse(house, grid)              # Moves house and adjusts freespace for all houses
            if grid.totalValue() >= oldValue:
                oldValue = grid.totalValue()
            else:                                   # Doesn't move house if value didn't increase so gives it back it's old coordinates
                house.x = temp_x
                house.y = temp_y
                grid.value = oldValue               # Adjust new highest value in grid
                md.adjustFreespace(grid)            # Adjusts freespace for all houses
                oldValue = pai.swapHouse(house, grid, oldValue)
        print(grid.value)
        print()


        # Call to LivePlot function in visualize.py file with grid, i and repeatHillclimber
        vs.live_plot(grid, i, repeatHillclimber)
    # Call to Writers functions
    writeHousesToFile()
    writeWaterbodiesToFile()

# Call to saveValue function in filewriter.py file with grid.value
fw.saveValue(grid.value)
