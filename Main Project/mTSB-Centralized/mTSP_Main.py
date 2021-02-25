from GA_Functions import *

taskList = []
TASK_NUMBER = 10
MAP_SIZE = 300
POP_SIZE = 10
ELITE_SIZE = 3

taskList = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)
home_city = taskList.pop(0)

initial_pop = initialPopulation(POP_SIZE, taskList)
print("\n")
#print("Initial population: ", initial_pop)
#print("Length of population: ", len(initial_pop))
rankedFitness = rankRoutes(initial_pop, home_city)
print("Fitness scores: ", rankedFitness)
selection = Crossover(rankedFitness, ELITE_SIZE).selection()
print("Selected individuals: ", selection)


# print("Home City: ", home_city)

"""
for i in range(len(taskList)):
    print(taskList[i].x)
"""
