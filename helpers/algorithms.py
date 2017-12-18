# Filename: algorithms.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Contains the algorithms.

from helpers import filewriter as fw
from helpers import minimumDistance as md
from helpers import placeAndIntersect as pai
from helpers import visualize as vs
import random
import math

# Number of times trying to reposition all the houses in function improveValue.
repositionHouse = 2


def hillClimber(house, grid, oldValue, temp_x, temp_y):
    """Function for starting a hillclimber on a grid."""

    # Set coördinates.
    house.x = temp_x
    house.y = temp_y

    # Adjust new highest value in grid.
    grid.value = oldValue

    # Adjust new freespace for all houses.
    md.adjustFreespace(grid)


def swapHouses(swapHouseCounter, oldValue, house, grid, swapHouseLevel):
    """Function to swap houses on a grid."""

    # Counter as maximum to call to function swapHouse.
    swapHouseCounter += 1
    if swapHouseCounter > swapHouseLevel:
        oldValue, grid = pai.swapHouse(house, grid, oldValue)
        swapHouseCounter = 0
    return swapHouseCounter, oldValue


def simulatedAnnealing(grid, newValue, oldValue, iteration, temperature,
                       totalIterations):
    """Function for starting simulated annealing on a grid."""

    # Set oldTemperature and endTemperature if temperature is higher then zero.
    if temperature > 0:
        oldTemperature = temperature
        endTemperature = 0

        # Calculate acceptance probability.
        acceptanceProbability = math.exp((newValue - oldValue) / temperature)

        # Adjust a new temperature with temperature formule.
        temperature = oldTemperature - (iteration * (oldTemperature -
                                        endTemperature) / totalIterations)

        # Reject deterioration.
        if acceptanceProbability < random.random():
            print("   {}".format(acceptanceProbability))
            # Put house back in place.
            return False, temperature

        # Accept deterioration.
        else:
            print("accepted: prob({}), old: {}, new: {}  > \
                  temperature: {}".format(acceptanceProbability, oldValue,
                                          newValue, temperature))
            return True, temperature

    # Reject deterioration if temperature is not higher then zero.
    else:
        return False, temperature


def improveValue(grid, chosenAlgorithm, repeatAlgorithm):
    """Function for improving the value of houses on the grid."""

    # Set swap counter, swap level, temperature and iteration
    swapHouseCounter = 0
    swapHouseLevel = 150
    temperature = 1000000
    iteration = 0

    # The total of iterations defined with a formule.
    totalIterations = repeatAlgorithm * len(grid.housesList) * repositionHouse

    # Plot of the houses on a grid.
    vs.plot_houses(grid)

    # Adjust new highest value in grid.
    oldValue = grid.value

    # For loop for repeatAlgorithm, housesList, repositionHouse.
    for i in range(repeatAlgorithm):
        for house in grid.housesList:
            # Store x and y coordinates in temporary values if algrorithm
            # can't find a better position to increase value.
            for j in range(repositionHouse):
                iteration += 1
                temp_x = house.x
                temp_y = house.y

                # Moves house and adjust freespace for all houses.
                pai.moveHouse(house, grid)

                # Accept new value if value has improved.
                if grid.totalValue() >= oldValue:
                    swapHouseCounter = 0
                    oldValue = grid.totalValue()
                    print("   Improved: €{:,}".format(grid.value))

                # Doesn't move house if value didn't increase
                # so gives it back it's old coordinates.
                else:
                    if chosenAlgorithm is 1:
                        # Hillclimber puts house back at old position if
                        # value hasn't improved.
                        hillClimber(house, grid, oldValue, temp_x, temp_y)
                    if chosenAlgorithm is 2:
                        # The swap house function tries swapping a house with
                        # all the other houses to improve value.
                        hillClimber(house, grid, oldValue, temp_x, temp_y)
                        swapHouseCounter, oldValue = \
                            swapHouses(swapHouseCounter, oldValue, house, grid,
                                       swapHouseLevel)
                        grid.totalValue()
                    # Put house back in old position if the simulated
                    # annealing algrorithm does not accept deterioration.
                    if chosenAlgorithm is 3:
                        accept, temperature = \
                                simulatedAnnealing(grid, grid.value, oldValue,
                                                   iteration, temperature,
                                                   totalIterations)
                        if accept is False:
                            hillClimber(house, grid, oldValue, temp_x, temp_y)
                    # Implements simulated annealing but if the algorithm does
                    # not accept deterioration try to swap the house
                    if chosenAlgorithm is 4:
                        accept, temperature = \
                                simulatedAnnealing(grid, grid.value, oldValue,
                                                   iteration, temperature,
                                                   totalIterations)
                        if accept is False:
                            hillClimber(house, grid, oldValue, temp_x, temp_y)
                            swapHouseCounter, oldValue = \
                                swapHouses(swapHouseCounter,
                                           oldValue, house, grid, 0)
        print("Iteration: {}".format(i+1))

        # Call to LivePlot function in visualize.py file with grid,
        # i and repeatHillclimber.
        vs.live_plot(grid, i, repeatAlgorithm)

    print("\nFinal value: €{:,}\n".format(grid.value))

    # Call to function filewriter.
    while True:
        saveGrid = input("Save grid coördinates to replot? (Y/N): ")
        if saveGrid == 'Y':
            fw.writeHousesToFile(grid)
            fw.writeWaterbodiesToFile(grid)
            break
        if saveGrid == 'N':
            break
        else:
            print(" Please enter Y or N.")
            continue
