import random
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import math
from itertools import permutations
import time


def similarity(population, pairs_to_compare, current_index):
    similarity_score = 0
    match_list = []

    # Pick out the two individuals to be compared from the population
    individual_one = population[pairs_to_compare[current_index][0]]
    individual_two = population[pairs_to_compare[current_index][1]]

    for genome1 in individual_one:
        for genome2 in individual_two:
            # Compare element i in genome 1 with all elements in genome 2
            # If element i in genome 1 is found in genome 2 return the index at which the match occurred
            for i in range(len(genome1)):
                for k in range(len(genome2)):
                    if genome1[i] == genome2[k]:
                        match_list.append(k)
                        break

            # We order the list in ascending order.
            match_list = sorted(match_list)

            # We check for matching task order. If the same order is found we add 1 to the similarity score
            for index in range(len(match_list) - 1):
                if match_list[index + 1] == match_list[index] + 1:
                    similarity_score += 1

    return similarity_score


def analysePOP(population):
    salesmen_data = []
    similarity_data = []
    pairs_to_compare = []
    num_unique_pairs = int(len(population) * 0.5)

    # We create a list containing the number of salesmen in each individual in the population
    for individuals in population:
        salesmen_data.append(len(individuals))

    # We create a list containing a select number of unique pairs in the population to compare
    while len(similarity_data) != num_unique_pairs:
        individual_one = int(random.random() * len(population) - 1)
        individual_two = int(random.random() * len(population) - 1)

        comparing_pair = (individual_one, individual_two)

        # Check if the selected pair is already is already added to the list
        if comparing_pair in pairs_to_compare or reversed(comparing_pair) in pairs_to_compare:
            continue
        else:
            pairs_to_compare.append(comparing_pair)

        current_index = len(pairs_to_compare) - 1
        similarity_data.append(similarity(population, pairs_to_compare, current_index))

    return salesmen_data, similarity_data


def PopAnalytics(population, method_used):
    salesmen_data, similarity_data = analysePOP(population)

    mean_salesmen = sum(salesmen_data) / len(salesmen_data)
    mean_similarity = sum(similarity_data) / len(similarity_data)

    temp_data = []
    for salesmen in salesmen_data:
        temp_data.append((salesmen - mean_salesmen) ** 2)
    salesmen_variance = sum(temp_data) / (len(temp_data) - 1)
    salesmen_sigma = math.sqrt(salesmen_variance)

    temp_data_ = []
    for similaritys in similarity_data:
        temp_data_.append((similaritys - mean_similarity) ** 2)
    similarity_variance = sum(temp_data_) / (len(temp_data_) - 1)
    similarity_sigma = math.sqrt(similarity_variance)

    x = np.linspace(mean_salesmen - 3 * salesmen_sigma, mean_salesmen + 3 * salesmen_sigma, 100)
    x_ = np.linspace(mean_similarity - 3 * similarity_sigma, mean_similarity + 3 * similarity_sigma, 100)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle(f'{method_used} Population Analytics')

    ax1.plot(x, stats.norm.pdf(x, mean_salesmen, salesmen_sigma))
    ax1.set_ylabel('Salesmen')

    ax2.plot(x_, stats.norm.pdf(x_, mean_similarity, similarity_sigma))
    ax2.set_ylabel('Similarity')

    plt.show()


def brute_force(taskList):
    start = time.time()
    min_length = calc_length(taskList, range(len(taskList)))
    min_path = range(len(taskList))
    print(range(len(taskList)))

    for path in permutations(range(len(taskList))):
        length = calc_length(taskList, path)
        if length < min_length:
            min_length = length
            min_path = path
            print("min_length: ", min_length)

    print("min_path: ", min_path)
    tottime = time.time() - start
    print("Found path of length %s in %s seconds" % (round(min_length, 2), round(tottime, 2)))
    return min_path


def dist_squared(c1, c2):
    t1 = c2[0] - c1[0]
    t2 = c2[1] - c1[1]
    return t1 ** 2 + t2 ** 2


def calc_length(cities, path):
    length = 0
    for i in range(len(path)):
        length += math.sqrt(dist_squared(cities[path[i - 1]], cities[path[i]]))
    return length


taskList = [(67,423), (381,127), (247,224), (325,394), (46,14), (417,216), (381,1), (222,360), (114,472), (450,15), (12,270), (469,190), (108,211), (14,110), (218,247), (116,115), (109,229), (144,10), (418,278), (321,92), (496,429), (60,166), (360,355), (468,211), (415,335)]
#taskList = [(422,368), (430,268), (81,439), (444,412), (261,136), (357,235), (227,215), (291,12), (293,315), (369,32)]

#brute_force(taskList)