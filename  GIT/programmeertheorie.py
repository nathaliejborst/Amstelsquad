import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
# import pylab

# axes = pylab.axes()
# pylab.axis("scaled")

# plt.axis([0, 160, 0, 180])

fig, ax = plt.subplots()
ax.set_xlim(xmin=0, xmax=180)
ax.set_ylim(ymin=0, ymax=160)
# ax.plot()
# , range(10)
ax.set_aspect('equal', adjustable='box')
# , projection='3d'
ax.set_title('AmstelHaege')
ax.tick_params(length=2, width=1)

sumHouses = 1

NMaison = 3 * sumHouses
NBungalow = 5 * sumHouses
NEengezins = 12 * sumHouses
value = 0
# testarrayx = []

for i in range(NMaison):
    x = np.random.randint(0, 180)
    y = np.random.randint(0, 160)
    plt.scatter(x, y, s=0, marker="s", c="yellow")
    rect = patches.Rectangle((x, y), 11, 10.5, angle=0.0, linewidth=1,
                             edgecolor="black", facecolor="yellow")
    ax.add_patch(rect)
    freespace = FancyBboxPatch((x - 6, y - 6), 23.0, 22.5, boxstyle='round,\
    pad=0, rounding_size=10', transform=ax.transData, ec='black', fill=False)
    ax.add_patch(freespace)
    # testarrayx.append(x)
    # testarrayy = np.array(y)
    # print(testarrayx)

    value += 610000

for i in range(NBungalow):
    x = np.random.randint(0, 180)
    y = np.random.randint(0, 160)
    plt.scatter(x, y, s=0, marker="s", c="orange")
    rect = patches.Rectangle((x, y), 10, 7.5, angle=0.0, linewidth=1,
                             edgecolor="black", facecolor="orange")
    ax.add_patch(rect)
    freespace = FancyBboxPatch((x - 3, y - 3), 16.0, 13.5, boxstyle='square,\
    pad=0', transform=ax.transData, ec='black', fill=False)
    ax.add_patch(freespace)

    value += 399000

for i in range(NEengezins):
    x = np.random.randint(0, 180)
    y = np.random.randint(0, 160)
    plt.scatter(x, y, s=0, marker="s", c="red")
    rect = patches.Rectangle((x, y), 8, 8, angle=0.0, linewidth=1,
                             edgecolor="black", facecolor="red")
    ax.add_patch(rect)
    freespace = FancyBboxPatch((x - 2, y - 2), 12.0, 12.0, boxstyle='square,\
    pad=0', transform=ax.transData, ec='black', fill=False)
    ax.add_patch(freespace)

    value += 285000

print(value)
# fig.savefig('yourfilename.png')

plt.show()

# circle1 = pylab.Circle((0,0), radius=20, alpha=.5)
# circle2 = pylab.Circle((0.5,0.5), radius=20, alpha=.5)
# axes.add_patch(circle1)
# axes.add_patch(circle2)
# pylab.axis('scaled')
# pylab.show()
