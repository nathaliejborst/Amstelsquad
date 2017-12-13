from helpers import classes as cl
from datetime import datetime
from helpers import visualize as vs
from helpers import MinimumDistance as md
from helpers import PlaceAndIntersect as pai
from helpers import filewriter as fw
import csv
import random
import math

# temperature = 1000
repositionHouse = 15

def writeHousesToFile(grid):
    with open('coordinatesHouses.csv', 'w', newline='') as filewriter:
        fieldnames = ['x', 'y', 'width', 'value']
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        writer.writerow({'value': grid.value})
        for house in grid.housesList:
            writer.writerow({'x': house.x, 'y': house.y, 'width': house.width})

def writeWaterbodiesToFile(grid):
    with open('coordinatesWaterbodies.csv', 'w', newline='') as filewriter:
        fieldnames = ['x', 'y', 'width', 'height']
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        for body in grid.waterBodiesList:
            writer.writerow({'x': body.x, 'y': body.y, 'width': body.width, 'height': body.height})

def hillClimber(house, grid, oldValue, temp_x, temp_y):
    house.x = temp_x
    house.y = temp_y
    grid.value = oldValue               # Adjust new highest value in grid
    md.adjustFreespace(grid)            # Adjusts freespace for all houses

def swapHouses(swapHouseCounter, oldValue, house, grid):
    swapHouseLevel = 150
    swapHouseCounter += 1
    if swapHouseCounter > swapHouseLevel:
        oldValue = pai.swapHouse(house, grid, oldValue)
        swapHouseCounter = 0
    return swapHouseCounter, oldValue

def simulatedAnnealing(grid, newValue, oldValue, iteration, temperature):
    # temperature = 1000
    coolingRate = 0.008 * (1 + (((iteration * 30 )/ len(grid.housesList))/3000))

    # print("temp: {}  >> coolingrate: {}".format(temperature, coolingRate))
    # Calculate acceptance probability
    acceptanceProbability = math.exp((newValue - oldValue) / temperature)
    # print("  prob: {}".format(acceptanceProbability))

    temperature *= 1 - coolingRate

    # accept deterioration
    if acceptanceProbability < random.random():
        # put house back in place
        return False, temperature
    else:
        print("accepted: prob({}), old: {}, new: {}  > temperature: {}".format(acceptanceProbability, oldValue, newValue, temperature))
        return True, temperature



def improveValue(grid, chosenAlgorithm, repeatAlgorithm):
    swapHouseCounter = 0
    temperature = 1000000
    iteration = 0

    print(repeatAlgorithm)
    vs.plot_houses(grid)
    oldValue = grid.value
    for i in range(repeatAlgorithm):
        for house in grid.housesList:
            for j in range(repositionHouse):            # Store x and y coordinates in temporary values if algrorithm can't find a better position to increase value
                iteration += 1
                temp_x = house.x
                temp_y = house.y
                pai.moveHouse(house, grid)              # Moves house and adjusts freespace for all houses
                # Accept new value if value has improved
                if grid.totalValue() >= oldValue:
                    swapHouseCounter = 0
                    oldValue = grid.totalValue()
                else:                                   # Doesn't move house if value didn't increase so gives it back it's old coordinates
                    # house.x = temp_x
                    # house.y = temp_y
                    # grid.value = oldValue               # Adjust new highest value in grid
                    # md.adjustFreespace(grid)            # Adjusts freespace for all houses
                    # Hillclimber algrorithm moves house back to old position if value hasn't improved

                    if chosenAlgorithm is 1:
                        # Hillclimber puts house back at old position if value hasn't improved
                        hillClimber(house, grid, oldValue, temp_x, temp_y)
                    if chosenAlgorithm is 2:
                        # the swap house function tries swapping a house with all the other houses to improve value
                        swapHouseCounter, oldValue = swapHouses(swapHouseCounter, oldValue, house, grid)
                    # Put house back in old position if the simulated annealing algrorithm does not accept deterioration
                    if chosenAlgorithm is 3:
                        accept, temperature = simulatedAnnealing(grid, grid.value, oldValue, iteration, temperature)
                        if accept is False:
                            hillClimber(house, grid, oldValue, temp_x, temp_y)
                    # Implements simulated annealing but if the algorithm does not accept deterioration try to swap the house
                    if chosenAlgorithm is 4:
                        accept, temperature = simulatedAnnealing(grid, grid.value, oldValue, iteration, temperature)
                        if accept is False:
                            hillClimber(house, grid, oldValue, temp_x, temp_y)
                        else:
                            swapHouseCounter, oldValue = swapHouses(swapHouseCounter, oldValue, house, grid)
            print(grid.value)
            print()
        # Call to LivePlot function in visualize.py file with grid, i and repeatHillclimber
        vs.live_plot(grid, i, repeatAlgorithm)
    # Call to Writers functions
    while True:
        saveGrid = input("Save grid? (Y/N): ")
        if saveGrid == 'Y':
            writeHousesToFile(grid)
            writeWaterbodiesToFile(grid)
            break
        if saveGrid == 'N':
            break
        else:
            print(" Please enter Y or N")
            continue
