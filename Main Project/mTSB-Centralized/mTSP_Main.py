from GA_Functions import *

taskList = []
TASK_NUMBER = 40
MAP_SIZE = 300

taskList = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)
home_city = taskList.pop(0)

initial_pop = initialPopulation(40, taskList)
print("\n")
print(len(initial_pop))

# print("Home City: ", home_city)

"""
for i in range(len(taskList)):
    print(taskList[i].x)
"""
