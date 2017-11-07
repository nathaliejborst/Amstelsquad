class House:

    def __init__(self, length, width, freespace, value, valueUpdate):
        self.length = length
        self.width = width
        self.freespace = freespace
        self.value = value
        self.valueUpdate = valueUpdate

    def area(self):
        return self.length * self.width

    def addFreespace(self, meter):
        self.meter = meter
        self.freespace += meter
        self.value = round(self.value * self.valueUpdate ** int(meter), 2)


maison = House(length=11, width=10.5, freespace=6, value=610000,
               valueUpdate=1.06)

bungalow = House(length=10, width=7.5, freespace=3, value=399000,
                 valueUpdate=1.04)

familyHouse = House(length=8, width=8, freespace=2, value=285000,
                    valueUpdate=1.03)

print(maison.freespace)
print(maison.value)
maison.addFreespace(meter=2)
print(maison.freespace)
print(maison.value)
