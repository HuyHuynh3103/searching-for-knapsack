import time
from queue import Queue
import utils.read
import utils.write
class Item:
    def __init__(self, weight, value, kind, position):
        self.weight = weight
        self.value = value
        self.kind = kind
        self.originalIndex = position
        self.sortedIndex = position
        self.priority = self.value / self.weight
    def __str__(self): 
        return "Item(weight:% s,value:% s,kind:% s,priority:% s)" % (self.weight, self.value, self.kind, self.priority) 
    def __repr__(self): 
        # return "Item(weight:% s,value:% s,kind:% s,priority:% s)" % (self.weight, self.value, self.kind, self.priority) 
        return "Item(original:% s,sorted:% s)" % (self.originalIndex, self.sortedIndex) 
class Node:
    def __init__(self, weight: float, value: int, kinds: list, items: list[Item]):
        self.totalWeight = weight
        self.totalValue = value
        self.kinds = kinds
        self.items = items
    def satisfiesClassSetCondition(self,numClasses) -> bool: 
        return len(set(self.kinds)) == numClasses
    def __str__(self): 
        return "Node(weight:% s,value:% s,kinds:% s,items:% s)" % (self.totalWeight, self.totalValue, self.kinds, self.items) 

def branchBound(knapsackWeight, numClasses, weights, values, classSet):
    items = [Item(weights[i], values[i], classSet[i], i) for i in range(len(weights))]
    items.sort(key=lambda x: x.priority, reverse=True)
    # Save the new index after sorting
    for i in range(len(items)):
        items[i].sortedIndex = i
    # Declare node with best value.
    nodeBestValue = Node(0, 0, [], [])
    
    queue = [Node(0, 0, [], [])]
    while queue:
        currentNode = queue.pop(0)
        i = len(currentNode.items)
        # update node best value if current node is a leaf, satisfies class condition and more optimze than node `best_value`.
        if i == len(items) and currentNode.satisfiesClassSetCondition(numClasses):
                nodeBestValue = bestNode(currentNode, nodeBestValue)
        else:
            item = items[i]
            newClasses = currentNode.kinds.copy()
            # A child node for not picking the i'th item
            notIncludedItem = Node(currentNode.totalWeight,
                                currentNode.totalValue,
                                newClasses,
                                currentNode.items + [0])
            if isPromissing(notIncludedItem, knapsackWeight, numClasses, nodeBestValue, items):
                queue.append(notIncludedItem)
            # A child node for picking the i'th item
            includedItem = Node(currentNode.totalWeight + item.weight,
                            currentNode.totalValue + item.value,
                            newClasses + [item.kind],
                            currentNode.items + [1])
            if isPromissing(includedItem, knapsackWeight, numClasses, nodeBestValue, items):
                queue.append(includedItem)
    items.sort(key=lambda x: x.originalIndex)
    solutionItems = []
    for i in range(len(items)):
        solutionItems.append(
            nodeBestValue.items[items[i].sortedIndex])
    return nodeBestValue.totalValue,solutionItems
def bestNode(nodeA: Node, nodeB: Node) -> Node: 
    return nodeA if nodeA.totalValue > nodeB.totalValue else nodeB
def isPromissing(node: Node, knapsackWeight: float, numClasses: int, nodeBest: Node, items: list[Item]) -> bool:
    return node.totalWeight <= knapsackWeight and getBound(node, knapsackWeight, items) > nodeBest.totalValue and verifyClass(node, knapsackWeight, numClasses, items)

def getBound(node: Node, knapsackWeight: float, items: list[Item]) -> float:
    remainingWeight = knapsackWeight - node.totalWeight
    bound = node.totalValue

    for i in range(len(node.items), len(items)):
        item = items[i]
        if remainingWeight >= item.weight:
            remainingWeight -= item.weight
            bound += item.value
        else:
            bound += item.priority * remainingWeight
            break
    return bound

def verifyClass(node: Node, knapsackWeight: float, numClasses: int, items: list[Item]):
    remainingWeight = knapsackWeight - node.totalWeight
    tempClass = node.kinds.copy()

    for i in range(len(node.items), len(items)):
        item = items[i]
        tempClass += [item.kind]
        if remainingWeight >= item.weight:
            remainingWeight -= item.weight
        else:
            break
    return (len(set(tempClass)) == numClasses)

if __name__ == '__main__':
    print("==Branch Bound Solution==")
    knapsackWeight, numberOfClasses, weights, values, classSet = utils.read.readDataset()
    start_time = time.time()
    totalValue, solutionItems = branchBound(knapsackWeight, numberOfClasses, weights, values, classSet)
    end_time = time.time()
    running_time = end_time - start_time
    print(f"Time (ms): {running_time*1000} ms")
    utils.write.writeOutput(totalValue, solutionItems)
