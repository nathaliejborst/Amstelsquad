# Heuristics Fall 2017: AmstelHaege

This program offers the possibility to plot a map with three housevariants (20 houses, 40 houses, 60 houses) at the request of the municipality for the new district Amstelhaege. The value of a map is the sum of all houses in the neighborhood including the number of meters of free standing per house. Thereby an attempt is made to realize a maximum value and a maximum free standing. Surface water is also added and there are three different houses, namely single-family homes, bungalows and maisonettes.

## Example Visualisation
![alt text](https://raw.githubusercontent.com/nathaliejborst/Amstelsquad/master/visualisations/Figure_1.png?token=AWTZAlee4q8v7oR0N5KgqtAeyO6Cel-sks5aL81dwA%3D%3D)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

* Python 3
* Numpy
* Matplotlib
* Shapely

### Installing

Mac:
```
# Install numpy
$ pip install numpy

# Install matplotlib
$ pip install matplotlib

# Install shapely
$ pip install shapely
```

Windows:
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
$ python amstelhaege.py
# or
$ python3 amstelhaege.py

# To stop the program, the user must type the following in the terminal on Windows:
$ Ctrl C

# To stop the program, the user must type the following in the terminal on Mac:
$ Command C
```

## The Program

### State-Space

On a grid of 156 by 176 gives 27.456 'blocks' can be placed somewhere. In reality, the plotting of houses is lower since this number applies to the smallest house. Next to that, no account is taken of water and of already placed houses. The State-space is as maximum 27.456 per house. 

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
