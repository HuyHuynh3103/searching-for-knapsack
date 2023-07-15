import os
import numpy as np
import time
import utils.read
import utils.write

def generateSelections(i, WList, selection, m, NList):
   if i == len(WList):
      num = sum(selection)
      if num >= int(m):
         # count numbers of class in NList
         tempNum = [NList[k] for k in range(len(selection)) if selection[k] == 1]
         # if enough class then save the selection
         if set(tempNum) == set(NList):
               yield selection
      return
   # mark the position
   for j in range(2):
      selection[i] = j
      yield from generateSelections(i+1, WList, selection, m, NList)

def bruteForce(w, m, WList, VList, NList):
   # Change string to float
   WList = np.array(WList, dtype=float)
   VList = np.array(VList, dtype=float)
   NList = np.array(NList, dtype=float)
   selection = np.zeros(len(WList), dtype=int)
   maxValue = 0
   bestSelection = None
   # Chose best solution in solutions
   solutions = generateSelections(0, WList, selection, m, NList)
   for sel in solutions:
      currentW = np.sum(sel * WList)
      # if the solution weight bigger than max weight(w) then skip this loop turn
      if currentW > w:
         continue 
      currentV = np.sum(sel * VList)
      # if the solution value bigger than max value then update the max value and copy the solution to the best selection
      if currentV > maxValue:
            maxValue = currentV
            bestSelection = sel.copy()

   if bestSelection is None:
      return (0, None)
   else:
      return (maxValue, bestSelection.tolist())


if __name__ == "__main__":
    print("==Brute Force Solution==")
    w, m, WList, VList, NList = utils.read.readDataset()
    start = time.time() 
    maxValue, listW = bruteForce(w, m, WList, VList, NList)
    utils.write.writeOutput(maxValue, listW)
    end = time.time()                                                                                                                                                              
    print("Time: ", end - start, '\n')