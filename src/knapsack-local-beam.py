import time
import utils.read
import utils.write

def localBeam(knapsackWeight, numClasses, weights, values, classSet, bWidth):
    highest_val = float
    path = [(tuple(), 0, 0, tuple())]

    for i in range(len(values)):
        paths = []

        for j in range(len(path)):
            item, val, weight, classes = path[j]
            # Filter out paths that violate the weight constraint during path generation
            for k in range(len(values)):
                if(k not in item and weight + weights[k] <= knapsackWeight):
                    newItem = set(item).copy()
                    newItem.add(k)
                    newItem = tuple(newItem)
                    updateClass = set(classes).copy()
                    updateClass.add(classSet[k])
                    updateClass = tuple(updateClass)
                    nextPath = (newItem,val+values[k], weight+weights[k],updateClass)

                else:
                    nextPath = (item,val,weight,classes)
                paths.append(nextPath)
        # Add randomness to path selection for diversity
        pathOrder = sorted(paths,key = lambda element:(len(element[3]), element[1],knapsackWeight-element[2]), reverse = True)
        pathOrder = list(sorted(set(pathOrder), key = pathOrder.index))
        path = pathOrder[:bWidth]

    best_track = [0]*len(values)
    best_path = path[0]

    temp = []
    for x in best_path[0]:
        best_track[x] = 1
        if(best_track[x] == 1):
            temp.append(classSet[x]) 
            
    # Ensure that the selected items cover all classes
    for y in range(1,numClasses):
        if (sorted(temp)).count(y) == 0:
            return 0,0


    highest_val = best_path[1]
    return  highest_val,best_track

if __name__ == '__main__':
    print("==Local Beam Solution==")
    knapsackWeight, numClasses, weights, values, classLabels = utils.read.readDataset()
    start = time.time()
    for x in range(1,9):
        lb = localBeam(knapsackWeight,numClasses,weights,values,classLabels,x)
        for y in range(2,len(weights)):
            best_val = localBeam(knapsackWeight,numClasses,weights,values,classLabels,x)
    end = time.time()
    utils.write.writeOutput(best_val[0], best_val[1])
    print("Time (ms): ", end - start, '\n')
    
