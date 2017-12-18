# Filename: placeAndIntersect.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Functions to place houses to the grid.

import numpy as np
from shapely.geometry import Polygon
from helpers import minimumDistance as md
from helpers import classes as cl

# Amount of times it tries to place a house at the waterside.
trialTimes = 100


def leftSideOfWater(houseType, grid):
    """Try to place house at the left side of a waterbody."""
    i = 0

    # Tries placing a house at the waterside a 100 times.
    while i < trialTimes:
        i += 1
        for waterBody in grid.waterBodiesList:
            # Generate a x and y matching with the waterside.
            houseType.x = waterBody.Xmin(waterBody.x) - houseType.width
            houseType.y = np.random.randint(low=waterBody.Ymin(waterBody.y),
                                            high=waterBody.Ymax(waterBody.y) -
                                            houseType.height)

            # Check if house intersects with other houses.
            intersect = intersectHouse(houseType, grid)

            # Add house to grid if it doesn't intersect with other houses.
            if intersect is False:
                houseType.position = len(grid.housesList)
                houseType.status = 'placed'
                grid.housesList.append(houseType)
                return True
    return False


def topSideOfWater(houseType, grid):
    """Try to place house at the top side of a waterbody."""
    i = 0
    while i < trialTimes:
        i += 1
        for waterBody in grid.waterBodiesList:
            # Generate a x and y matching with the waterside.
            houseType.x = np.random.randint(low=waterBody.Xmin(waterBody.x),
                                            high=waterBody.Xmax(waterBody.x) -
                                            houseType.width)

            houseType.y = waterBody.Ymax(waterBody.y)

            # Check if house intersects with other houses.
            intersect = intersectHouse(houseType, grid)

            # Add house to the grid if it doesn't intersect with other houses.
            if intersect is False:
                houseType.position = len(grid.housesList)
                houseType.status = 'placed'
                grid.housesList.append(houseType)
                return True
    return False


def rightSideOfWater(houseType, grid):
    """Try to place house at the right side of a waterbody."""
    i = 0

    while i < trialTimes:
        i += 1
        for waterBody in grid.waterBodiesList:
            # Generate a x and y matching with the waterside.
            houseType.x = waterBody.Xmax(waterBody.x)
            houseType.y = np.random.randint(low=waterBody.Ymin(waterBody.y),
                                            high=waterBody.Ymax(waterBody.y) -
                                            houseType.height)

            # Check if house intersects with other houses.
            intersect = intersectHouse(houseType, grid)

            # Add house to the grid if it doesn't intersect with other houses.
            if intersect is False:
                houseType.position = len(grid.housesList)
                houseType.status = 'placed'
                grid.housesList.append(houseType)
                return True
    return False


def bottomSideOfWater(houseType, grid):
    """Try to place house at the bottom side of a waterbody."""
    i = 0

    while i < trialTimes:
        i += 1
        for waterBody in grid.waterBodiesList:
            # Generate a x and y matching with the waterside.
            houseType.x = np.random.randint(low=waterBody.Xmin(waterBody.x),
                                            high=waterBody.Xmax(waterBody.x) -
                                            houseType.width)

            houseType.y = waterBody.Ymin(waterBody.y) - houseType.height

            # Check if house intersects with other houses.
            intersect = intersectHouse(houseType, grid)

            # Add house to the grid if it doesn't intersect with other houses.
            if intersect is False:
                houseType.position = len(grid.housesList)
                houseType.status = 'placed'
                grid.housesList.append(houseType)
                return True
    return False


def placeHouse(houseType, grid):
    """Places a house randomly in the grid."""

    # Declare true at first, because it has to place a house.
    intersect = True

    # Try to place a house until it does not intersect with another house.
    while intersect is True:

        # Generate random x and y bottom corner coordinates.
        houseType.x = np.random.randint(low=houseType.freespace,
                                        high=grid.areaWidth -
                                        houseType.freespace - houseType.width)

        houseType.y = np.random.randint(low=houseType.freespace,
                                        high=grid.areaHeight -
                                        houseType.freespace - houseType.height)

        # Check if house intersects with water and other houses.
        intersect = intersectWater(houseType, grid)
        if intersect is False:
            intersect = intersectHouse(houseType, grid)

    # Place house on grid if it doesn't intersect with water or another house.
    if intersect is False:
        if houseType.status == 'placed':
            m = 0
        else:
            houseType.position = len(grid.housesList)
            houseType.status = 'placed'
            grid.housesList.append(houseType)


