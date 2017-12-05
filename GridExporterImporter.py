import csv


def writeToFile(totalvalue):
    with open("values.csv", "a") as filewriter:
        fieldnames = ["value"]
        writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
        writer.writerow({"value": totalvalue})
