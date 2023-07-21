import time
import utils.read
import utils.write

def generateInitialPaths(num_items, knapsackWeight, weights, values):
    initial_path = [(tuple(), 0, 0)]
    for i in range(num_items):
        item, val, weight = initial_path[0]
        if weight + weights[i] <= knapsackWeight:
            newItem = set(item).copy()
            newItem.add(i)
            newItem = tuple(newItem)  # Convert set to tuple
            new_path = (newItem, val + values[i], weight + weights[i])
            initial_path.append(new_path)
    return initial_path

def beamSearchAtEachStep(path, knapsackWeight, weights, values):
    newPaths = []
    for item, val, weight in path:
        for i in range(len(weights)):
            if i not in item and weight + weights[i] <= knapsackWeight:
                newItem = set(item).copy()
                newItem.add(i)
                newItem = tuple(newItem)  # Convert set to tuple
                new_path = (newItem, val + values[i], weight + weights[i])
            else:
                new_path = (item, val, weight)
            newPaths.append(new_path)
    return newPaths

def selectBestPaths(paths, beam_width):
    sorted_paths = sorted(paths, key=lambda x: (x[1], knapsackWeight - x[2]), reverse=True)
    unique_paths = list(sorted(set(sorted_paths), key=sorted_paths.index))
    return unique_paths[:beam_width]

def selectItemsForClasses(bestPath, class_set):
    best_items = bestPath[0]
    selectedClasses = set()
    selectedItems = [0] * len(values)

    for item in best_items:
        selectedItems[item] = 1
        selectedClasses.add(class_set[item])

    return selectedItems, selectedClasses

def localBeamSearch(knapsackWeight, numClasses, weights, values, class_set, beam_width):
    paths = generateInitialPaths(len(values), knapsackWeight, weights, values)
    
    for _ in range(len(values)):
        newPaths = beamSearchAtEachStep(paths, knapsackWeight, weights, values)
        paths = selectBestPaths(newPaths, beam_width)

    bestPath = paths[0]
    selectedItems, selectedClasses = selectItemsForClasses(bestPath, class_set)

    for classLabel in range(1, numClasses):
        if sorted(selectedClasses).count(classLabel) == 0:
            return 0, [0] * len(values)

    return bestPath[1], selectedItems

if __name__ == '__main__':
    print("==Local Beam Solution==")
    knapsackWeight, numClasses, weights, values, classLabels = utils.read.readDataset()
    start = time.time()
    best_val = (0, [0] * len(values))
    for beam_width in range(1, 9):
        val, items = localBeamSearch(knapsackWeight, numClasses, weights, values, classLabels, beam_width)
        if val > best_val[0]:
            best_val = (val, items)
    end = time.time()
    utils.write.writeOutput(best_val[0], best_val[1])
    print("Time (ms): ", end - start, '\n')
