# Import package
import math


'''addExtraFreespaceToAllHouse function'''


# Return a list for every house with the distances to all other houses (house.distanceToOthers)
def addExtraFreespaceToAllHouse(grid):
    i=0
    for house in grid.housesList:
        for i in range(len(grid.housesList)):
            receiveHouses(house, grid.housesList[i])
        # i plus one because when the distance from house a to b is added to the list of a, the distance from b to a is added to the list of b so no need to recalculate the distance
        i += 1
        addExtraFreespace(house, grid)


'''receiveHouses function'''


# Calculate distance between two houses and adds it to both's distanceToOthers-lists
def receiveHouses(house0, house1):
    distance = GetDistance(house0, house1)

    # Adjust both lists with distance to the other house
    house0.distanceToOthers[house1.position] = distance
    house1.distanceToOthers[house0.position] = distance


'''GetDistance function'''


def GetDistance(house0, house1):
    distances = {}

    # Get distance in y and x coordinates to other house (returns false if x or y coordinates match)
    distance_x = straightDistance(house0.Xmint(), house0.Xmaxt(), house1.Xmint(), house1.Xmaxt(),)
    distance_y = straightDistance(house0.Ymint(), house0.Ymaxt(), house1.Ymint(), house1.Ymaxt(),)

    # Check if y coordinates match
    if((distance_x is not False) and (distance_y is False)):
        distance = distance_x
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    # Check if y coordinates match
    elif((distance_x is False) and (distance_y) is not False):
        distance = distance_y
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    # x and y coordinates don't match so use Pythagoras to calculate distance
    elif((distance_x is not False) and (distance_y is not False)):
        # Pythagoras
        distance = round(math.sqrt(pow(distance_x, 2) + pow(distance_y, 2)), 4)
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    # Set distance to itself to 0
    elif((distance_x is False) and (distance_y is False)):
        distance = 0
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    return distances


''''straightDistance function'''


# Return the distance between two coordinates on the same axis
def straightDistance(min_h, max_h, min_i, max_i):

    if((min_h - max_i) >= 0):
        distance = min_h - max_i
        return distance
    if ((min_i - max_h) >= 0):
        distance = min_i - max_h
        return distance
    else:
        return False


'''getMinimum function'''


# Return the distance to the nearest house and the position of that nearest house
def getMinimum(house, grid):
    minimum = 1000
    place = 0
    for i in range(len(house.distanceToOthers)):
        if house.distanceToOthers[i]['distance'] < minimum and house.distanceToOthers[i]['distance'] > 0:
            minimum = house.distanceToOthers[i]['distance']
            house.positionNearestHouse = i
            place = i
    return minimum, place


'''addExtraFreespace function'''


# Add the extra freespace to a house
def addExtraFreespace(house, grid):
    # Get minimum distance and nr of that house in the houses[]-list
    minimumDistance, position = getMinimum(house, grid)
    house.extraFreespace = minimumDistance


'''moveHouse function'''


# Move house and adjusts freespace
def moveHouse(house0, grid):
    for house1 in grid.housesList:
        receiveHouses(house0, house1)
    addExtraFreespace(house0, grid)
    for house1 in grid.housesList:
        addExtraFreespace(house1, grid)


'''adjustFreespace function'''


# Adjust freespace for all houses
def adjustFreespace(grid):
    for house1 in grid.housesList:
        for house2 in grid.housesList:
            receiveHouses(house1, house2)
        addExtraFreespace(house1, grid)
