# Filename: main.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Main file of the solution to solve the Amstelhaege case. Ask the
# user for input. Declare variables according to input. Call functions from
# helpers to run a possible solution and show a visualisation to the user.

from helpers import classes as cl
from helpers import placeAndIntersect as pai
from helpers import minimumDistance as md
from helpers import algorithms as al
from helpers import filewriter as fw


def userInput():
    """Ask the user for input and check if the input is valid."""
    # Let user choose area variant (20, 40 or 60 houses).
    while True:
        try:
            areaVariant = int(input("Area variant (nr. between 1 to 3): "))
            if areaVariant < 1 or areaVariant > 3:
                print("   Please enter a number between 1 to 3")
                continue
        except ValueError:
            print("   This is not a whole number.")
            continue
        break

    # Let user choose an algrorithm.
    while True:
        try:
            print(" 1: Hillclimber")
            print(" 2: Hillclimber combined with swap houses")
            print(" 3: Simulated annealing")
            print(" 4: Combine all")
            chosenAlgorithm = int(input("Choose an algrorithm: "))
            if chosenAlgorithm < 1 or chosenAlgorithm > 4:
                print("   Please enter a number between 1 to 4")
                continue
        except ValueError:
            print("   This is not a whole number.")
            continue
        break

    # Let user choose how many times it wants to repeat the chosen algorithm.
    while True:
        try:
            repeatAlgorithm = \
                int(input("How many times repeat the algorithm?: "))
            if repeatAlgorithm < 0:
                print("   Please enter a number between 1 to 4")
                continue
        except ValueError:
            print("   This is not a whole number.")
            continue
        break

    return areaVariant, chosenAlgorithm, repeatAlgorithm


# Create instance of the grid.
grid = cl.Grid()

# Save userinput.
cl.areaVariant, chosenAlgorithm, repeatAlgorithm = userInput()

# Declaration of variables of the water. Total surface = 5760.
# Manually add value(s) for waterbodies.
waterWidth = [144]
waterHeight = [40]
waterX = [18]
waterY = [20]

# Declaration of the number of elements in grid according to area variant.
# Maisons minus 1, because first maison is placed manually.
amountOfMaisons = (3 * cl.areaVariant) - 1
amountOfBungalows = 5 * cl.areaVariant
amountOfFamilyHouses = 12 * cl.areaVariant
amountOfWater = len(waterWidth)

# Place water to the grid.
for i in range(amountOfWater):
    water = cl.Water()
    water.width = waterWidth[i]
    water.height = waterHeight[i]
    water.x = waterX[i]
    water.y = waterY[i]
    grid.waterBodiesList.append(water)

# Place first maison manually.
pai.placeFirstMaison(cl.House(width=11, height=10.5, freespace=6, value=610000,
                     valueUpdate=0.06), grid)

# Place bungalows.
for bungalows in range(amountOfBungalows):
    bungalow = cl.House(width=10, height=7.5, freespace=3, value=399000,
                        valueUpdate=0.04, color='orange')
    # Try to place house at waterside, else place it random in grid.
    pai.placeHouseWithWatersidePriority(bungalow, grid)

# Place maisons.
for maisons in range(amountOfMaisons):
    maison = cl.House(width=11, height=10.5, freespace=6, value=610000,
                      valueUpdate=0.06, color='red')
    # Try to place house at waterside, else place it random in grid.
    pai.placeHouseWithWatersidePriority(maison, grid)

# Place familyhouses.
for familyHouses in range(amountOfFamilyHouses):
    familyHouse = cl.House(width=8, height=8, freespace=2, value=285000,
                           valueUpdate=0.03, color='yellow')
    # Try to place house at waterside, else place it random in grid.
    pai.placeHouseWithWatersidePriority(familyHouse, grid)

# Add extra freespace to all houses added to grid.
md.addExtraFreespaceToAllHouse(grid)

# Write begin value of grid to csv.
fw.saveBeginValue(grid.totalValue())

# Show begin value to user and give instructions to continue.
print("Begin value: {}".format(round(grid.totalValue(), 2)))
print("Close plot window to start the algorithm")

# Run algorithms according to user input to improve grid value.
al.improveValue(grid, chosenAlgorithm, repeatAlgorithm)

# Write final value of grid to csv.
fw.saveValue(grid.value)
