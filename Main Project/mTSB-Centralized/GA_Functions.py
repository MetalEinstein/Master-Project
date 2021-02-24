import random, time
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
            insert_rand_genome = int(random.random() * len(genome)-1)
            insert_rand_index = int(random.random() * len(genome[insert_rand_genome])-1)

            genome[insert_rand_genome].insert(insert_rand_index, temp_taskList.pop())

    return genome


def initialPopulation(popSize, taskList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(taskList))

    return population


def routeDistance(population, homeCity):
    pathDistance = []
    for i in range(len(population)):
        geneDistance = 0
        individual = population[i]
        for j in range(len(individual)):
            gene = individual[j]
            # Add home town to start and end of specific agent route
            print("old", gene)
            gene.insert(0, homeCity)
            gene.append(homeCity)
            print(gene)
            for k in range(len(gene)):
                fromCity = gene[k]
                toCity = None
                if k + 1 < len(gene):
                    toCity = gene[k + 1]
                else:
                    # When we get to the last city in the list we add the distance from it back to the initial city
                    toCity = gene[0]
                geneDistance += fromCity.distance(toCity)
        pathDistance.append(geneDistance)
    return pathDistance
