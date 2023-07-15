import os
def readDataset(fileName = "../../INPUT_10.txt"):
   path = os.path.dirname(__file__)
   pathFileName = (path + "/" + fileName)
   with open(pathFileName, "r") as fin:
      w = float(fin.readline())
      m = int(fin.readline())
      WList = list(map(float, fin.readline().rstrip("\n").split(", ")))
      VList = list(map(float, fin.readline().rstrip("\n").split(", ")))
      NList = list(map(float, fin.readline().rstrip("\n").split(", ")))
   return w, m, WList, VList, NList
