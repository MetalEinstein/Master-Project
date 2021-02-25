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
            routeDistance.append(geneDistance)
        return routeDistance


    def routeFitness(self):
        fitnessList = [0] * len(self.routeDistance())
        for i in range(len(self.routeDistance())):
            if fitnessList[i] == 0:
                fitnessList[i] = 1/self.routeDistance()[i]

        return fitnessList


class Crossover:
    def __init__(self, popRanked, eliteSize):
        self.popRanked = popRanked
        self.eliteSize = eliteSize

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
