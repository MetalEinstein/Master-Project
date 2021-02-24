from GA_Functions import *

taskList = []
TASK_NUMBER = 10
MAP_SIZE = 300
POP_SIZE = 10

taskList = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)
home_city = taskList.pop(0)

initial_pop = initialPopulation(POP_SIZE, taskList)
print("\n")
print("Initial population: ", initial_pop)
print("Length of population: ", len(initial_pop))
fitness = rankRoutes(initial_pop, home_city)
print("Fitness scores: ", fitness)


# print("Home City: ", home_city)

"""
for i in range(len(taskList)):
    print(taskList[i].x)
"""
