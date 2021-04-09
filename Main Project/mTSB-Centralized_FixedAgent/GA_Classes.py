import numpy as np
import random
from typing import *


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


class Selection:
    def __init__(self, population, popRanked, eliteSize, selectionSize):
        self.popRanked = popRanked
        self.eliteSize = eliteSize
        self.population = population
        self.selectionSize = selectionSize

    # Selects the best fitting individual in a selected subset of a chosen size
    def tournament_selection(self):
        selectionResults = []
        selectionPool = random.sample(self.popRanked, len(self.popRanked))

        # Add the elites directly to the mating pool
        for i in range(0, self.eliteSize):
            selectionResults.append(self.popRanked[i][0])

        # Choose the remaining individuals to the mating pool through tournament selection
        for i in range(0, len(self.popRanked) - self.eliteSize):
            temp_subPool = random.sample(selectionPool, self.selectionSize)

            max_index = temp_subPool[0][0]
            last_fitness = temp_subPool[0][1]
            for index, fitness in temp_subPool:
                if last_fitness < fitness:
                    max_index = index
                last_fitness = fitness
            selectionResults.append(max_index)

        return selectionResults

    # Creates a list of the best suited routes
    def matingPool(self):
        matingpool = []
        selectionResults = self.tournament_selection()
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            matingpool.append(self.population[index])
        return matingpool


class Crossover:
    def __init__(self, matingPool, eliteSize):
        self.matingPool = matingPool
        self.eliteSize = eliteSize

    @staticmethod
    def continuous(individual):
        continuous_indi = []
        for g in range(len(individual)):
            if g < len(individual):
                continuous_indi.extend(individual[g])
                continuous_indi.append(0)
            else:
                break
        return continuous_indi

    @staticmethod
    def compare(parent1, parent2):
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

    @staticmethod
    def create_fragment(fragment, remainder):
        # Order the fragments in a nested list for reconstruction
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
    def crossover(self, parent1: List[object], parent2: List[object]) -> List[object]:
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

        options = [p1_breakpoints, p2_breakpoints]
        selected_breakpoints = random.choice(options)
        for breakpoints in selected_breakpoints:
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

        return child_final

    def evolve(self):
        newPopulation = []
        matingpool = self.matingPool
        pool = random.sample(matingpool, len(matingpool))
        legth = len(matingpool) - self.eliteSize

        # We insure that our best solutions/individuals are passed directly to the next generation without change
        for i in range(self.eliteSize):
            newPopulation.append(matingpool[i])

        # The remaining children in the next generation are a product of the crossover method
        for i in range(legth):
            parent1 = self.continuous(pool[i])
            parent2 = self.continuous(pool[len(pool) - i - 1])
            newPopulation.append(self.crossover(parent1, parent2))

        return newPopulation


