import math

def straightDistance(min_h, max_h, min_i, max_i):
    # Checks distance in x or y coordinates, returns false if x or y coordinates don't match.
    if((min_h - max_i) >= 0):
        distance = min_h - max_i
        return distance
    if ((min_i - max_h) >= 0):
        distance = min_i - max_h
        return distance
    else:
        return False

def GetDistance(h, houses):

    distances = []

    Xmin_h = houses[h].Xmin(houses[h].x)
    Xmax_h = houses[h].Xmax(houses[h].x)
    Ymin_h = houses[h].Ymin(houses[h].y)
    Ymax_h = houses[h].Ymax(houses[h].y)

    for house in houses:
        Xmin_i = house.Xmin(house.x)
        Xmax_i = house.Xmax(house.x)
        Ymin_i = house.Ymin(house.y)
        Ymax_i = house.Ymax(house.y)

        # Get distance in y and x coordinates to other house (returns false if x or y coordinates match)
        distance_x = straightDistance(Xmin_h, Xmax_h, Xmin_i, Xmax_i)
        distance_y = straightDistance(Ymin_h, Ymax_h, Ymin_i, Ymax_i)

        # Check if y coordinates match
        if((distance_x is not False) and (distance_y is False)):
            distance = distance_x

            dictValues = {'distance': distance, 'x': distance_x, 'y': distance_y}
            distances.append(dictValues)

        # Check if y coordinates match
        elif((distance_x is False) and (distance_y) is not False):
            distance = distance_y

            dictValues = {'distance': distance, 'x': distance_x, 'y': distance_y}
            distances.append(dictValues)

        # x and y coordinates don't match so use Pythagoras to calculate distance
        elif((distance_x is not False) and (distance_y is not False)):
            # Pythagoras
            distance = round(math.sqrt(pow(distance_x, 2) + pow(distance_y, 2)), 4)

            dictValues = {'distance': distance, 'x': distance_x, 'y': distance_y}
            distances.append(dictValues)

        # Set distance to itself to 0:
        elif((distance_x is False) and (distance_y is False)):
            distance = 0

            dictValues = {'distance': distance, 'x': distance_x, 'y': distance_y}
            distances.append(dictValues)

    return distances

def getMinimum(distances = []):
    minimum = 1000
    place = 0
    for i in range(len(distances)):
        if distances[i]['distance'] < minimum and distances[i]['distance'] > 0:
            minimum = distances[i]['distance']
            place = i
    return minimum, place

def addFreeSpaceToHouse(grid):
    for h in range(len(grid.housesList)):
        # Add list of distance to other houses to class instance
        grid.housesList[h].distanceToOthers = GetDistance(h, grid.housesList)

        # Get minimum distance and nr of that house in the houses[]-list
        minimumDistance, position = getMinimum(grid.housesList[h].distanceToOthers)
        # Returns amount of decimalpoints
        decimalPointsOfMinimum = str(minimumDistance)[::-1].find('.')

        # Makes sure water has no freespace
        if grid.housesList[h].freespace is not 0:
            # If minimum has more than 2 decimalpoints, then distance if calculated using Pythagoras
            if (decimalPointsOfMinimum > 2):
                # take the smallest distance as largest possible freespace
                if grid.housesList[h].distanceToOthers[position]['x'] < grid.housesList[h].distanceToOthers[position]['y']:
                    grid.housesList[h].extraFreespace = grid.housesList[h].distanceToOthers[position]['y']
                else:
                    grid.housesList[h].extraFreespace = grid.housesList[h].distanceToOthers[position]['x']
            else:
                grid.housesList[h].extraFreespace = minimumDistance
        else:
            grid.housesList[h].extraFreespace = 0
