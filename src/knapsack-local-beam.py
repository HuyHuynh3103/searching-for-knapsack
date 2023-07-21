import time
import utils.read
import utils.write

def generateInitialStates(numItems, knapsackWeight, weights, values):
    # Generate initial states with an empty set of items
    initialStates = [(tuple(), 0, 0)]
    for i in range(numItems):
        state, val, weight = initialStates[0]
        if weight + weights[i] <= knapsackWeight:
            # Add a new item to the state if the weight constraint is not violated
            newState = set(state).copy()
            newState.add(i)
            newState = tuple(newState)  # Convert set to tuple
            newStateInfo = (newState, val + values[i], weight + weights[i])
            initialStates.append(newStateInfo)
    return initialStates

def beamSearchAtEachStep(states, knapsackWeight, weights, values):
    # Explore possible next states by adding a new item to each current state
    newStates = []
    for state, val, weight in states:
        for i in range(len(weights)):
            if i not in state and weight + weights[i] <= knapsackWeight:
                # Add a new item to the state if the weight constraint is not violated
                newState = set(state).copy()
                newState.add(i)
                newState = tuple(newState)  # Convert set to tuple
                newStateInfo = (newState, val + values[i], weight + weights[i])
            else:
                newStateInfo = (state, val, weight)
            newStates.append(newStateInfo)
    return newStates

def selectBestStates(states, beamWidth):
    # Select the best states with the highest value and lowest weight
    sortedStates = sorted(states, key=lambda x: (x[1], knapsackWeight - x[2]), reverse=True)
    uniqueStates = list(sorted(set(sortedStates), key=sortedStates.index))
    return uniqueStates[:beamWidth]

def selectItemsForClasses(bestState, classSet):
    # Select the items and classes covered by the best state
    bestItems = bestState[0]
    selectedClasses = set()
    selectedItems = [0] * len(values)

    for item in bestItems:
        selectedItems[item] = 1
        selectedClasses.add(classSet[item])

    return selectedItems, selectedClasses

def localBeamSearch(knapsackWeight, numClasses, weights, values, classSet, beamWidth):
    # Initialize the states and perform beam search
    states = generateInitialStates(len(values), knapsackWeight, weights, values)
    
    for _ in range(len(values)):
        newStates = beamSearchAtEachStep(states, knapsackWeight, weights, values)
        states = selectBestStates(newStates, beamWidth)

    bestState = states[0]
    selectedItems, selectedClasses = selectItemsForClasses(bestState, classSet)

    for classLabel in range(1, numClasses):
        if sorted(selectedClasses).count(classLabel) == 0:
            return 0, [0] * len(values)

    return bestState[1], selectedItems

if __name__ == '__main__':
    print("==Local Beam Solution==")
    knapsackWeight, numClasses, weights, values, classLabels = utils.read.readDataset()
    start = time.time()
    bestVal = (0, [0] * len(values))
    for beamWidth in range(1, 9):
        val, items = localBeamSearch(knapsackWeight, numClasses, weights, values, classLabels, beamWidth)
        if val > bestVal[0]:
            bestVal = (val, items)
    end = time.time()
    utils.write.writeOutput(bestVal[0], bestVal[1])
    print("Time (ms): ", end - start, '\n')
