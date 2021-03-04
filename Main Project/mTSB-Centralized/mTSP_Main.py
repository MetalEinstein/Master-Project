from GA_Functions import *
from Analytics import *
import cv2
import matplotlib.pyplot as plt



taskList = []
TASK_NUMBER = 20
MAP_SIZE = 300
POP_SIZE = 50
ELITE_SIZE = 5
MUTATION_RATE = 0.02


#random.seed(1)

taskList = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)
# home_city = taskList.pop(0)
# initial_pop = initialPopulation(POP_SIZE, taskList)
# print("\n")
# print("Initial population: ", initial_pop)
# #print("Length of population: ", len(initial_pop))
# rankedFitness = rankRoutes(initial_pop, home_city)
# print("Fitness scores: ", rankedFitness)
# evolvePopulation = evolvePopulation(initial_pop, rankedFitness, ELITE_SIZE, MUTATION_RATE)
# print("Evolved Population: ", evolvePopulation)

# (tasklist, POP_SIZE, ELITE_SIZE, MUTATION_RATE, DEF GENERATIONS, DEF BREAKPOINT)

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, breakpoint):
    home_city = population.pop(0)
    print(home_city)
    pop = initialPopulation(popSize, population)
    generation_diff = []
    progress = []
    progress.append(1 / rankRoutes(pop, home_city)[0][1])  # We track progress according to the best route

    p_counter = 0
    for i in range(0, generations):
        p_counter += 1
        # print("counter: ", p_counter)

        progress_past = 1 / rankRoutes(pop, home_city)[0][1]
        #pop = nextGeneration(pop, eliteSize, mutationRate)
        rankedFitness = rankRoutes(pop, home_city)
        pop = evolvePopulation(pop, rankedFitness, eliteSize, mutationRate)
        progress_future = 1 / rankRoutes(pop, home_city)[0][1]
        generation_diff.append(abs(progress_past - progress_future))
        # print("ranked routes:", rankedFitness)
        # print("ranked routes:", rankedFitness[0][1])
        # progress.append(1 / rankRoutes(pop, home_city)[0][1])
        progress.append(1 / rankedFitness[0][1])
        print("Current Distance: " + str(1 / rankedFitness[0][1]) + ",   ", "Generation: " + str(i))

        # We check the progress over a set number of generations. If progress = 0 we stop the algorithm
        # Might be an alternative just to use breakpoint instead of iteration for a set number of generations
        if p_counter == breakpoint:
            p_counter = 0
            total_diff = sum(generation_diff)
            generation_diff.clear()

            if total_diff == 0:
                break

    best_indi = rankedFitness[0][0]
    map_city = city_connect(pop, MAP_SIZE, best_indi, home_city)

    best_indi = pop[best_indi]
    print("agents: ")
    for agents in best_indi:
        print(agents)
    cv2.imshow("Connections", map_city)
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')

    plt.show()
    cv2.waitKey()


geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUTATION_RATE, generations=200, breakpoint=20)

#PopAnalytics(initial_pop, "Random")

# print("Home City: ", home_city)

"""
for i in range(len(taskList)):
    print(taskList[i].x)
"""
