from GA_Functions import *
import cv2
import matplotlib.pyplot as plt
import time
import matplotlib
import numpy as np

#Best Score: 3391.88

taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500
POP_SIZE = 50
ELITE_SIZE = 5
MUT_RATE = 0.20
MAX_GENERATIONS = 500
BREAKPOINT = 50
K_AGENTS = 3

taskList = taskGeneratortesting(taskList)


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, breakpoint, numAgents):
    home_city = population.pop(0)
    pop = initialPopulation(popSize, population, numAgents)
    generation_diff = []
    progress = []
    mean_progress = []

    temp_rank = rankRoutes(pop, home_city)
    progress.append(1 / temp_rank[0][1])  # We track progress according to the best route

    sum_distance = 0
    for i in range(len(temp_rank)):
        sum_distance += 1/temp_rank[i][1]
    mean_progress.append(sum_distance/len(temp_rank))

    p_counter = 0
    for i in range(0, generations):
        sum_distance = 0
        p_counter += 1

        progress_past = 1 / rankRoutes(pop, home_city)[0][1]
        rankedFitness = rankRoutes(pop, home_city)
        postMu, postSel, pop = evolvePopulation(pop, rankedFitness, eliteSize, mutationRate, i)
        progress_future = 1 / rankRoutes(pop, home_city)[0][1]
        generation_diff.append(abs(progress_past - progress_future))

        progress.append(1 / rankedFitness[0][1])
        print("Current Distance: " + str(1 / rankedFitness[0][1]) + ",   ", "Generation: " + str(i))

        for f in range(len(rankedFitness)):
            sum_distance += 1/rankedFitness[f][1]
        mean_progress.append(sum_distance/len(rankedFitness))

        """
        # PLOTTING Standard Deviation
        std_list_Sel = [postSel]
        std_list_Mu = [postMu]
        gen = [i]
        if i % 5 == 0:
            std_list_Sel.append(postSel)
            std_list_Mu.append(postMu)
            gen.append(i)

            plt.subplot(2, 1, 1)
            plt.plot(gen, std_list_Sel, '-ok')
            plt.title('Population Deviation After Selection and Mutation')
            plt.ylabel('Standard Deviation')

            plt.subplot(2, 1, 2)
            plt.plot(gen, std_list_Mu, '-ok')
            plt.xlabel('Generation')
            plt.ylabel('Standard Deviation')

            plt.pause(0.005)
        """

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

    plt.subplot(2, 1, 1)
    plt.plot(progress)
    plt.title('Distance for King and Mean distance for Population over the Generations')
    plt.ylabel('Distance of King')

    plt.subplot(2, 1, 2)
    plt.plot(mean_progress)
    plt.ylabel('Mean distance of Population')
    plt.xlabel('Generation')

    plt.show()
    cv2.waitKey()


start_time = time.time()
geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUT_RATE,
                 generations=MAX_GENERATIONS, breakpoint=BREAKPOINT, numAgents=K_AGENTS)