class Mutation:
    def __init__(self, population, mutation_rate):
        self.mut_rate = mutation_rate
        self.population = population

    def mutate(self):
        newPopulation = [0] * (len(self.population))
        newPopulation[0] = self.population[0]  # Store the best individual without change (The king)
        mutation_types = {0: lambda x: Mutation.sequence_inversion(x),
                          1: lambda x: Mutation.gene_transposition(x),
                          2: lambda x: Mutation.gene_insertion(x),
                          3: lambda x: Mutation.cross_gene_insertion(x),
                          4: lambda x: Mutation.cross_gene_swap(x)}

        for i in range(1, len(self.population)):
            individual = self.population[i]

            # Randomly choose if the individual should be mutated
            if random.random() <= self.mut_rate:
                # Select a random mutation to apply to the individual
                selected_mutation = random.choice(list(mutation_types.values()))
                newPopulation[i] = selected_mutation(individual)

            else:
                newPopulation[i] = individual

        return newPopulation

    # In-Route mutation. Inverts a chosen subset of a selected genome
    @staticmethod
    def sequence_inversion(individual):
        # Select a genome from the individual at random
        k = random.randint(0, len(individual) - 1)
        genome = individual[k]

        if len(genome) > 1:
            # Randomly choose a start and end index to specify the gene sequence to be inverted
            start_index = random.randint(0, len(genome) - 2)
            end_index = random.randint(start_index, len(genome) - 1)

            # Insure that at least two genes are always being inverted
            if start_index == end_index:
                end_index += 1

            # Take out the selected sequence and invert it
            subset = genome[start_index:end_index + 1]
            subset.reverse()

            # Reinsert the inverted gene sequence into the original genome and insert into the individual
            genome[start_index:end_index + 1] = subset
            individual[k] = genome

        return individual

    # In-Route mutation. Selects two genes in a selected genome and swaps them
    @staticmethod
    def gene_transposition(individual):
        #  Select a random genome from the individual
        k = random.randint(0, len(individual) - 1)

        # Insure that the genome selected has at least two genes
        while len(individual[k]) <= 1:
            k = random.randint(0, len(individual) - 1)

        # Randomly take two genes from the genome to be switched
        gene1, gene2 = random.sample(individual[k], 2)

        #  Takes the index positions, to only swap the chosen genes
        a, b = individual[k].index(gene1), individual[k].index(gene2)
        individual[k][b], individual[k][a] = individual[k][a], individual[k][b]

        return individual

    # In-Route mutation. Moves a gene in a genome to another index location
    @staticmethod
    def gene_insertion(individual):

        #  Select a random genome from the individual
        k = random.randint(0, len(individual) - 1)
        while len(individual[k]) <= 1:
            k = random.randint(0, len(individual) - 1)

        # Select a gene to be moved and a place to move it to
        selected_gene = individual[k].pop(random.randint(0, len(individual[k]) - 1))
        insertion_point = random.randint(0, len(individual[k]) - 1)

        # Insert the gene into its new index location
        individual[k].insert(insertion_point, selected_gene)

        return individual

    # Cross-Route mutation. Takes a gene from one genome and inserts it in another
    @staticmethod
    def cross_gene_insertion(individual):
        # Randomly sample two genomes to be manipulated
        genome1, genome2 = random.sample(individual, 2)

        # Insure that at least one of the genomes has more than one gene
        while len(genome1) and len(genome2) <= 1:
            genome1, genome2 = random.sample(individual, 2)
        genome1_index, genome2_index = individual.index(genome1), individual.index(genome2)

        # Insure that we don't remove a gene from a genome with a single gene
        if len(genome1) == 1:
            r_genome = genome2_index
            e_genome = genome1_index
        elif len(genome2) == 1:
            r_genome = genome1_index
            e_genome = genome2_index
        else:
            r_genome = random.choice([genome1_index, genome2_index])
            if r_genome == genome1_index:
                e_genome = genome2_index
            else:
                e_genome = genome1_index

        # Remove the selected gene from the chosen genome and insert it into the other
        selected_gene = individual[r_genome].pop(random.randint(0, len(individual[r_genome])-1))
        individual[e_genome].insert(random.randint(0, len(individual[e_genome])-1), selected_gene)

        return individual

    # Takes a gene from two different genomes and swaps them
    @staticmethod
    def cross_gene_swap(individual):
        # Randomly sample two genomes to be manipulated
        genome1, genome2 = random.sample(individual, 2)
        genome1_index, genome2_index = individual.index(genome1), individual.index(genome2)

        # Select two genes from the two genomes to be swapped
        select_element1 = random.randint(0, len(individual[genome1_index]) - 1)
        select_element2 = random.randint(0, len(individual[genome2_index]) - 1)
        swap_element1 = individual[genome1_index][select_element1]
        swap_element2 = individual[genome2_index][select_element2]

        # Swap the two elements
        individual[genome1_index][select_element1] = swap_element2
        individual[genome2_index][select_element2] = swap_element1

        return individual
