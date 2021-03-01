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

    if parent1 == parent2:
        return parent1

    print("Parent 1: ", parent1)
    print("Parent 2: ", parent2)


    # --- CROSSOVER OPERATOR (DPX) ---
    child = []
    match_list = []
    fragment = []
    fragment_list = []
    considerations = []

    # Compare element i in gene 1 with all elements in gene 2
    # If element i in gene1 is found in gene 2 return the index at which the match occurred
    for i in range(len(parent1)):
        for k in range(len(parent2)):
            if parent1[i] == parent2[k] and parent1[i] != 0:
                match_list.append(k)
                break

    print("Match List: ", match_list)

    # Check if the matches occurred in sequence and if they did add them as a fragment
    former_match = False
    for i in range(len(match_list)):
        if i < len(match_list) - 1:
            if match_list[i + 1] == match_list[i] + 1 or match_list[i + 1] == match_list[i] - 1:
                former_match = True
                fragment.append(parent2[match_list[i]])

            else:
                if former_match:
                    fragment.append(parent2[match_list[i]])
                    fragment.append(0)
                    former_match = False
        else:
            if former_match:
                fragment.append(parent2[match_list[i]])

    print("\nFragments: ", fragment)
    # Find the tasks that are not part of a common sequence in both parents
    remainder = [task for task in parent2 if task not in fragment]
    print("Remainder: ", remainder)

    # Order the fragments in a nested list for reconstruction
    sub_list = []
    for sub_fragment in fragment:
        if sub_fragment != 0:
            sub_list.append(sub_fragment)
        else:
            fragment_list.append(sub_list)
            sub_list = []

    for sub_fragment in remainder:
        fragment_list.append([sub_fragment])

    print("\nFragment List: ", fragment_list)

    # Points to consider for greedy reconstruction
    for points in fragment_list:
        if len(points) == 1:
            considerations.append(points[0])
        else:
            considerations.append(points[0])
            considerations.append(points[-1])

    # The initial fragment is selected and added as the first fragment in the reconstruction list
    initial_task = random.choice(considerations)
    reconstructed = [frag for frag in fragment_list if initial_task in frag]
    initial_endpoint = reconstructed[0][-1]

    fragment_list.remove(reconstructed[0])
    if len(reconstructed[0]) == 1:
        considerations.remove(initial_endpoint)
    else:
        considerations.remove(initial_endpoint)
        considerations.remove(reconstructed[0][0])

    distance_list = []
    task_index_endpoint = parent1.index(initial_endpoint)

    while len(fragment_list) != 0:
        i = 0
        if i == 0:
            # Calculate the distance between initial endpoint and all other end and startpoints among considerations
            for tasks in considerations:
                parent_index_nextpoint = parent1.index(tasks)
                distance_list.append(parent1[task_index_endpoint].distance(parent1[parent_index_nextpoint]))
            min_index = distance_list.index(min(distance_list))
            distance_list = []
            next_fragment = [frag for frag in fragment_list if considerations[min_index] in frag]
            next_fragment = next_fragment[0]

            # If the lowest distance is to a fragment startpoint, add associated fragment directly to reconstruction
            # Else reverse and add it
            if next_fragment[0] == considerations[min_index]:
                reconstructed.append(next_fragment)
            else:
                end = next_fragment[-1]
                start = next_fragment[0]
                next_fragment[0] = end
                next_fragment[-1] = start

                reconstructed.append(next_fragment)

            # Remove fragment and associated considerations
            fragment_list.remove(next_fragment)
            if len(next_fragment) == 1:
                considerations.remove(next_fragment[0])
            else:
                considerations.remove(next_fragment[0])
                considerations.remove(next_fragment[-1])
            i = 1

        else:
            endpoint = parent1.index(reconstructed[-1][-1])
            for tasks in considerations:
                parent_index_nextpoint = parent1.index(tasks)
                distance_list.append(parent1[endpoint].distance(parent1[parent_index_nextpoint]))
            min_index = distance_list.index(min(distance_list))
            distance_list = []
            next_fragment = [frag for frag in fragment_list if considerations[min_index] in frag]
            next_fragment = next_fragment[0]

            # If the lowest distance is to a fragment startpoint, add associated fragment directly to reconstruction
            # Else reverse and add it
            if next_fragment[0] == considerations[min_index]:
                reconstructed.append(next_fragment)
            else:
                end = next_fragment[-1]
                start = next_fragment[0]
                next_fragment[0] = end
                next_fragment[-1] = start

            # Remove fragment and associated considerations
            fragment_list.remove(next_fragment)
            if len(next_fragment) == 1:
                considerations.remove(next_fragment[0])

            else:
                considerations.remove(next_fragment[0])
                considerations.remove(next_fragment[-1])

    for frags in reconstructed:
        child.extend(frags)
    print("\nChild: ", child)

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
