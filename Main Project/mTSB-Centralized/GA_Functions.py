import random, time, operator
import numpy as np
import cv2
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


def taskGeneratortesting(taskList: List[object]):
    # We create a set number of city's each of which is positioned randomly
    #list = [(67,423), (381,127), (247,224), (325,394), (46,14), (417,216), (381,1), (222,360), (114,472), (450,15), (12,270), (469,190), (108,211), (14,110), (218,247), (116,115), (109,229), (144,10), (418,278), (321,92), (496,429), (60,166), (360,355), (468,211), (415,335)]
    cityx = [67, 381, 247, 325, 46, 417, 381, 222, 114, 450, 12, 469, 108, 14, 218, 116, 109, 144, 418, 321, 496, 60, 360, 468, 415]
    cityy = [423, 127, 224, 394, 14, 216, 1, 360, 472, 15, 270, 190, 211, 110, 247, 115, 229, 10, 278, 92, 429, 166, 355, 211, 335]
    for i in range(len(cityx)):
        city_posx = cityx[i]
        city_posy = cityy[i]
        taskList.append(City(x=city_posx, y=city_posy))

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
    newCrossoverPopulation = Crossover(population, popRanked, eliteSize).evolve()
    # TODO make a mutation check here, so we don't initiate function unless we have to. Might give faster execution
    # TODO: input population should be the one coming from the crossover function
    newPopulation = Mutation(newCrossoverPopulation, mutationRate).mutate()

    return newPopulation


def city_connect(final_population, size, best_index, home_city):
    map_city = np.ones((size, size, 3), np.uint8)
    map_city.fill(255)
    color_dic = {}

    # Add the home city to the task list of each salesmen
    best_individual = final_population[best_index]
    for genome_index in range(len(best_individual)):
        best_individual[genome_index].insert(0, home_city)

    # Generate unique colors for each salesman
    for i in range(0, len(best_individual)):
        b_val = int(random.random() * 255)
        g_val = int(random.random() * 255)
        r_val = int(random.random() * 255)
        color_dic[i] = (b_val, g_val, r_val)

    # Draw the tasks and their connections on a map
    for genomes in best_individual:
        # We plot the city's on the map and draw the most optimized route between them
        for i in range(0, len(genomes)):
            if i == len(genomes) - 1:
                city1_posx, city1_posy = genomes[i].x, genomes[i].y
                city2_posx, city2_posy = genomes[0].x, genomes[0].y

            else:
                city1_posx, city1_posy = genomes[i].x, genomes[i].y
                city2_posx, city2_posy = genomes[i + 1].x, genomes[i + 1].y

            if i == 0:
                cv2.circle(map_city, (city1_posx, city1_posy), 3, 0, -1)  # Visualizing the position of city's on map
                cv2.line(map_city, (city1_posx, city1_posy), (city2_posx, city2_posy), color_dic[best_individual.index(genomes)], thickness=1, lineType=8)
            else:
                cv2.circle(map_city, (city1_posx, city1_posy), 3, (0, 0, 255),
                           -1)  # Visualizing the position of city's on map
                cv2.line(map_city, (city1_posx, city1_posy), (city2_posx, city2_posy), color_dic[best_individual.index(genomes)], thickness=1, lineType=8)

    return map_city
