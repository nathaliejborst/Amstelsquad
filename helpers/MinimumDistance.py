# Filename: minimumDistance.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Functions to calculate minimum distance between houses.

import math


def addExtraFreespaceToAllHouse(grid):
    """Returns a list for every house with the distance to all other houses."""
    i = 0
    for house in grid.housesList:
        for i in range(len(grid.housesList)):
            receiveHouses(house, grid.housesList[i])
        # i + 1 to prevent calculating the same distance twice.
        i += 1
        addExtraFreespace(house, grid)


def receiveHouses(house0, house1):
    """Calculate distance between two houses and add it to both
    distance to others lists."""
    distance = GetDistance(house0, house1)

    # Adjust both lists with distance to the other house.
    house0.distanceToOthers[house1.position] = distance
    house1.distanceToOthers[house0.position] = distance


def GetDistance(house0, house1):
    '''GetDistance function'''
    distances = {}

    # Get distance in y and x coordinates to other house.
    # Returns false if x or y coordinates match.
    distance_x = straightDistance(house0.Xmint(), house0.Xmaxt(),
                                  house1.Xmint(), house1.Xmaxt(),)
    distance_y = straightDistance(house0.Ymint(), house0.Ymaxt(),
                                  house1.Ymint(), house1.Ymaxt(),)

    # Check if y coordinates match.
    if((distance_x is not False) and (distance_y is False)):
        distance = distance_x
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    # Check if y coordinates match.
    elif((distance_x is False) and (distance_y) is not False):
        distance = distance_y
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    # x and y coordinates don't match so use Pythagoras to calculate distance.
    elif((distance_x is not False) and (distance_y is not False)):
        # Pythagoras.
        distance = round(math.sqrt(pow(distance_x, 2) + pow(distance_y, 2)), 4)
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    # Set distance to itself to 0.
    elif((distance_x is False) and (distance_y is False)):
        distance = 0
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    return distances


def straightDistance(min_h, max_h, min_i, max_i):
    """Return the distance between two coordinates on the same axis."""
    if((min_h - max_i) >= 0):
        distance = min_h - max_i
        return distance
    if ((min_i - max_h) >= 0):
        distance = min_i - max_h
        return distance
    else:
        return False


def getMinimum(house, grid):
    """Return distance to nearest house and position of that nearest house."""
    minimum = 1000
    place = 0
    for i in range(len(house.distanceToOthers)):
        if house.distanceToOthers[i]['distance'] < \
           minimum and house.distanceToOthers[i]['distance'] > 0:
            minimum = house.distanceToOthers[i]['distance']
            house.positionNearestHouse = i
            place = i
    return minimum, place


def addExtraFreespace(house, grid):
    """Add extra freespace to a house."""
    # Get minimum distance and nr. of that house in the houses[]-list.
    minimumDistance, position = getMinimum(house, grid)
    house.extraFreespace = minimumDistance


def moveHouse(house0, grid):
    """Move house and adjusts freespace."""
    for house1 in grid.housesList:
        receiveHouses(house0, house1)
    addExtraFreespace(house0, grid)
    for house1 in grid.housesList:
        addExtraFreespace(house1, grid)


def adjustFreespace(grid):
    """Adjust freespace for all houses."""
    for house1 in grid.housesList:
        for house2 in grid.housesList:
            receiveHouses(house1, house2)
        addExtraFreespace(house1, grid)
