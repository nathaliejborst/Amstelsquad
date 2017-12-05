import matplotlib.pyplot as plt
import matplotlib.patches as patches


def PlotHouses(grid):
    fig, area = plt.subplots()
    area.set_xlim(xmin=0, xmax=grid.areaWidth)
    area.set_ylim(ymin=0, ymax=grid.areaHeight)
    area.set_aspect('equal', adjustable='box')
    area.set_title('Amstelhaege ${}'.format(grid.value))
    area.set_facecolor((0.624,0.816,0.404))

    for waterBody in grid.waterBodiesList:
        area.add_patch(plt.Polygon(waterBody.corners(waterBody.x, waterBody.y), color=waterBody.color))

    for house in grid.housesList:
        area.add_patch(plt.Polygon(house.corners(house.x, house.y), color=house.color))
        # area.add_patch(plt.Polygon(house.spacecorners(house.x, house.y), fill=False))
        # area.add_patch(plt.Polygon(house.extraFreeSpaceCorners(house.x, house.y), fill=False, edgecolor='green'))
        area.add_patch(patches.FancyBboxPatch(xy=(house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                                                  house.extraFreeSpaceCorners(house.x, house.y)[0][1]),
                                                  width=house.extraFreeSpaceCorners(house.x, house.y)[3][0]-house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                                                  height=house.extraFreeSpaceCorners(house.x, house.y)[1][1]-house.extraFreeSpaceCorners(house.x, house.y)[0][1],
                                                  boxstyle='round, pad=0, rounding_size={}'.format(house.freespace+house.extraFreespace),
                                                  transform=area.transData, ec='black', fill=True, alpha=0.2, color=house.color))

    plt.show()


def livePlot(grid, end, repeatHillclimber):
    # Declare area.
    plt.ion()
    plt.axis([0, 180, 0, 160])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().set_title('Amstelhaege ${}'.format(grid.value))
    plt.xticks([])
    plt.yticks([])
    plt.gca().set_facecolor((0.624,0.816,0.404))

    # Add patches to area.
    for waterBody in grid.waterBodiesList:
        plt.gca().add_patch(plt.Polygon(waterBody.corners(waterBody.x, waterBody.y), color=waterBody.color))

    for house in grid.housesList:
        plt.gca().add_patch(plt.Polygon(house.corners(house.x, house.y), color=house.color))
        plt.gca().add_patch(patches.FancyBboxPatch(xy=(house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                                                  house.extraFreeSpaceCorners(house.x, house.y)[0][1]),
                                                  width=house.extraFreeSpaceCorners(house.x, house.y)[3][0]-house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                                                  height=house.extraFreeSpaceCorners(house.x, house.y)[1][1]-house.extraFreeSpaceCorners(house.x, house.y)[0][1],
                                                  boxstyle='round, pad=0, rounding_size={}'.format(house.freespace+house.extraFreespace),
                                                  transform=plt.gca().transData, ec='black', fill=True, alpha=0.2, color=house.color))

    # Show updates.
    plt.pause(0.05)

    # Show plot at last itteration.
    if end == repeatHillclimber - 1:
        plt.gca().set_title('Amstelhaege ${} final value'.format(grid.value))
        plt.show(block=True)

    # Clear area at the end of function.
    plt.cla()
