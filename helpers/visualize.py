# Filename: visalize.py
# Authors: Nathalie Borst, Dennis Broekhuizen, Bob Hamelers
#
# Description: Functions to visualize or live plot a grid.

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Declaration of items in legend.
maison_label = patches.Patch(color='red', label='Maison')
bungalow_label = patches.Patch(color='orange', label='Bungalow')
family_label = patches.Patch(color='yellow', label='Familyhouse')
water_label = patches.Patch(color='blue', label='Water')


def plot_houses(grid):
    """Draws all houses from houselist in a plot."""

    # Declare area.
    plt.axis([0, grid.areaWidth, 0, grid.areaHeight])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().set_title('Amstelhaege €{:,}'.format(round(grid.value, 2)),
                        fontweight="bold")
    plt.legend(handles=[maison_label, bungalow_label, family_label,
               water_label], bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.,
               title="Area variant {}".format(len(grid.housesList)))
    plt.gca().get_legend().get_title().set_weight('bold')
    plt.gca().get_legend()._legend_box.align = 'left'
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=0.775, bottom=0.02)

    # Add patches to plot to visualize water, houses and freespace.
    for waterBody in grid.waterBodiesList:
        plt.gca().add_patch(plt.Polygon(waterBody.corners(waterBody.x,
                                        waterBody.y), color=waterBody.color))
    for house in grid.housesList:
        plt.gca().add_patch(plt.Polygon(house.corners(house.x, house.y),
                            color=house.color))
        plt.gca().add_patch(patches.FancyBboxPatch(xy=(
                  house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                  house.extraFreeSpaceCorners(house.x, house.y)[0][1]),
                  width=house.extraFreeSpaceCorners(house.x, house.y)[3][0] -
                  house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                  height=house.extraFreeSpaceCorners(house.x, house.y)[1][1] -
                  house.extraFreeSpaceCorners(house.x, house.y)[0][1],
                  boxstyle='round, pad=0, rounding_size={}'.format(
                  house.freespace+house.extraFreespace),
                  transform=plt.gca().transData, ec='black', fill=True,
                  alpha=0.2, color=house.color))

    # Show plot
    plt.show()


def live_plot(grid, end, repeatHillclimber):
    """Plots live changes while performing an algrorithm."""

    # Declare area.
    plt.ion()
    plt.axis([0, grid.areaWidth, 0, grid.areaHeight])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().set_title('Amstelhaege €{:,}'.format(round(grid.value, 2)),
                        fontweight="bold")
    plt.legend(handles=[maison_label, bungalow_label, family_label,
               water_label], bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.,
               title="Area variant {}".format(len(grid.housesList)))
    plt.gca().get_legend().get_title().set_weight('bold')
    plt.gca().get_legend()._legend_box.align = 'left'
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=0.775, bottom=0.02)

    # Add patches to plot to visualize water, houses and freespace.
    for waterBody in grid.waterBodiesList:
        plt.gca().add_patch(plt.Polygon(waterBody.corners(waterBody.x,
                                        waterBody.y), color=waterBody.color))

    for house in grid.housesList:
        plt.gca().add_patch(plt.Polygon(house.corners(house.x, house.y),
                            color=house.color))
        plt.gca().add_patch(patches.FancyBboxPatch(xy=(
                  house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                  house.extraFreeSpaceCorners(house.x, house.y)[0][1]),
                  width=house.extraFreeSpaceCorners(house.x, house.y)[3][0] -
                  house.extraFreeSpaceCorners(house.x, house.y)[0][0],
                  height=house.extraFreeSpaceCorners(house.x, house.y)[1][1] -
                  house.extraFreeSpaceCorners(house.x, house.y)[0][1],
                  boxstyle='round, pad=0, rounding_size={}'.format(
                  house.freespace+house.extraFreespace),
                  transform=plt.gca().transData, ec='black', fill=True,
                  alpha=0.2, color=house.color))

    # Show updates.
    plt.pause(0.05)

    # Show plot at last iteration.
    if end == repeatHillclimber - 1:
        plt.gca().set_title('Amstelhaege €{:,} final value'.format(grid.value),
                            fontweight="bold")
        plt.show(block=True)

    # Delete all patches from plot while running live plot.
    if end != repeatHillclimber:
        plt.cla()

    # Close plot at the end of function.
    plt.close()
