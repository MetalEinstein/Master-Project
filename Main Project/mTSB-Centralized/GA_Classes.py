import numpy as np
import random
import pandas as pd
from typing import *
from mutation_test import *


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Fitness:
    def __init__(self, population, homeCity):
        self.homeCity = homeCity
        self.population = population
        #self.route = route
        self.distance = 0
        self.fitness = 0.0

    def routeDistance(self):
        routeDistance = []
        for i in range(len(self.population)):
            geneDistance = 0
            individual = self.population[i]
            # print("\n")
            # print("individual: ", individual)
            for j in range(len(individual)):
                gene = individual[j]
                # print("gene: ", gene)
                # Add home town to start of specific agent route
                gene.insert(0, self.homeCity)
                for k in range(len(gene)):
                    fromCity = gene[k]
                    toCity = None
                    if k + 1 < len(gene):
                        toCity = gene[k + 1]
                    else:
                        # When we get to the last city in the list we add the distance from it back to the initial city
                        toCity = gene[0]
                    geneDistance += fromCity.distance(toCity)
                # Delete home city again, so we  don't end up with multiple home cities in a row
                gene.pop(0)
            routeDistance.append(geneDistance)
        return routeDistance


    def routeFitness(self):
        fitnessList = [0] * len(self.routeDistance())
        for i in range(len(self.routeDistance())):
            if fitnessList[i] == 0:
                fitnessList[i] = 1/self.routeDistance()[i]

        return fitnessList


