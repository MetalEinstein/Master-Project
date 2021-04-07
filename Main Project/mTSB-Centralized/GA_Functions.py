import random, time, operator
import numpy as np
import cv2
from typing import *
from GA_Classes import *
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import kneed
import copy
from mutations import *

def taskGenerator(taskList: List[object], taskNum: int, mapSize: int):
    # We create a set number of city's each of which is positioned randomly
    temp = []
    temp2 = []
    NUM_SALESMEN = 5
    for i in range(0, taskNum):
        # Generate a random location for a city
        city_posx = int(random.random() * mapSize)
        city_posy = int(random.random() * mapSize)
        #
        # Add the generated city to the city list and add it to the map
        # taskList.append(City(x=city_posx, y=city_posy))
        temp.append((city_posx, city_posy))  # Creating a list of objects/city's
    homeCity = temp.pop(0)
    homeCity = City(x=homeCity[0], y=homeCity[1])
    print("home city: ", homeCity)

    label = perform_k_means(temp, NUM_SALESMEN)
    map, start_individual = get_groups(temp, label, mapSize)
    print("start individual: ", start_individual)

    for agents in start_individual:
        for genes in agents:

            temp2.append(City(x=genes[0], y=genes[1]))
        taskList.append(temp2)
        temp2 = []
    print("tasklist: ", taskList)
    return taskList, homeCity


# def taskGenerator(taskList: List[object], taskNum: int, mapSize: int):
#     # We create a set number of city's each of which is positioned randomly
#     for i in range(0, taskNum):
#         # Generate a random location for a city
#         city_posx = int(random.random() * mapSize)
#         city_posy = int(random.random() * mapSize)
#
#         # Add the generated city to the city list and add it to the map
#         taskList.append(City(x=city_posx, y=city_posy))  # Creating a list of objects/city's
#
#     return taskList


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


# def initialPopulation(popSize, taskList):
#     population = []
#
#     for i in range(0, popSize):
#         population.append(createRoute(taskList))
#
#     return population

def initialPopulation(popSize, taskList):
    population = []
    #taskList2 = taskList.copy()
    #taskList2 = [[(313,51), (340,161), (203,0), (60,108)], [(27,432), (76,472), (117,289), (71,223)], [(458,403)]]
    #temp = []
    mutation_types = {0: lambda x: sequence_inversion(x),
                      1: lambda x: transposition(x),
                      2: lambda x: insertion(x),
                      3: lambda x: chromosome_contraction(x),
                      4: lambda x: chromosome_partition(x),
                      }

    # for i in range(0, popSize):
    #     selected_mutation = random.choice(list(mutation_types.values()))
    #     # selected_mutation = random.choice(mutation_types)
    #     population.append(selected_mutation(taskList))


    for i in range(popSize):
        print("\n")
        taskList2 = copy.deepcopy(taskList)
        selected_mutation = np.random.choice(list(mutation_types.values()),p=[0.6,0.2,0.1,0.05,0.05])
        print("Tasklist: ", taskList2)
        temp = selected_mutation(taskList2)
        population.append(copy.deepcopy(temp))
        print("Population: ", population[i])
    print("Population: ", population)


    return population

# def sequence_inversion(individual):
#     print("inversion")
#     # print("\nPrevious Individual: ", individual)
#
#     # Select a genome from the individual at random
#     k = random.randint(0, len(individual) - 1)
#     genome = individual[k]
#     # print("Selected Genome: ", individual[k])
#
#     if len(genome) > 1:
#         # Randomly choose a start and end index to specify the gene sequence to be inverted
#         start_index = random.randint(0, len(genome) - 2)
#         end_index = random.randint(start_index, len(genome) - 1)
#         # print(f"Selected Sequence: {start_index} -> {end_index + 1}")
#
#         # Insure that at least two genes are always being inverted
#         if start_index == end_index:
#             end_index += 1
#
#         # Take out the selected sequence and invert it
#         subset = genome[start_index:end_index + 1]
#         # print("\nGene subset: ", subset)
#         subset.reverse()
#         # print("Reversed Gene subset: ", subset)
#
#         # Reinsert the inverted gene sequence into the original genome and insert into the individual
#         genome[start_index:end_index + 1] = subset
#         individual[k] = genome
#         # print("New Individual: ", individual)
#
#     return individual


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


def perform_k_means(data, num_salesmen):
    sse = []
    k_rng = range(1, num_salesmen+1)

    for k in k_rng:
        km = KMeans(n_clusters=k)
        km.fit(data)
        sse.append(km.inertia_)

    # TODO improve the estimation of the best number of K. Maybe through tracking the slope of the curve
    """
    for i in range(0, len(sse)-1):
        m = 1-((sse[i+1]/sse[i])/1)
        print(m)
    """

    kn = kneed.KneeLocator(k_rng, sse, curve='convex', direction='decreasing', interp_method='interp1d')
    print("Best Estimated K: ", kn.elbow)
    km = KMeans(n_clusters=kn.elbow)
    y_predicted = km.fit_predict(data)

    plt.xlabel('K')
    plt.ylabel('Sum of squared error')
    plt.plot(k_rng, sse, 'bx-')

    return y_predicted


def get_groups(data, grouping, map_size):
    map_city = np.ones((map_size, map_size, 3), np.uint8)
    map_city.fill(255)
    num_groups = len(set(grouping))
    color_dic = {}
    initial_salesman = [[] for _ in range(0, num_groups)]

    # Generate unique colors for each salesman
    for i in range(0, num_groups):
        b_val = int(random.random() * 255)
        g_val = int(random.random() * 255)
        r_val = int(random.random() * 255)
        color_dic[i] = (b_val, g_val, r_val)

    # Visualize groups on a map and distribute the groups between salesmen
    for i in range(0, len(data)):
        x = data[i][0]
        y = data[i][1]
        cv2.circle(map_city, (x, y), 3, color_dic[grouping[i]], -1)
        initial_salesman[grouping[i]].append([x, y])

    return map_city, initial_salesman
