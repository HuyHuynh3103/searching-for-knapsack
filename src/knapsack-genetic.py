import random
import time
import utils.read
import utils.write

class Knapsack:
    maxWeight = 0
    classNum = 0

    def __init__(self, items):
        self.items = items
    
    def value(self):
        # calculate the total value of the items in the knapsack
        value = 0
        for item in self.items:
            value += item[0]
        return value
    
    def checkWeight(self):
        # check if the total weight of the items in the knapsack exceeds the maximum weight limit
        weight = 0
        for item in self.items:
            weight += item[1]
        return weight
    
    def checkClass(self):
        # check if the knapsack contains items from all classes
        foundClass = []
        for item in self.items:
            foundClass.append(item[2])
        foundClass = list(set(foundClass))
        return len(foundClass)

class Genetic:
    populationSize = 100
    itemList = []
    reproductionRate = 0.3
    crossoverRate = 0.8
    mutationRate = 0.4
    
    def genetic2SolutionConverter(geneticSequence):
        # convert a genetic sequence to a knapsack solution
        individual = []
        pos = []
        for i in range(len(geneticSequence)):
            if (geneticSequence[i] == 1):
                pos.append(i)
        for i in pos:
            individual.append(Genetic.itemList[i])
        return Knapsack(individual)
    
    def fitness(individual):
        # calculate the fitness score of a knapsack solution
        weight = individual.checkWeight()
        if (weight > Knapsack.maxWeight):
            return 0
        if (individual.checkClass() != Knapsack.classNum):
            return 0
        return individual.value()
    
    def initialPopulation():
        # create an initial population of random solutions
        population = []
        while (len(population) < Genetic.populationSize):
            geneticSequence = [random.randint(0, 1) for _ in range(len(Genetic.itemList))]
            solution = Genetic.genetic2SolutionConverter(geneticSequence)
            individual = (solution, geneticSequence, Genetic.fitness(solution))
            population.append(individual)
        return population
    
    def selection(population):
        # select two parents using tournament selection
        parent = []
        tournament_size = 4
        for i in range(2):
            # randomly select individuals from the population for the tournament
            tournament = random.sample(population, tournament_size)
            # select the fittest individual as a parent
            fittest_individual = max(tournament, key=lambda x: x[2])
            parent.append(fittest_individual)
        return parent

    def crossover(parent):
        # perform uniform crossover
        child1Gene = []
        child2Gene = []
        for i in range(len(parent[0][1])):
            if random.random() < 0.5:
                child1Gene.append(parent[0][1][i])
                child2Gene.append(parent[1][1][i])
            else:
                child1Gene.append(parent[1][1][i])
                child2Gene.append(parent[0][1][i])

        child1Solution = Genetic.genetic2SolutionConverter(child1Gene)
        child2Solution = Genetic.genetic2SolutionConverter(child2Gene)
        
        child1 = (child1Solution, child1Gene, Genetic.fitness(child1Solution))
        child2 = (child2Solution, child2Gene, Genetic.fitness(child2Solution))

        return child1, child2
    
    def mutation(children):
        mutantChildren = []
        if not children:
            return mutantChildren  # return empty list if children is empty
        
        mutation_probability = Genetic.mutationRate / len(children[0][1])
        
        for individual in children:
            mutatedGene = individual[1].copy()
            for i in range(len(mutatedGene)):
                if (random.random() < mutation_probability):
                    mutatedGene[i] = random.randint(0, 1)
            
            mutantChildSolution = Genetic.genetic2SolutionConverter(mutatedGene)
            mutantChildren.append((mutantChildSolution, mutatedGene, Genetic.fitness(mutantChildSolution)))

        return mutantChildren

    def nextGeneration(population):
        nextGen = []
        # create next generation if it good enough
        while len(nextGen) < len(population):
            children = []
            parents = Genetic.selection(population)
            if (random.random() < Genetic.reproductionRate):
                children = parents
            else:
                if (random.random() < Genetic.crossoverRate):
                    children = Genetic.crossover(parents)
                if (random.random() < Genetic.mutationRate):
                    children = Genetic.mutation(children)

            nextGen.extend(children)

        nextGen = sorted(nextGen, key=lambda x: x[2], reverse=True)
        return nextGen[:len(population)]

    # Solve the genetic problem
    def solveProblem():
        numGen = 1000
        population = Genetic.initialPopulation()
        bestIndividual = None
        for i in range(numGen):
            population = Genetic.nextGeneration(population)
            if bestIndividual is None or population[0][2] > bestIndividual[2]:
                bestIndividual = population[0]
        return bestIndividual


if __name__ == "__main__":
    print("==Genetic Solution==")
    w, m, WList, VList, NList = utils.read.readDataset()
    Knapsack.maxWeight = float(w)
    Knapsack.classNum = float(m)
    itemList = []
    for j in range(len(WList)):
        item = (float(VList[j]), float(WList[j]), int(NList[j]))
        itemList.append(item)
    Genetic.itemList = itemList
    start = time.time()
    solution = Genetic.solveProblem()
    end = time.time()    
    utils.write.writeOutput(solution[2], solution[1])
    print("Time: ", end - start, '\n')