def placeFirstMaison(houseType, grid):
    """Place first maison to prevent houselist is empty when checking for
    intersetion when placing other houses."""
    # Declare true at first, because it has to place a house.
    intersect = True

    # Try to place the maison until it does not intersect with water.
    while intersect is True:
        houseType.x = np.random.randint(low=houseType.freespace,
                                        high=grid.areaWidth -
                                        houseType.freespace - houseType.width)
        houseType.y = np.random.randint(low=houseType.freespace,
                                        high=grid.areaHeight -
                                        houseType.freespace - houseType.height)
        intersect = intersectWater(houseType, grid)

    houseType.color = 'red'
    houseType.position = len(grid.housesList)
    houseType.status = 'placed'
    grid.housesList.append(houseType)


def placeHouseWithWatersidePriority(houseType, grid):
    """Try to place house at the waterside, else random in the grid."""
    if topSideOfWater(houseType, grid) is False:
        if leftSideOfWater(houseType, grid) is False:
            if rightSideOfWater(houseType, grid) is False:
                if bottomSideOfWater(houseType, grid) is False:
                    placeHouse(houseType, grid)


def intersectWater(houseType, grid):
    """Check if house intersects with water."""
    # Declare corners for house to be placed.
    p1 = Polygon(houseType.corners(houseType.x, houseType.y))

    for waterBody in grid.waterBodiesList:
        p2 = Polygon(waterBody.corners(waterBody.x, waterBody.y))
        if p1.intersects(p2):
            return True
    return False


def intersectHouse(houseType, grid):
    """Check if house intersects with another house."""
    # Declare corners and free space corners for house to be placed.
    p1 = Polygon(houseType.corners(houseType.x, houseType.y))
    s1 = Polygon(houseType.spacecorners(houseType.x, houseType.y))

    for house in grid.housesList:
        p2 = Polygon(house.corners(house.x, house.y))
        s2 = Polygon(house.spacecorners(house.x, house.y))
        if p1.intersects(p2) is True or p1.intersects(s2) is True \
           or s1.intersects(p2) is True:
            if house.position is not houseType.position:
                return True
    return False


def moveHouse(houseType, grid):
    """Function to move a house."""
    placeHouse(houseType, grid)
    md.moveHouse(houseType, grid)


def swapCoordinates(house0, house1):
    """Function to swap coordinates of two houses."""
    temp_x = house0.x
    temp_y = house0.y

    house0.x = house1.x
    house0.y = house1.y

    house1.x = temp_x
    house1.y = temp_y


def swapHouse(houseType, grid, oldValue):
    """Check if houses fit on each other's position in the grid."""
    for house in grid.housesList:
        # Swap coordinates of both houses and calculate new freespace & value.
        swapCoordinates(houseType, house)
        md.adjustFreespace(grid)
        grid.totalValue()

        if intersectWater(houseType, grid) is False \
           and intersectWater(house, grid) is False:
            if intersectHouse(houseType, grid) is False \
               and intersectHouse(house, grid) is False:
                if grid.value > oldValue:
                    grid.totalValue()
                    oldValue = grid.value
                    print(" !! better: {}".format(grid.value))
                else:
                    swapCoordinates(house, houseType)
                    md.adjustFreespace(grid)
                    grid.totalValue()
            # If houses intersect, swap houses back to old position.
            else:
                swapCoordinates(house, houseType)
                md.adjustFreespace(grid)
                grid.totalValue()
        else:
            swapCoordinates(house, houseType)
            md.adjustFreespace(grid)
            grid.totalValue()
    return oldValue, grid


def trySwappingMaisons(grid):
    """Try to swap maisons for experiment."""
    oldValue = grid.totalValue()

    amountOfMaisons = 3 * cl.areaVariant
    for i in range(amountOfMaisons):
        for house in grid.housesList:
            swapCoordinates(grid.housesList[i], house)
            md.adjustFreespace(grid)
            grid.totalValue()

            if intersectWater(grid.housesList[i], grid) is False \
               and intersectWater(house, grid) is False:
                if intersectHouse(grid.housesList[i], grid) is False \
                   and intersectHouse(house, grid) is False:
                    if grid.value > oldValue:
                        grid.totalValue()
                        oldValue = grid.value
                    if grid.value <= oldValue:
                        print("Worse: {} < {}".format(grid.value, oldValue))
                        swapCoordinates(house, grid.housesList[i])
                        md.adjustFreespace(grid)
                        grid.totalValue()
                # If houses intersect, swap houses back to old position.
                else:
                    swapCoordinates(house, grid.housesList[i])
                    md.adjustFreespace(grid)
                    grid.totalValue()

            else:
                swapCoordinates(house, grid.housesList[i])
                md.adjustFreespace(grid)
                grid.totalValue()

    grid.Value = oldValue
