import random
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import math


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
    num_unique_pairs = int(len(population)*0.5)

    # We create a list containing the number of salesmen in each individual in the population
    for individuals in population:
        salesmen_data.append(len(individuals))

    # We create a list containing a select number of unique pairs in the population to compare
    while len(similarity_data) != num_unique_pairs:
        individual_one = int(random.random() * len(population)-1)
        individual_two = int(random.random() * len(population)-1)

        comparing_pair = (individual_one, individual_two)

        # Check if the selected pair is already is already added to the list
        if comparing_pair in pairs_to_compare or reversed(comparing_pair) in pairs_to_compare:
            continue
        else:
            pairs_to_compare.append(comparing_pair)

        current_index = len(pairs_to_compare)-1
        similarity_data.append(similarity(population, pairs_to_compare, current_index))

    return salesmen_data, similarity_data


def PopAnalytics(population):
    salesmen_data, similarity_data = analysePOP(population)

    mean_salesmen = sum(salesmen_data) / len(salesmen_data)
    mean_similarity = sum(similarity_data) / len(similarity_data)

    temp_data = []
    for salesmen in salesmen_data:
        temp_data.append((salesmen - mean_salesmen) ** 2)
    salesmen_variance = sum(temp_data) / (len(temp_data) - 1)
    salesmen_sigma = math.sqrt(salesmen_variance)

    x = np.linspace(mean_salesmen - 3 * salesmen_sigma, mean_salesmen + 3 * salesmen_sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mean_salesmen, salesmen_sigma))
    plt.show()

    temp_data_ = []
    for similaritys in similarity_data:
        temp_data_.append((similaritys - mean_similarity) ** 2)
    similarity_variance = sum(temp_data_) / (len(temp_data_) - 1)
    similarity_sigma = math.sqrt(similarity_variance)

    x = np.linspace(mean_similarity - 3 * similarity_sigma, mean_similarity + 3 * similarity_sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mean_similarity, similarity_sigma))
    plt.show()
