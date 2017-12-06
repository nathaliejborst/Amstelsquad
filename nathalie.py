

######### Roep je aan in de main file om huizen en het water te exporteren

def writeHousesToFile():
    with open('coordinatesHouses.csv', 'w', newline='') as filewriter:
        fieldnames = ['x', 'y', 'width', 'value' ]
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


writeHousesToFile()
writeWaterbodiesToFile()

######################################################################################################



########################### plaats dit in GridExporterImporter en run dit bestand om een kaart in te laden #########################
import csv
# import amstelhaegev2
import os
import classes as cl
import MinimumDistance as md
import visualize as vs

# Hoe vaak hij het hele bestand amstelhaegev2 runtime
repetition = 1

# for i in range(repetition):
# os.system('amstelhaegev2.py')
#
#
# def writeToFile(totalvalue):
#     with open("values.csv", "a") as filewriter:
#         fieldnames = ["value"]
#         writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
#         writer.writerow({"value": totalvalue})
#

grid = cl.Grid()
importedHousesList = []
importedWaterbodiesList = []

with open('coordinatesHouses.csv') as csvfile:
    i = 0
    reader= csv.reader(csvfile, delimiter=',')
    for row in reader:
        houseCoordinates = {}
        if i > 0:
            houseCoordinates = {'x': row[0], 'y': row[1], 'width': row[2]}
            importedHousesList.append(houseCoordinates)
        i +=1

with open('coordinatesWaterbodies.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        bodyCoordinates = {}
        bodyCoordinates = {'x': row[0], 'y': row[1], 'width': row[2], 'height': row[3]}
        importedWaterbodiesList.append(bodyCoordinates)

for i in range(len(importedWaterbodiesList)):
    water = cl.Water()
    water.width = int(importedWaterbodiesList[i]['width'])
    water.height = int(importedWaterbodiesList[i]['height'])
    water.x = int(importedWaterbodiesList[i]['x'])
    water.y = int(importedWaterbodiesList[i]['y'])
    grid.waterBodiesList.append(water)

for i in range(len(importedHousesList)):
    width = int(importedHousesList[i]['width'])
    # familyHouse
    if width is 8:
        familyHouse = cl.House(width=8, height=8, freespace=2, value=285000,
                            valueUpdate=0.03, color='yellow')
        familyHouse.x = float(importedHousesList[i]['x'])
        familyHouse.y = float(importedHousesList[i]['y'])
        familyHouse.position = i
        # print("fh: {}".format(importedHousesList[0]['x']))
        grid.housesList.append(familyHouse)
    # Bungalow
    if width is 10:
        bungalow = cl.House(width=10, height=7.5, freespace=3, value=399000,
                     valueUpdate=0.04, color='orange')
        bungalow.x = float(importedHousesList[i]['x'])
        bungalow.y = float(importedHousesList[i]['y'])
        bungalow.position = i
        # print("bungalow: {}".format(importedHousesList[0]['x']))
        grid.housesList.append(bungalow)
    # Maison
    if width is 11:
        maison = cl.House(width=11, height=10.5, freespace=6, value=610000,
                   valueUpdate=0.06, color='red')
        maison.x = float(importedHousesList[i]['x'])
        maison.y = float(importedHousesList[i]['y'])
        maison.position = i
        # print("maison: {}".format(importedHousesList[0]['x']))
        grid.housesList.append(maison)


md.adjustFreespace(grid)
grid.totalValue()
# vs.PlotHouses(grid)
