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
    def __init__(self, weight: float, value: int, classes: list, items: list[int]):
        self.totalWeight = weight
        self.totalValue = value
        self.totalClasses = classes
        self.totalItems = items
class BranchBound:
    def __init__(self, knapsackWeight, numClasses, weights, values, classLabels ):
        self.knapsackWeight = knapsackWeight
        self.numClasses = numClasses
        self.items = [Item(weights[i], values[i], classLabels[i], i) for i in range(len(weights))]
        # after having a list of items, we sort them by their "prio" value
        self.items.sort(key=lambda x: x.prio, reverse=True)
        # Save the new index after sorting
        for i in range(len(self.items)):
            self.items[i].positionAfterSorting = i
        # Initialize our result
        self.nodeResult = Node(0, 0, [], [])
        
    def solve(self):
        """Calculating and return the result"""
        stack = [Node(0, 0, [], [])]
        while stack:
            currentNode = stack.pop(0)
            i = len(currentNode.totalItems)
            # check if the current node is a leaf
            if i == len(self.items):
                if len(set(currentNode.totalClasses)) == self.numClasses:
                    if currentNode.totalValue > self.nodeResult.totalValue:
                        # Update out result
                        self.nodeResult = currentNode
            else:
                item = self.items[i]
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
                if self.isPromissing(NotAddItem):
                    stack.insert(0, NotAddItem)
                if self.isPromissing(AddItem):
                    stack.insert(0, AddItem)

        return self.nodeResult

    def isPromissing(self, node: Node):
        """Check if we prunch or not prunch a node"""
        return node.totalWeight <= self.knapsackWeight and self.getBound(node) > self.nodeResult.totalValue and self.verifyClass(node)

    def getBound(self, node: Node):
        """Calculate the "possible value" we can get if travel this branch"""
        remainingWeight = self.knapsackWeight - node.totalWeight
        bound = node.totalValue

        for i in range(len(node.totalItems), len(self.items)):
            item = self.items[i]
            if remainingWeight >= item.weight:
                remainingWeight -= item.weight
                bound += item.value
            else:
                bound += item.prio * remainingWeight
                break
        return bound

    def verifyClass(self, node: Node):
        """Check if we can have full of classes if we travel this branch
        Return True if we can, else return False"""
        remainingWeight = self.knapsackWeight - node.totalWeight
        tempClass = node.totalClasses.copy()

        for i in range(len(node.totalItems), len(self.items)):
            item = self.items[i]
            tempClass += [item._class]
            if remainingWeight >= item.weight:
                remainingWeight -= item.weight
            else:
                break
        return (len(set(tempClass)) == self.numClasses)

    def getResult(self):
        self.items.sort(key=lambda x: x.prePosition)
        answerItems = []
        # traceback our item, because after sorting, our items are messed up
        # So we need to get them to their previous positions
        for i in range(len(self.items)):
            answerItems.append(
                self.nodeResult.totalItems[self.items[i].positionAfterSorting])
        return self.nodeResult.totalValue,answerItems


if __name__ == '__main__':
    print("==Branch Bound Solution==")
    knapsackWeight, numberOfClasses, weights, values, classLabels = utils.read.readDataset()
    algo = BranchBound(knapsackWeight, numberOfClasses, weights, values, classLabels)
    start_time = time.time()
    result = algo.solve()
    end_time = time.time()
    print(result.totalValue)
    running_time = end_time - start_time
    print(f"Running time (ms): {running_time*1000} ms")
    totalValue, answerItems = algo.getResult()
    utils.write.writeOutput(totalValue, answerItems)
