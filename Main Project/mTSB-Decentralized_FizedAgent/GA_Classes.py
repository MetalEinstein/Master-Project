import numpy as np
import random
from typing import *
import operator
import ray


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

    # Takes in two individuals and mates them using ordered crossover resulting in a new route
    @staticmethod
    def crossover(parent1, parent2):
        # Check if the parents are alike
        equal = False
        if parent1 == parent2:
            equal = True

        # Make parent 2 into a sequential list of genes for comparison with parent 1
        parent2_comparable = []
        for genomes in parent2:
            parent2_comparable.extend(genomes)
            parent2_comparable.append(0)

        # Compare the two parents and add similarities to a list
        fragments = []
        for genome in parent1:
            init_loop = True
            temp = []
            pre_index = 0

            # If the parents are alike we just avoid searching for similarities
            if equal or len(genome) == 1:
                fragments.append(genome)
                continue

            for gene in genome:
                next_index = parent2_comparable.index(gene)

                if init_loop:
                    temp.append(gene)
                    pre_index = next_index
                    init_loop = False
                    continue

                if next_index == pre_index + 1:
                    temp.append(gene)
                    pre_index = next_index
                    if genome.index(gene) == len(genome)-1:
                        fragments.append(temp)

                elif next_index == pre_index - 1:
                    temp.insert(0, gene)
                    pre_index = next_index
                    if genome.index(gene) == len(genome)-1:
                        fragments.append(temp)

                else:
                    fragments.append(temp)
                    temp = [gene]
                    pre_index = next_index

                    if genome.index(gene) == len(genome) - 1:
                        fragments.append(temp)

        # Reconstruct the list of fragments according to a distance heuristic
        frags_reconstructed = [fragments.pop(fragments.index(random.choice(fragments)))]
        for i in range(len(fragments)):
            if len(frags_reconstructed) == 1:
                consideration = frags_reconstructed[i][0]
            else:
                consideration = frags_reconstructed[i][-1]

            dist_list = {}
            for f_id, fragment in enumerate(fragments):
                if len(fragment) == 1:
                    dist = consideration.distance(fragment[0])
                    dist_list[(f_id, 0)] = dist
                else:
                    dist = consideration.distance(fragment[0])
                    dist_ = consideration.distance(fragment[-1])
                    dist_list[(f_id, 0)] = dist
                    dist_list[(f_id, len(fragment)-1)] = dist_

            # Sort the distance list according the lowest distance Low -> high
            dist_list = sorted(dist_list.items(), key=operator.itemgetter(1), reverse=False)
            lowest_dist_id = dist_list[0][0][0]  # Genome id

            # Reverse the selected fragment if the lowest distance is to the last element in the fragment
            if dist_list[0][0][1] != 0:  # Gene id. Check if it occurs in the beginning or the end of the genome
                fragments[lowest_dist_id] = fragments[lowest_dist_id][::-1]

            frags_reconstructed.append(fragments.pop(lowest_dist_id))

        # Make the fragment list continues in order for it to be remade using a parent blueprint
        extended_frags = []
        for frags in frags_reconstructed:
            extended_frags.extend(frags)

        # Choose a parent at random to act as the blueprint for task distribution among the agents in the child
        agent_blueprint = random.choice([parent1, parent2])

        # Create the child using the above blueprint
        child = []
        for genome in agent_blueprint:
            length = len(genome)
            child.append(extended_frags[0:length])
            del extended_frags[0:length]

        return child

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
            parent1 = pool[i]
            parent2 = pool[len(pool) - i - 1]
            newPopulation.append(Crossover.crossover(parent1, parent2))

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