import numpy as np, random, operator, pandas as pd
from my_classes import Fitness
from typing import *


# Draws a random sample from our city_list
# route = a list of city objects the order of which is randomized
def createRoute(cityList: List[object]) -> List[object]:
    route = random.sample(cityList, len(cityList))
    return route


# Creates a nested list where the inner lists each contain a random sequence of city objects
def initialPopulation(popSize: int, cityList: List[object]) -> List[List[object]]:
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population


# Goes through each route in our population and ranks them according to distance
# Highest scored route = lowest overall distance
# TODO I'm not sure about the return, i keep getting a complaint
def rankRoutes(population: List[List[object]]) -> List[Tuple[int, float]]:
    fitnessResults = {}

    # Will fill a dictionary with key-value pairs
    # Key = Population index, value = corresponding fitness score
    for i in range(0, len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()

    # key = operator.itemgetter(1) -> Will create a sorted list according to the '1' element, 0 being the population index
    # and 1 being the fitness score. Thus we sort it from highest to lowest score
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)  # Returns sorted list


# Creates a mating pool by assigning probabilities according to the individual fitness scores
# Better fitness score = Higher probability of being picked
# Also insures that the best individuals in the population carries on to the next
def selection(popRanked: List[Tuple[int, float]], eliteSize: int) -> List[int]:
    selectionResults = []

    # Assign probabilities to each individual in the population
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    # Picks out the top individuals in the population for the mating-pool. Not chosen by probability
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])  # Appends list with the index of the best individuals

    # Fills out the remaining mating pool according to the probabilities assigned to each individual
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100 * random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


# Creates a list of the best suited routes
def matingPool(population: List[List[object]], selectionResults: List[int]) -> List[List[object]]:
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


# Takes in two individuals and mates them using ordered crossover resulting in a new route
def breed(parent1: List[object], parent2: List[object]) -> List[object]:
    child = []
    childP1 = []
    childP2 = []

    # Select a random subset from parent 1. Subset = a set of city's found in that particular route
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    # Insure that parts of the randomly created subset does not exist in parent 2
    childP2 = [item for item in parent2 if item not in childP1]
    child = childP2

    # We combine parent 1 & 2 by inserting the gene subset from the first parent into the second at the appropriate position
    child[startGene:startGene] = childP1
    return child


# Breeds the individuals in our mating pool
def breedPopulation(matingpool: List[List[object]], eliteSize: int) -> List[List[object]]:
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    # Will carry the best individuals in our mating pool over to the next generation unchanged
    for i in range(0, eliteSize):
        children.append(matingpool[i])

    # Will mate the individuals in the remaining mating pool and add the child to the next generation
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children


# Mutates an individual by swapping out two city's in the route
def mutate(individual: List[object], mutationRate: float) -> List[object]:
    for swapped in range(len(individual)):
        if (random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


# Mutates the new generations
def mutatePopulation(population: List[List[object]], mutationRate: float) -> List[List[object]]:
    mutatedPop = []

    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)

    return mutatedPop


# Takes in the current generation and returns the next
def nextGeneration(currentGen: List[List[object]], eliteSize: int, mutationRate: float) -> List[List[object]]:
    popRanked = rankRoutes(currentGen)  # Ranks the routes in the current generation
    selectionResults = selection(popRanked, eliteSize)  # Determines potential parents
    matingpool = matingPool(currentGen, selectionResults)  # Creates mating pool
    children = breedPopulation(matingpool, eliteSize)  # Creates new generation
    nextGeneration = mutatePopulation(children, mutationRate)  # Apply mutation to new generation
    return nextGeneration
