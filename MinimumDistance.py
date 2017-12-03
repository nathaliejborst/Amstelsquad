import math

# Returns a list for every house with the distances to all other houses (house.distanceToOthers)
def addExtraFreespaceToAllHouse(grid):
    i=0
    for house in grid.housesList:
        for i in range(len(grid.housesList)):
            receiveHouses(house, grid.housesList[i])
        # i plus one because when the distance from house a to b is added to the list of a, the distance from b to a is added to the list of b so no need to recalculate the distance
        i += 1
        addExtraFreespace(house, grid)

# Calculates distance between two houses and adds it to both's distanceToOthers-lists
def receiveHouses(house0, house1):
    distance = GetDistance(house0, house1)

    # Adjust both lists with distance to the other house
    house0.distanceToOthers[house1.position] = distance
    house1.distanceToOthers[house0.position] = distance

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

    # Set distance to itself to 0:
    elif((distance_x is False) and (distance_y is False)):
        distance = 0
        distances = {'distance': distance, 'x': distance_x, 'y': distance_y}

    return distances

# Returns the distance between two coordinates on the same axis
def straightDistance(min_h, max_h, min_i, max_i):

    if((min_h - max_i) >= 0):
        distance = min_h - max_i
        return distance
    if ((min_i - max_h) >= 0):
        distance = min_i - max_h
        return distance
    else:
        return False

# Returns the distance to the nearest house and the position of that nearest house
def getMinimum(house, grid):
    minimum = 1000
    place = 0
    for i in range(len(house.distanceToOthers)):
        if house.distanceToOthers[i]['distance'] < minimum and house.distanceToOthers[i]['distance'] > 0:
            minimum = house.distanceToOthers[i]['distance']
            house.positionNearestHouse = i
            place = i
    return minimum, place

# Adds the extra freespace to a house
def addExtraFreespace(house, grid):
    # Get minimum distance and nr of that house in the houseslist
    minimumDistance, position = getMinimum(house, grid)
    # Returns amount of decimalpoints
    decimalPointsOfMinimum = str(minimumDistance)[::-1].find('.')

    # Makes sure water has no freespace
    if house.freespace is not 0:
        # If minimum has more than 2 decimalpoints, then distance if calculated using Pythagoras
        if (decimalPointsOfMinimum > 2):
            # take the smallest distance as largest5 possible freespace
            if house.distanceToOthers[position]['x'] < house.distanceToOthers[position]['y']:
                house.extraFreespace = house.distanceToOthers[position]['y']
            else:
                house.extraFreespace = house.distanceToOthers[position]['x']
        else:
            house.extraFreespace = minimumDistance
    else:
        house.extraFreespace = 0


def moveHouse(house, grid):
    for x in grid.housesList:
        receiveHouses(house, x)
    addExtraFreespace(house, grid)
    for i in grid.housesList:
        # if(house.position is i.positionNearestHouse):
        #     addExtraFreespace(i, grid)
        # if(house.positionNearestHouse is i.position):
        addExtraFreespace(i, grid)
