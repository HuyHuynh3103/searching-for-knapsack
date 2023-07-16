import numpy as np
import time
import utils.read
import utils.write

def generateSelections(index, weights, selection, numClasses, classes):
   if index == len(weights):
      num = sum(selection)
      if num >= int(numClasses):
         # count numbers of class in NList
         tempNum = [classes[k] for k in range(len(selection)) if selection[k] == 1]
         # if enough class then save the selection
         if set(tempNum) == set(classes):
               yield selection
      return
   # mark the position
   for j in range(2):
      selection[index] = j
      yield from generateSelections(index+1, weights, selection, numClasses, classes)

def bruteForce(knapsackWeight, numClasses, weights, values, classes):
   # Change string to float
   weights = np.array(weights, dtype=float)
   values = np.array(values, dtype=float)
   classes = np.array(classes, dtype=float)
   selection = np.zeros(len(weights), dtype=int)
   maxValue = 0
   bestSelection = None
   # Chose best solution in solutions
   solutions = generateSelections(0, weights, selection, numClasses, classes)
   for sel in solutions:
      currentW = np.sum(sel * weights)
      # if the solution weight bigger than max weight(w) then skip this loop turn
      if currentW > knapsackWeight:
         continue 
      currentV = np.sum(sel * values)
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
    knapsackWeight, numClasses, weights, values, classLabels = utils.read.readDataset()
    start = time.time() 
    maxValue, listW = bruteForce(knapsackWeight, numClasses, weights, values, classLabels)
    utils.write.writeOutput(maxValue, listW)
    end = time.time()                                                                                                                                                              
    print("Time: ", end - start, '\n')