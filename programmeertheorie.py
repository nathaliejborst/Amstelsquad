import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

plt.axis([0, 160, 0, 180])

NMaison = 3
NBungalow = 5
NEengezins = 12

dataOne = np.random.random(NMaison)
dataTwo = np.random.random(NBungalow)
dataThree = np.random.random(NEengezins)

for i in range(NMaison):
    x = np.random.randint(0, 160)
    y = np.random.randint(0, 180)
    plt.scatter(x, y, marker="s", c="yellow")
for i in range(NBungalow):
    x = np.random.randint(0, 160)
    y = np.random.randint(0, 180)
    plt.scatter(x, y, s=100, marker="s", c="orange")
for i in range(NEengezins):
    x = np.random.randint(0, 160)
    y = np.random.randint(0, 180)
    plt.scatter(x, y, s=1000, marker="s", c="red")

plt.show()
