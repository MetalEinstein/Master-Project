from GA_Functions import *
import seaborn as sns
import matplotlib as plt
import random


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


taskList = []
TASK_NUMBER = 10
MAP_SIZE = 300
POP_SIZE = 100

taskList = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)
home_city = taskList.pop(0)
initial_pop = initialPopulation(POP_SIZE, taskList)

print("Initial population: ", initial_pop)
print("Length of population: ", len(initial_pop))

fitness = rankRoutes(initial_pop, home_city)
print("Fitness scores: ", fitness)
print("\n")


salesmen_data, similarity_data = analysePOP(initial_pop)
print(f"The number of salesmen for each individual: {salesmen_data}")
print(f"The similarity score for a select number of uniquely compared individuals: {similarity_data}")

# print("Home City: ", home_city)

"""
for i in range(len(taskList)):
    print(taskList[i].x)
"""
