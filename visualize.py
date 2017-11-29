import matplotlib.pyplot as plt
import matplotlib.patches as patches


def PlotHouses(grid):
    fig, area = plt.subplots()
    area.set_xlim(xmin=0, xmax=grid.areaWidth)
    area.set_ylim(ymin=0, ymax=grid.areaHeight)
    area.set_aspect('equal', adjustable='box')
    area.set_title('Amstelhaege ${}'.format(grid.value))

    for house in grid.housesList:
        area.add_patch(plt.Polygon(house.corners(house.x, house.y), color=house.color))
        # area.add_patch(plt.Polygon(house.spacecorners(house.x, house.y), fill=False))
        # area.add_patch(plt.Polygon(house.extraFreeSpaceCorners(house.x, house.y), fill=False, edgecolor='green'))
        area.add_patch(patches.FancyBboxPatch(xy=(house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                                                  house.extraFreeSpaceCorners(house.x, house.y)[0][1]),
                                                  width=house.extraFreeSpaceCorners(house.x, house.y)[3][0]-house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                                                  height=house.extraFreeSpaceCorners(house.x, house.y)[1][1]-house.extraFreeSpaceCorners(house.x, house.y)[0][1],
                                                  boxstyle='round, pad=0, rounding_size={}'.format(house.freespace+house.extraFreespace),
                                                  transform=area.transData, ec='black', fill=False))

    plt.show()
