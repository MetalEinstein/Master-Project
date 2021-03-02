import random, time, operator
from typing import *
from GA_Classes import *


def taskGenerator(taskList: List[object], taskNum: int, mapSize: int):
    # We create a set number of city's each of which is positioned randomly
    for i in range(0, taskNum):
        # Generate a random location for a city
        city_posx = int(random.random() * mapSize)
        city_posy = int(random.random() * mapSize)

        # Add the generated city to the city list and add it to the map
        taskList.append(City(x=city_posx, y=city_posy))  # Creating a list of objects/city's

    return taskList


def createRoute(taskList):
    temp_taskList = random.sample(taskList, len(taskList))
    genome = []

    while len(temp_taskList) > 1:
        # Select a random subset of tasks
        subset_range = int(random.random() * len(temp_taskList))
        while subset_range == 0:
            subset_range = int(random.random() * len(temp_taskList))

        # Remove the subset from the full task set and assign it to a genome/salesman
        gene = [temp_taskList.pop(random.randrange(len(temp_taskList))) for _ in range(subset_range)]
        genome.append(gene)

        # If a singe task is left insert it into a random genome in the salesman
        if len(temp_taskList) == 1:
            insert_rand_genome = int(random.random() * len(genome) - 1)
            insert_rand_index = int(random.random() * len(genome[insert_rand_genome]) - 1)

            genome[insert_rand_genome].insert(insert_rand_index, temp_taskList.pop())

    return genome


def initialPopulation(popSize, taskList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(taskList))

    return population


def rankRoutes(population, homeCity):
    fitnessResults = {}

    # Will fill a dictionary with key-value pairs
    # Key = Population index, value = corresponding fitness score
    fitness = Fitness(population, homeCity).routeFitness()
    for i in range(len(fitness)):
        fitnessResults[i] = fitness[i]

    # key = operator.itemgetter(1) -> Will create a sorted list according to the '1' element, 0 being the population index
    # and 1 being the fitness score. Thus we sort it from highest to lowest score
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)  # Returns sorted list


def evolvePopulation(population, popRanked, eliteSize, mutationRate):
    # newPopulation = Crossover(population, popRanked, eliteSize).evolve()
    # TODO make a mutation check here, so we don't initiate function unless we have to. Might give faster execution
    # TODO: input population should be the one coming from the crossover function
    newPopulation = Mutation(population, mutationRate).swap()

    return newPopulation
