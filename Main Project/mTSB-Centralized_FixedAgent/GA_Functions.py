# import operator
# import numpy as np
import cv2
# from typing import *
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
    #list = [(67,423), (381,127), (247,224), (325,394), (46,14), (417,216), (381,1), (222,360), (114,472), (450,15), (12,270), (469,190), (108,211), (14,110), (218,247), (116,115), (109,229), (144,10), (418,278), (321,92), (496,429), (60,166), (360,355), (468,211), (415,335)]
    cityx = [67, 381, 247, 325, 46, 417, 381, 222, 114, 450, 12, 469, 108, 14, 218, 116, 109, 144, 418, 321, 496, 60, 360, 468, 415]
    cityy = [423, 127, 224, 394, 14, 216, 1, 360, 472, 15, 270, 190, 211, 110, 247, 115, 229, 10, 278, 92, 429, 166, 355, 211, 335]
    # cityx = [43, 25, 106, 25, 119, 119, 86, 86, 5, 56, 106, 100, 76, 149, 76, 124, 76, 122, 76, 148, 76]
    # cityy = [2, 22, 14, 22, 26, 16, 17, 17, 48, 53, 20, 55, 5, 57, 5, 29, 5, 11, 5, 3, 5]
    #city_posx = [43, 25, 106, 119, 119, 86,  5, 56, 106, 100, 76, 149, 124, 122, 148, 43, 80, 80, 51, 25,  5, 51, 56, 110, 106, 86, 75, 110, 118, 132, 110, 121, 121, 121, 100]
    #city_posy = [ 2, 22,  14,  26,  16, 17, 48, 53,  20,  55,  5,  57,  29,  11,   3, 11, 11, 26, 26, 26, 26, 45, 45,  11,  11, 11, 11,  21,  11,   3,  30,  30,  26,  57,  57]

    for i in range(len(cityx)):
        taskList.append(City(x=cityx[i], y=cityy[i]))

    return taskList


def createRoute(taskList, num_agents):
    temp_taskList = random.sample(taskList, len(taskList))
    individual = []
    tasks_each = int(len(temp_taskList)/num_agents)

    # Distribute the tasks among the agents
    genome = []
    for a in range(num_agents-1):
        for i in range(tasks_each):
            selected_task = random.randint(0, len(temp_taskList)-1)
            genome.append(temp_taskList.pop(selected_task))
        individual.append(genome)
        genome = []

    # Add the remaining tasks in the tasklist to the last agent
    individual.append(temp_taskList)

    return individual


def initialPopulation(popSize, taskList, num_agents):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(taskList, num_agents))

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


def evolvePopulation(population, popRanked, eliteSize, mutationRate, sel_size, generation):
        matingPool = Selection(population, popRanked, eliteSize, sel_size, generation).matingPool()
        newCrossoverPopulation = Crossover(matingPool, eliteSize).evolve()
        newPopulation = Mutation(newCrossoverPopulation, mutationRate).mutate()

        return newPopulation


def city_connect(final_population, size, best_index, home_city, best_dist):
    map_city = np.ones((size, size, 3), np.uint8)
    map_city.fill(255)
    color_dic = {}

    txt = 'Distance = %2.f' % (1/best_dist)
    y = 100+50

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
    cv2.putText(map_city, txt, org=(0, y), fontFace=cv2.FONT_ITALIC, fontScale=0.4, color=(0, 0, 0), thickness=1, lineType=8)
    return map_city
