import time
import utils.read
import utils.write
class Item:
    def __init__(self, weight, value, _class, pre_pos):
        self.weight = weight
        self.value = value
        self._class = _class
        self.prePosition = pre_pos
        self.positionAfterSorting = pre_pos
        self.prio = self.value / self.weight


class Node:
    def __init__(self, weight: float, value: int, classes: list, items: list[Item]):
        self.totalWeight = weight
        self.totalValue = value
        self.totalClasses = classes
        self.totalItems = items

def branchBound(knapsackWeight, numClasses, weights, values, classLabels):
    """Calculating and return the result"""
    items = [Item(weights[i], values[i], classLabels[i], i) for i in range(len(weights))]
    # after having a list of items, we sort them by their "prio" value
    items.sort(key=lambda x: x.prio, reverse=True)
    # Save the new index after sorting
    for i in range(len(items)):
        items[i].positionAfterSorting = i
    # Initialize our result
    nodeResult = Node(0, 0, [], [])
    
    stack = [Node(0, 0, [], [])]
    while stack:
        currentNode = stack.pop(0)
        i = len(currentNode.totalItems)
        # check if the current node is a leaf
        if i == len(items):
            if len(set(currentNode.totalClasses)) == numClasses:
                if currentNode.totalValue > nodeResult.totalValue:
                    # Update out result
                    nodeResult = currentNode
        else:
            item = items[i]
            new_class = currentNode.totalClasses.copy()
            # A child node for not picking the i'th item
            NotAddItem = Node(currentNode.totalWeight,
                                currentNode.totalValue,
                                new_class,
                                currentNode.totalItems + [0])
            # A child node for picking the i'th item
            AddItem = Node(currentNode.totalWeight + item.weight,
                            currentNode.totalValue + item.value,
                            new_class + [item._class],
                            currentNode.totalItems + [1])
            if isPromissing(NotAddItem, knapsackWeight, numClasses, nodeResult, items):
                stack.insert(0, NotAddItem)
            if isPromissing(AddItem, knapsackWeight, numClasses, nodeResult, items):
                stack.insert(0, AddItem)
    items.sort(key=lambda x: x.prePosition)
    solutionItems = []
    for i in range(len(items)):
        solutionItems.append(
            nodeResult.totalItems[items[i].positionAfterSorting])
    return nodeResult.totalValue,solutionItems

def isPromissing(node: Node, knapsackWeight: float, numClasses: int, nodeResult: Node, items: list[Item]):
    return node.totalWeight <= knapsackWeight and getBound(node, knapsackWeight, items) > nodeResult.totalValue and verifyClass(node, knapsackWeight, numClasses, items)

def getBound(node: Node, knapsackWeight: float, items: list[Item]):
    remainingWeight = knapsackWeight - node.totalWeight
    bound = node.totalValue

    for i in range(len(node.totalItems), len(items)):
        item = items[i]
        if remainingWeight >= item.weight:
            remainingWeight -= item.weight
            bound += item.value
        else:
            bound += item.prio * remainingWeight
            break
    return bound

def verifyClass(node: Node, knapsackWeight: float, numClasses: int, items: list[Item]):
    remainingWeight = knapsackWeight - node.totalWeight
    tempClass = node.totalClasses.copy()

    for i in range(len(node.totalItems), len(items)):
        item = items[i]
        tempClass += [item._class]
        if remainingWeight >= item.weight:
            remainingWeight -= item.weight
        else:
            break
    return (len(set(tempClass)) == numClasses)

if __name__ == '__main__':
    print("==Branch Bound Solution==")
    knapsackWeight, numberOfClasses, weights, values, classLabels = utils.read.readDataset()
    start_time = time.time()
    totalValue, solutionItems = branchBound(knapsackWeight, numberOfClasses, weights, values, classLabels)
    end_time = time.time()
    running_time = end_time - start_time
    print(f"Time (ms): {running_time*1000} ms")
    utils.write.writeOutput(totalValue, solutionItems)
