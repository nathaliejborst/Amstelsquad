# Filename: filewriter.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Writes values or coördinates from houses or water to csv files.

import csv


def saveValue(totalvalue):
    """Function to save values of the grid in values.csv."""

    with open("values.csv", "a") as filewriter:
        fieldnames = ["value"]
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        writer.writerow({"value": totalvalue})


def saveBeginValue(gridvalue):
    """Function to save begin values of the grid in beginValues.csv."""

    with open('beginValues.csv', 'a', newline='') as filewriter:
        fieldnames = ["value"]
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        writer.writerow({'value': gridvalue})


def writeHousesToFile(grid):
    """Function to save all houses coördinates in coordinatesHouses.csv."""

    with open('coordinatesHouses.csv', 'w', newline='') as filewriter:
        fieldnames = ['x', 'y', 'width', 'value']
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        writer.writerow({'value': grid.value})
        for house in grid.housesList:
            writer.writerow({'x': house.x, 'y': house.y, 'width': house.width})


def writeWaterbodiesToFile(grid):
    """Function to save water coördinates in coordinatesWaterbodies.csv."""

    with open('coordinatesWaterbodies.csv', 'w', newline='') as filewriter:
        fieldnames = ['x', 'y', 'width', 'height']
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        for body in grid.waterBodiesList:
            writer.writerow({'x': body.x, 'y': body.y, 'width': body.width,
                             'height': body.height})
