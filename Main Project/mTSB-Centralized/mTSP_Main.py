from GA_Functions import *
from Analytics import *
import cv2
import matplotlib.pyplot as plt
import time



taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500
POP_SIZE = 80
ELITE_SIZE = 10
MUTATION_RATE = 0.2
MAX_GENERATIONS = 500
BREAKPOINT = 100


#random.seed(1)

#taskList = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)
taskList = taskGeneratortesting(taskList)
print(taskList)

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, breakpoint):
    home_city = population.pop(0)
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
    print("--- %s seconds ---" % int((time.time() - start_time)))
    cv2.imshow("Connections", map_city)
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')

    plt.show()
    cv2.waitKey()


start_time = time.time()
geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUTATION_RATE, generations=MAX_GENERATIONS, breakpoint=BREAKPOINT)

#PopAnalytics(initial_pop, "Random")
