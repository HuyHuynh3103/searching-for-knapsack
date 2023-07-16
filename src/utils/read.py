import os
def readDataset(fileName = "../../INPUT_10.txt"):
   path = os.path.dirname(__file__)
   pathFileName = (path + "/" + fileName)
   with open(pathFileName, "r") as fin:
      knapsackWeight = float(fin.readline())
      numberOfClasses = int(fin.readline())
      weights = list(map(float, fin.readline().rstrip("\n").split(", ")))
      values = list(map(float, fin.readline().rstrip("\n").split(", ")))
      classes = list(map(float, fin.readline().rstrip("\n").split(", ")))
   return knapsackWeight, numberOfClasses, weights, values, classes
