from GA_Functions import *
import cv2
import matplotlib.pyplot as plt
import time

# BEST SCORE SO FAR = 3401 IN 199 GENERATIONS

taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500  # meter
POP_SIZE = 50
ELITE_SIZE = 5
MUT_RATE = 0.20
MAX_GENERATIONS = 500
BREAKPOINT = 50
INITIAL_SELECTION_SIZE = 6
#VELOCITY = 100  # 100 / hour

taskList, K_AGENTS = taskGeneratortesting(taskList)
#taskList, K_AGENTS = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, breakpoint, numAgents, sel_size):
    velocity = 0.7  # m/s
    home_city = population.pop(0)
    pop = initialPopulation(popSize, population, numAgents)
    generation_diff = []
    progress = []
    mean_progress = []

    temp_rank = rankRoutes(pop, home_city, velocity)
    progress.append(1 / temp_rank[0][1])  # We track progress according to the best route

    sum_distance = 0
    for i in range(len(temp_rank)):
        sum_distance += 1/temp_rank[i][1]
    mean_progress.append(sum_distance/len(temp_rank))

    p_counter = 0
    for i in range(0, generations):
        sum_distance = 0
        p_counter += 1

        progress_past = 1 / rankRoutes(pop, home_city, velocity)[0][1]
        rankedFitness = rankRoutes(pop, home_city, velocity)
        pop = evolvePopulation(pop, rankedFitness, eliteSize, mutationRate, sel_size)
        progress_future = 1 / rankRoutes(pop, home_city, velocity)[0][1]
        generation_diff.append(abs(progress_past - progress_future))

        progress.append(1 / rankedFitness[0][1])
        print("Current Distance: " + str(1 / rankedFitness[0][1]) + ",   ", "Generation: " + str(i))

        for f in range(len(rankedFitness)):
            sum_distance += 1/rankedFitness[f][1]
        mean_progress.append(sum_distance/len(rankedFitness))

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
                 generations=MAX_GENERATIONS, breakpoint=BREAKPOINT, numAgents=K_AGENTS, sel_size=INITIAL_SELECTION_SIZE)

