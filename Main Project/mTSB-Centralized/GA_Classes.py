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

