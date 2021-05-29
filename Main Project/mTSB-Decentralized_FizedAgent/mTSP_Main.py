from GA_Functions import *
import cv2
import matplotlib.pyplot as plt
import time
import ray
from numba import jit, cuda


taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500
POP_SIZE = 50
ELITE_SIZE = 5
MUT_RATE = 0.90
MAX_GENERATIONS = 500
BREAKPOINT = 50
INITIAL_SELECTION_SIZE = 15

taskList, K_AGENTS = taskGeneratortesting(taskList)
K_AGENTS = 3
#taskList, K_AGENTS = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)


@ray.remote()
def evolvePopulation(population, popRanked, eliteSize, mutationRate, sel_size):
    matingPool = Selection(population, popRanked, eliteSize, sel_size).matingPool()
    newCrossoverPopulation = Crossover(matingPool, eliteSize).evolve()
    newPopulation = Mutation(newCrossoverPopulation, mutationRate).mutate()

    return newPopulation


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, breakpoint, numAgents, sel_size):
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

        # Generate N new populations in parallel and thereafter rank them
        pop = ray.get([evolvePopulation.remote(pop, rankedFitness, eliteSize, mutationRate, sel_size) for _ in range(3)])
        popsFitness = [rankRoutes(pops, home_city) for pops in pop]

        # Find the id of the population with the best score
        best_pop_id = [1/popsFitness[pop_id][0][1] for pop_id, _ in enumerate(popsFitness)]
        print("Best pops scores: ", best_pop_id)
        best_pop_id = np.argmin(best_pop_id)
        print(f"Best pop id: {best_pop_id}\n")

        pop = pop[best_pop_id]

        progress_future = 1 / rankRoutes(pop, home_city)[0][1]
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


if __name__ == "__main__":
    ray.init(address='auto', _redis_password='5241590000000000')

    start_time = time.time()

    geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUT_RATE,
                     generations=MAX_GENERATIONS, breakpoint=BREAKPOINT, numAgents=K_AGENTS, sel_size=INITIAL_SELECTION_SIZE)



