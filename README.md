# Heuristics Fall 2017: AmstelHaege

This program offers the possibility to plot a map with three housevariants (20 houses, 40 houses, 60 houses) at the request of the municipality for the new district Amstelhaege. The value of a map is the sum of all houses in the neighborhood including the number of meters of free standing per house. Thereby an attempt is made to realize a maximum value and a maximum free standing. Surface water is also added and there are three different houses, namely single-family homes, bungalows and maisonettes.

## Example Visualisation
![alt text](https://raw.githubusercontent.com/nathaliejborst/Amstelsquad/master/visualisations/GroupedHouses_1000Hillclimbs.png?token=AWTZAv3Bvz-JJFMI7wGaeB4PpJYSutHRks5aPPgrwA%3D%3D)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites (extern libraries)

* Python 3
* Numpy
* Matplotlib
* Shapely

### Installing
To install shapely on Windows, do the following:

(Ctrl + )Click on the link below and download the right WHL file

[link to Shapeley WHL files](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)

Set the right file in the right workspace, after that:


To install all extern libraries:

```
# Install all extern libraries
$ pip install --user -r requirements.txt
```

#### Alternative installation
As an alternative, the following files can be installed separately:

On Mac:
```
# Install numpy
$ pip install numpy

# Install matplotlib
$ pip install matplotlib

# Install shapely
$ pip install shapely
```

On Windows:
```
# Install numpy
$ pip install numpy

# Install matplotlib
$ pip install matplotlib
```
To install shapely, do the following:

(Ctrl + )Click on the link below and download the right WHL file

[link to Shapeley WHL files](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)

Set the right file in the right workspace, after that:
```
$ pip install shapely
```

## Running the tests

Type in the terminal in the correct folder where this file is stored:
```
$ python main.py
# or
$ python3 main.py

# To stop the program, the user must type the following in the terminal:
$ Ctrl C

# To replot a grid, the user must have "coordinatesHouses.csv" and "coordinatesWaterbodies.csv" in the same directory as replot.py and must type the following:
$ python replot.py
# or
$ python3 replot.py
```

An user can change areavariants and choose an algorithm in the terminal. The user can also choose an amount of repeats of the algorithm. 
If the user wants to change amount of houses moved per iteration, the user has to type the following in algorithms.py in line 14:
```
# Type an integer below here instead of "amount" with the (areavariant * 20) as maximum:
$ repositionHouse = "amount"
```

If a user wants to change the order of houses placed on the map, a user can change the order in main.py between line 94 and line 113.
```
# To do that, a user has to select one kind of house (6 lines of code) and place it above or below the other housevariant(s) (also 6 lines of code or 12 lines of code) as near as possible with one empty line. Below an example of 1 housevariant (6 lines of code): 

$ # Place familyhouses.
$ for familyHouses in range(amountOfFamilyHouses):
$     familyHouse = cl.House(width=8, height=8, freespace=2, value=285000,
$                            valueUpdate=0.03, color='yellow')
$     # Try to place house at waterside, else place it random in grid.
$     pai.placeHouseWithWatersidePriority(familyHouse, grid)
```

If a user want to plot the water different, a user can type in main.py between line 69 and line 72 the following:
```
# Type an integer in these lines, with a comma you can place more areas of water. As example, for two areas of water
$ waterWidth = [72, 72]
$ waterHeight = [20, 20]
$ waterX = [18, 18]
$ waterY = [20, 52]
```

## The Program

### State-Space

On a grid of 156 by 176 gives 27.456 'blocks' can be placed somewhere. In reality, the plotting of houses is lower since this number applies to the smallest house. Next to that, no account is taken of water and of already placed houses. The State-space is as maximum 27.456 per house.

A more specific calculation is with half meters. On a grid of 156 by 176, there are twice (312 * 352) possibilities to place a smaller house. That are 109.824 possibilities for the smallest house.

(154 * 174)^2 = 308 * 348 = 107.184 (bungalow)
(148 * 168)^2 = 296 * 336 = 99.456 (maison)

single-family home = h1 = 12
bungalow = h2 = 5
maison = h3 = 3

For the 20-houses-variant n = 1, for the 40-houses-variant n = 2 and for the 60-houses-variant n = 3.
You can rotate a bungalow or a maison 90 degrees for a different solution so, x = 2 for a bungalow and a maison.

A better state-space calculation (non-discrete) reads as follows:
109.824 to the power of (n*h1) + (x * 107.184) to the power of (n*h2) + (x * 99.456) to the power of (n*h3) = state space non discrete.
109.824^(n*12) + 214.368^(n*5) + 99.456^(n*3) = state space non discrete.

20-houses-variant = 3,079~ * 10^60 + 4,527~ * 10^26 + 9,838~ * 10^14 = 1,74~ * 10^101

40-houses-variant = 9,478~ * 10^120 + 2,049~ * 10^53 + 9,678~ * 10^29 = 2,12~ * 10^203

60-houses-variant = 2,918~ * 10^181 + 9,278~ * 10^79 + 9,521~ * 10^44 = 2,17~ * 10^305


When there is a non discrete possibility to place houses (float), the asymptote would go towards infinity.

### Upper- and Lower-Bound Value
The maximum value is: 36 * 285.000 + 15 * 399.000 + 9 * 610.000 = 10.260.000 + 5.985.000 + 5.490.000 = 21.735.000

The space already taken from the grid (180*160= 28.800 ) = 36*(10*10) + 15*(13*10,5) + 9*(17*16,5) = 3600 + 2047,5 + 2524,5 = 8172 + water (160*180*0,2=5760) = 13.932. Total grid minus already taken space = 28.800 - 13.932 = 14.868 is available for freespace.

Freespace could overlap max 4 times, so 4 times the most expensive freespace. 4 * (610.000 * 0.06) =  4 * 36.600 = 146.400 / 34,5 = 4.243,48~ per square meter (this number is only true by the first extra meter of a maison).  

4.243,48 * 14.868 = 63.092.034,8

21.735.000 + 63.092.034,8 = 84.827.034,8~

84.827.034,8~ is an estimate of the absolute maximum of the value of Amstelhaege.



The minimum value is: 12 * 285.000 + 5 * 399.000 + 3 * 610.000 = 3.420.000 + 1.995.000 + 1.830.000 = 7.245.000 euro

### Constraints

1. The district is placed on a piece of land of 160x180 meters.

2. The number of homes in the neighborhood consists of 60% single-family homes, 25% of bungalows and 15% of maisonettes. In other words, with the 20-house variant there are 12 single-family homes, 5 bungalows and 3 maisons.

3. A single-family home is 8x8 meters (width x length) and has a value of € 285,000. The home has a minimum free standing of two meters; every meter extra provides a price improvement of 3% with respect to the original starting value (not cumulative).

4. A bungalow is 10x7.5 meters (width x length) and has a value of € 399,000. The home has a minimum free standing of three meters; every meter extra provides a price improvement of 4% with respect to the original starting value (not cumulative).

5. A Maison is 11x10.5 meters (width x length) and has a value of € 610,000. The home has a minimum free standing of six meters; every meter extra provides a price improvement of 6% with respect to the original starting value (not cumulative).

6. The free standing of a house is the smallest distance to the nearest other house in the neighborhood. In other words, for a free standing of 6 meters, all other houses in the neighborhood are at least 6 meters away. This distance is defined as the shortest distance between two walls and is therefore not calculated from the center of the house.

7. The compulsory free standing for every home falls within the map.

8. The percent value increase per property per meter is not cumulative. The percentage is always calculated with regard to the starting price of the house.

9. The district contains 20% surface water, divided into no more than four sections that are rectangular or oval in shape. The aspect ratios are between 1 and 4.

## Versioning

For the versions available, see the [commits on this repository](https://github.com/nathaliejborst/Amstelsquad/commits/master).

## Authors

* **Nathalie Borst** - [nathaliejborst](https://github.com/nathaliejborst)
* **Dennis Broekhuizen** - [DennisBroekhuizen](https://github.com/DennisBroekhuizen)
* **Bob Hamelers** - [bobhamelers](https://github.com/bobhamelers)

See also the list of [contributors](https://github.com/nathaliejborst/Amstelsquad/graphs/contributors) who participated in this project.

Also thanks to
**Bart van Baal** - [BartvBaal](https://github.com/BartvBaal)
for assisting us.

## License

This project is licensed under the University of Amsterdam, minor programming, programming theory/heuristics
