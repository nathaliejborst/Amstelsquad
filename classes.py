class Grid:
    def __init__(self, housesList = [], teslist = [], x=0):
        self.housesList = housesList

    def totalValue(self, housesList):
        value = 0
        for house in housesList:
            value += house.value
            value += (house.extraFreespace - house.freespace) * house.valueUpdate * house.value
            return value

# Declare elements of house in class.
class House:
    def __init__(self, width, height, freespace, value, valueUpdate, x=0, y=0, color=None, distanceToOthers = [], extraFreespace=0):
        self.width = width
        self.height = height
        self.freespace = freespace
        self.value = value
        self.valueUpdate = valueUpdate
        self.x = x
        self.y = y
        self.color = color
        self.distanceToOthers = distanceToOthers
        self.extraFreespace = extraFreespace

    def area(self):
        return self.width * self.height

    def Xmin(self, x):
        return x
    def Xmax(self, x):
        return (x + self.width)
    def Ymin(self, y):
        return y
    def Ymax(self, y):
        return (y + self.height)

    def corners(self, x, y):
        bottomLeft = [x, y]
        upperLeft = [x, (y + self.height)]
        upperRight = [(x + self.width), (y + self.height)]
        bottomRight = [(x + self.width), y]
        return [bottomLeft, upperLeft, upperRight, bottomRight]

    def spacecorners(self, x, y):
        bottomLeft = [x - self.freespace, y - self.freespace]
        upperLeft = [x - self.freespace, (y + self.height + self.freespace)]
        upperRight = [(x + self.width + self.freespace), (y + self.height + self.freespace)]
        bottomRight = [(x + self.width + self.freespace), y - self.freespace]
        return [bottomLeft, upperLeft, upperRight, bottomRight]

    def extraFreeSpaceCorners(self, x, y):
        bottomLeft = [x - self.extraFreespace, y - self.extraFreespace]
        upperLeft = [x - self.extraFreespace, (y + self.height + self.extraFreespace)]
        upperRight = [(x + self.width + self.extraFreespace), (y + self.height + self.extraFreespace)]
        bottomRight = [(x + self.width +  self.extraFreespace), y - self.extraFreespace]
        return [bottomLeft, upperLeft, upperRight, bottomRight]

    def addFreespace(self, meter):
        self.meter = meter
        self.freespace += meter
        self.value = round(self.value * self.valueUpdate ** int(meter), 2)
        return self.freespace, self.value

    def totalWidth(self):
        return self.width + self.freespace * 2

    def totalHeight(self):
        return self.height + self.freespace * 2
