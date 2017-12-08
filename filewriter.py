# Import csv package
import csv


'''saveValue'''


def saveValue(totalvalue):
    with open("values.csv", "a") as filewriter:
        fieldnames = ["value"]
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        writer.writerow({"value": totalvalue})
#
#
# '''writeHousesToFile'''
#
#
# def writeHousesToFile():
#     with open('coordinatesHouses.csv', 'w', newline='') as filewriter:
#         fieldnames = ['x', 'y', 'width', 'value']
#         writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
#         writer.writerow({'value': grid.value})
#         for house in grid.housesList:
#             writer.writerow({'x': house.x, 'y': house.y, 'width': house.width})
#
#
# '''writeWaterbodiesToFile'''
#
#
# def writeWaterbodiesToFile():
#     with open('coordinatesWaterbodies.csv', 'w', newline='') as filewriter:
#         fieldnames = ['x', 'y', 'width', 'height']
#         writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
#         for body in grid.waterBodiesList:
#             writer.writerow({'x': body.x, 'y': body.y, 'width': body.width, 'height': body.height})
