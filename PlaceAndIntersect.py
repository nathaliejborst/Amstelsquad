import numpy as np
from shapely.geometry import Polygon
import MinimumDistance as md

# Amount of times it tries to place a house at the waterside
trialTimes = 100

# Tries to place house at the left side of a waterbody
def leftSideOfWater(houseType, grid):
    i=0

    # Tries placing a house at the waterside a 100 times
    while i < trialTimes:
        i += 1
        try:
            for waterBody in grid.waterBodiesList:
                # Generate a x and y matching with the waterside
                houseType.x = waterBody.Xmin(waterBody.x) - houseType.width
                houseType.y = np.random.randint(low=waterBody.Ymin(waterBody.y), high=waterBody.Ymax(waterBody.y) - houseType.height)

                # Check if house intersects with other houses
                intersect = intersectHouse(houseType, grid)

                # Add house to the grid if it doesn't intersect with other houses
                if intersect is False:
                    houseType.position = len(grid.housesList)
                    houseType.status = 'placed'
                    grid.housesList.append(houseType)
                    return True
        except:
            pass
    return False

# Tries to place house at the top side of a waterbody
def topSideOfWater(houseType, grid):
    i=0
    while i < trialTimes:
        i += 1
        try:
            for waterBody in grid.waterBodiesList:
                # Generate a x and y matching with the waterside
                houseType.x = np.random.randint(low=waterBody.Xmin(waterBody.x), high=waterBody.Xmax(waterBody.x) - houseType.width)
                houseType.y = waterBody.Ymax(waterBody.y)

                # Check if house intersects with other houses
                intersect = intersectHouse(houseType, grid)

                # Add house to the grid if it doesn't intersect with other houses
                if intersect is False:
                    houseType.position = len(grid.housesList)
                    houseType.status = 'placed'
                    grid.housesList.append(houseType)
                    return True
        except:
            pass
    return False

# Tries to place house at the right side of a waterbody
def rightSideOfWater(houseType, grid):
    i=0

    while i < trialTimes:
        i += 1
        try:
            for waterBody in grid.waterBodiesList:
                # Generate a x and y matching with the waterside
                houseType.x = waterBody.Xmax(waterBody.x)
                houseType.y = np.random.randint(low=waterBody.Ymin(waterBody.y), high=waterBody.Ymax(waterBody.y) - houseType.height)

                # Check if house intersects with other houses
                intersect = intersectHouse(houseType, grid)

                # Add house to the grid if it doesn't intersect with other houses
                if intersect is False:
                    houseType.position = len(grid.housesList)
                    houseType.status = 'placed'
                    grid.housesList.append(houseType)
                    return True
        except:
            pass
    return False

# Tries to place house at the bottom side of a waterbody
def bottomSideOfWater(houseType, grid):
    i=0

    while i < trialTimes:
        i += 1
        try:
            for waterBody in grid.waterBodiesList:
                # Generate a x and y matching with the waterside
                houseType.x = np.random.randint(low=waterBody.Xmin(waterBody.x), high=waterBody.Xmax(waterBody.x) - houseType.width)
                houseType.y = waterBody.Ymin(waterBody.y) - houseType.height

                # Check if house intersects with other houses
                intersect = intersectHouse(houseType, grid)

                # Add house to the grid if it doesn't intersect with other houses
                if intersect is False:
                    houseType.position = len(grid.housesList)
                    houseType.status = 'placed'
                    grid.housesList.append(houseType)
                    return True
        except:
            pass
    return False

# Places a house randomly in the grid
def placeHouse(houseType, grid):
    # Declare true at first, because it has to place a house.
    intersect = True

    # Keeps trying to place a house until it does not intersect with another house anymore.
    while intersect is True:

        # Generate random x and y bottom corner coordinates.
        houseType.x = np.random.randint(low=houseType.freespace, high=grid.areaWidth -
                              houseType.freespace - houseType.width)

        houseType.y = np.random.randint(low=houseType.freespace,
                              high=grid.areaHeight - houseType.freespace -
                              houseType.height)

        # Check if house intersects with water and other houses
        intersect = intersectWater(houseType, grid)
        if intersect is False:
            intersect = intersectHouse(houseType, grid)

    # Place house on grid if house doesn't intersect with either water or another house
    if intersect is False:
        if houseType.status == 'placed':
            m = 0
        else:
            houseType.position = len(grid.housesList)
            houseType.status = 'placed'
            grid.housesList.append(houseType)

# Place first maison manually in the corner of the grid
def placeFirstMaison(houseType, grid):
    houseType.x = np.random.randint(low=houseType.freespace, high=grid.areaWidth -
                          houseType.freespace - houseType.width)
    houseType.y = np.random.randint(low=houseType.freespace,
                          high=grid.areaHeight - houseType.freespace -
                          houseType.height)
    houseType.color = 'red'

    houseType.position = len(grid.housesList)
    houseType.status = 'placed'
    grid.housesList.append(houseType)

# Tries to place house at the waterside, else places it randomly in the grid
def placeHouseWithWatersidePriority(houseType, grid):
        if topSideOfWater(houseType, grid) is False:
            if leftSideOfWater(houseType, grid) is False:
                if rightSideOfWater(houseType, grid) is False:
                    if bottomSideOfWater(houseType, grid) is False:
                        placeHouse(houseType, grid)

# Checks if a polygon intersects with the water
def intersectWater(houseType, grid):
    # Declare corners for house to be placed.
    p1 = Polygon(houseType.corners(houseType.x, houseType.y))

    for waterBody in grid.waterBodiesList:
        p2 = Polygon(waterBody.corners(waterBody.x, waterBody.y))
        if p1.intersects(p2):
            return True
    return False

# Checks if a polygon intersects with another house
def intersectHouse(houseType, grid):
    # Declare corners and free space corners for house to be placed.
    p1 = Polygon(houseType.corners(houseType.x, houseType.y))
    s1 = Polygon(houseType.spacecorners(houseType.x, houseType.y))

    for house in grid.housesList:
        p2 = Polygon(house.corners(house.x, house.y))
        s2 = Polygon(house.spacecorners(house.x, house.y))
        if p1.intersects(p2) is True or p1.intersects(s2) is True or s1.intersects(p2) is True:
            if house.position is not houseType.position:
                return True
    return False

def moveHouse(houseType, grid):
    placeHouse(houseType, grid)
    md.moveHouse(houseType, grid)
