import numpy as np
import random
import pandas as pd
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
        #self.route = route
        self.distance = 0
        self.fitness = 0.0

    def routeDistance(self):
        routeDistance = []
        for i in range(len(self.population)):
            geneDistance = 0
            individual = self.population[i]
            for j in range(len(individual)):
                gene = individual[j]
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
    def __init__(self, population, popRanked, eliteSize, mutation_rate):
        self.popRanked = popRanked
        self.eliteSize = eliteSize
        self.population = population
        self.mutation_rate = mutation_rate


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


    def evolve(self):
        newPopulation = []
        matingpool = self.matingPool()

        for i in range(self.eliteSize):
            #print("New pop: ", matingpool)
            newPopulation.append(matingpool[i])
            # matingpool.pop(0)
            # print("func new pop: ", matingpool)

        eliteOffset = len(self.population) - len(newPopulation)

        for i in range(eliteOffset):
            #TODO we might want to be more picky with the parents. We could base it on probability
            parent1 = random.sample(matingpool,1)
            parent2 = random.sample(matingpool,1)
            #newPopulation = self.crossover(parent1, parent2)
            print("newpopulation: ", newPopulation)
            #TODO change to output of crossover, when that function is working
            newPopulation = self.mutation(self.population)
            print("new population 1: ", newPopulation)
        return newPopulation


    def crossover(self, parent1, parent2):
        switchProb = random.random()
        for i in range(len(parent1)):
            print("i: ", len(parent1))
            #if switchProb >= 0.5:

    #TODO Make a mutation class instead, since there are going to be multiple mutations
    def mutation(self, population):
        newPopulation = []
        mutateProb = random.random()
        for i in range(len(population)):
            individual = population[i]
            # Check if individual_i will get this mutation
            # Mutation 1 (switch two genes)
            if mutateProb <= self.mutation_rate:
                print("Mutating")
                # Flatten list, since we need 1d list. Append 0 where original split was
                flatIndividual = self.flatten(individual)
                # Generate two genes to be switched
                gene1, gene2 = random.sample(flatIndividual, 2)
                # Switch genes
                a, b = flatIndividual.index(gene1), flatIndividual.index(gene2)
                flatIndividual[b], flatIndividual[a] = flatIndividual[a], flatIndividual[b]
                # Split list into lists by splitter value 0, so we get original list structure
                size = len(flatIndividual)
                idx_list = [idx + 1 for idx, val in
                            enumerate(flatIndividual) if val == 0]
                newIndividual = [flatIndividual[i: j] for i, j in
                       zip([0] + idx_list, idx_list +
                           ([size] if idx_list[-1] != size else []))]
                # Remove appended 0 from list, since it is no longer needed
                for item in newIndividual:
                    try:
                        item.remove(0)
                    except ValueError:
                        pass
                newPopulation.append(newIndividual)
            else:
                newPopulation.append(individual)
        return newPopulation


    def flatten(self, individual):
        newIndividual = []
        for sublist in individual:
            for subsublist in sublist:
                newIndividual.append(subsublist)
            newIndividual.append(0)  # To save the split locations
        return newIndividual



