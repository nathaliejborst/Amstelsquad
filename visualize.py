import matplotlib.pyplot as plt
import classes as cl





def PlotHouses(grid):
    fig, area = plt.subplots()
    area.set_xlim(xmin=0, xmax=grid.areaWidth)
    area.set_ylim(ymin=0, ymax=grid.areaHeight)
    area.set_aspect('equal', adjustable='box')
    area.set_title('Amstelhaege')

    for house in grid.housesList:
        area.add_patch(plt.Polygon(house.corners(house.x, house.y), color=house.color))
        # area.add_patch(plt.Polygon(house.spacecorners(house.x, house.y), fill=False))
        area.add_patch(plt.Polygon(house.extraFreeSpaceCorners(house.x, house.y), fill=False, edgecolor='green'))

    plt.show()