class Crossover:
    def __init__(self, population, popRanked, eliteSize):
        self.popRanked = popRanked
        self.eliteSize = eliteSize
        self.population = population

    # Creates a mating pool by assigning probabilities according to the individual fitness scores
    # Better fitness score = Higher probability of being picked
    # Also insures that the best individuals in the population carries on to the next
    def selection(self):
        selectionResults = []

        # Assign probabilities to each individual in the population
        df = pd.DataFrame(np.array(self.popRanked), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        # Picks out the top individuals in the population for the mating-pool. Not chosen by probability
        for i in range(0, self.eliteSize):
            selectionResults.append(self.popRanked[i][0])  # Appends list with the index of the best individuals

        # Fills out the remaining mating pool according to the probabilities assigned to each individual
        for i in range(0, len(self.popRanked) - self.eliteSize):
            pick = 100 * random.random()
            for i in range(0, len(self.popRanked)):
                if pick <= df.iat[i, 3]:
                    selectionResults.append(self.popRanked[i][0])
                    break
        return selectionResults

    # Creates a list of the best suited routes
    def matingPool(self):
        matingpool = []
        selectionResults = self.selection()
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            matingpool.append(self.population[index])
        return matingpool

    def continuous(self, individual):
        continuous_indi = []
        for g in range(len(individual)):
            if g < len(individual):
                continuous_indi.extend(individual[g])
                continuous_indi.append(0)
            else:
                break
        return continuous_indi

    def compare(self, parent1, parent2):
        match_list = []
        fragment = []

        # Compare element i in gene 1 with all elements in gene 2
        # If element i in gene1 is found in gene 2 return the index at which the match occurred
        for i in range(len(parent1)):
            for k in range(len(parent2)):
                if parent1[i] == parent2[k] and parent1[i] != 0:
                    match_list.append(k)
                    break

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

        # Find the tasks that are not part of a common sequence in both parents
        remainder = [task for task in parent2 if task not in fragment and task != 0]
        return match_list, fragment, remainder

    def create_fragment(self, fragment, remainder):
        # Order the fragments in a nested list for reconstruction
        sub_list = []
        fragment_list = []
        while len(fragment) > 0:
            if 0 in fragment:
                sub_list = fragment[0:fragment.index(0)]
                fragment_list.append(sub_list)
                del fragment[0:fragment.index(0) + 1]
            else:
                fragment_list.append(fragment)
                fragment = []

        for sub_fragment in remainder:
            fragment_list.append([sub_fragment])
        return fragment_list

    # Takes in two individuals and mates them using ordered crossover resulting in a new route
    def crossover(self, parent1: List[object], parent2: List[object], p1, p2) -> List[object]:
        if parent1 == parent2:
            parent2 = parent1

        # --- CROSSOVER OPERATOR (DPX) ---
        child = []
        considerations = []

        # Keeping track of the breakpoints for both parents
        p1_breakpoints = [i for i in range(len(parent1)) if parent1[i] == 0]
        p2_breakpoints = [i for i in range(len(parent2)) if parent2[i] == 0]

        match_list, fragment, remainder = self.compare(parent1, parent2)
        fragment_list = self.create_fragment(fragment, remainder)

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

        if p1 < p2:
            best_breakpoint = p1_breakpoints
        else:
            best_breakpoint = p2_breakpoints

        # TODO implement the original breakpoints from the parent with the best fitness
        for breakpoints in best_breakpoint:
            child.insert(breakpoints, 0)

        child_final = []
        while len(child) > 0:
            if 0 in child:
                sub_list = child[0:child.index(0)]
                child_final.append(sub_list)
                for i in range(0, child.index(0)+1):
                    child.pop(0)
            else:
                child_final.append(fragment)
                child = []
        #print("Final child: ", child_final)
        return child_final


    def evolve(self):
        newPopulation = []
        matingpool = self.matingPool()

        for i in range(self.eliteSize):
            newPopulation.append(matingpool[i])

        for i in range(len(self.population) - len(newPopulation)):
            # TODO we might want to be more picky with the parents. We could base it on probability
            p1 = int(random.random()*len(matingpool)-1)
            p2 = int(random.random()*len(matingpool)-1)
            parent1 = self.continuous((matingpool[p1]))
            parent2 = self.continuous((matingpool[p2]))
            #newPopulation = self.crossover(parent1, parent2)

            newPopulation.append(self.crossover(parent1, parent2, p1, p2))
        return newPopulation


class Mutation:
    def __init__(self, population, mutation_rate, mutation_rate2):
        self.mut_1 = mutation_rate
        self.mut_2 = mutation_rate2
        self.population = population

    def mutate(self):
        newPopulation = [0] * (len(self.population))

        for i in range(len(self.population)):
            individual = self.population[i]
            # Check if individual_i will get this mutation
            # Mutation 1 (switch two genes)
            if random.random() <= self.mut_1 and len(individual) > 1:
                #print("\n")
                #print("Parting individual", i, "-------------------------------------------")
                newPopulation[i] = partition_insertion(individual)
            else:
                newPopulation[i] = individual

            # if random.random() <= self.mut_1:
            #     #print("\n")
            #     newIndividual = partition_insertion(individual)
            #     newPopulation[i] = newIndividual
            # else:
            #     newPopulation[i] = individual

            # Check if individual_i will get this mutation
            # Mutation 1 (switch two genes)
            # individual2 = newPopulation[i]
            #print("Individual2: ", individual2)
            #if random.random() <= self.mut_2:
                #print("Inverting individual", i, "-------------------------------------------")

                #newIndividual = self.sequence_inversion(individual2)
                #newPopulation[i] = newIndividual
                #newPopulation[i] = self.sequence_inversion(newPopulation[i])
            # # TODO: we might be able to leave the below two lines out. Too tired to test now
            # else:
            #     newPopulation[i] = newPopulation[i]
        # Insert the best individual from the original population
        #newPopulation.insert(0, self.population[0])
        return newPopulation


    # def swap(self, individual):
    #     print("individual: ", individual)
    #     print("length: ", len(individual))
    #     genome1, genome2 = random.sample(individual, 2)
    #
    #     start_index = random.randint(0, len(genome1) - 1)
    #     end_index = random.randint(0, len(genome2) - 1)
    #
    #     newgenome2 = genome2[end_index]
    #
    #     genome2[end_index] = genome1[start_index]
    #     genome1[start_index] = newgenome2
    #
    #     return individual

    def sequence_inversion(self, individual):
        # print("\nPrevious Individual: ", individual)

        # Select a genome from the individual at random
        k = random.randint(0, len(individual) - 1)
        genome = individual[k]
        # print("Selected Genome: ", individual[k])

        if len(genome) > 1:
            print("Inverting sequence ------------------------")
            # Randomly choose a start and end index to specify the gene sequence to be inverted
            start_index = random.randint(0, len(genome) - 2)
            end_index = random.randint(start_index, len(genome) - 1)
            # print(f"Selected Sequence: {start_index} -> {end_index + 1}")

            # Insure that at least two genes are always being inverted
            if start_index == end_index:
                end_index += 1

            # Take out the selected sequence and invert it
            subset = genome[start_index:end_index + 1]
            # print("\nGene subset: ", subset)
            subset.reverse()
            # print("Reversed Gene subset: ", subset)

            # Reinsert the inverted gene sequence into the original genome and insert into the individual
            genome[start_index:end_index + 1] = subset
            individual[k] = genome
            # print("New Individual: ", individual)

        return individual
