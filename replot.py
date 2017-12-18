# Filename: visalize.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Replot grid from csv files.

import csv
from helpers import classes as cl
from helpers import minimumDistance as md
from helpers import visualize as vs

# Create instance of the grid.
grid = cl.Grid()

# Declare lists to save coordinates from csv files.
importedHousesList = []
importedWaterbodiesList = []

# Open houses csv file and read it.
with open('coordinatesHouses.csv') as csvfile:
    i = 0
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        houseCoordinates = {}
        if i > 0:
            houseCoordinates = {'x': row[0], 'y': row[1], 'width': row[2]}
            importedHousesList.append(houseCoordinates)
        i += 1

# Open water csv file and read it.
with open('coordinatesWaterbodies.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        bodyCoordinates = {}
        bodyCoordinates = \
            {'x': row[0], 'y': row[1], 'width': row[2], 'height': row[3]}
        importedWaterbodiesList.append(bodyCoordinates)

# Set readed water in classes file.
for i in range(len(importedWaterbodiesList)):
    water = cl.Water()
    water.width = int(importedWaterbodiesList[i]['width'])
    water.height = int(importedWaterbodiesList[i]['height'])
    water.x = int(importedWaterbodiesList[i]['x'])
    water.y = int(importedWaterbodiesList[i]['y'])
    grid.waterBodiesList.append(water)

# Set readed houses in classes file.
for i in range(len(importedHousesList)):
    width = int(importedHousesList[i]['width'])

    # Check for familyhouses and append to list.
    if width is 8:
        familyHouse = cl.House(width=8, height=8, freespace=2, value=285000,
                               valueUpdate=0.03, color='yellow')
        familyHouse.x = float(importedHousesList[i]['x'])
        familyHouse.y = float(importedHousesList[i]['y'])
        familyHouse.position = i
        grid.housesList.append(familyHouse)

    # Check for bungalows and append to list.
    if width is 10:
        bungalow = cl.House(width=10, height=7.5, freespace=3, value=399000,
                            valueUpdate=0.04, color='orange')
        bungalow.x = float(importedHousesList[i]['x'])
        bungalow.y = float(importedHousesList[i]['y'])
        bungalow.position = i
        grid.housesList.append(bungalow)

    # Check for maisons and append to list.
    if width is 11:
        maison = cl.House(width=11, height=10.5, freespace=6, value=610000,
                          valueUpdate=0.06, color='red')
        maison.x = float(importedHousesList[i]['x'])
        maison.y = float(importedHousesList[i]['y'])
        maison.position = i
        grid.housesList.append(maison)

# Call to adjustFreespace function in MinimumDistance.py file with grid
md.adjustFreespace(grid)

# Give grid.totalValue
grid.totalValue()

# Call to plot_houses function in visualize.py with grid
vs.plot_houses(grid)
