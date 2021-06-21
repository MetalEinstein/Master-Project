from GA_Functions import *
import cv2
from Socket_Setup import *
import matplotlib.pyplot as plt
import pickle
import time


# GA Parameters
taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500
POP_SIZE = 50
ELITE_SIZE = 15
MUT_RATE = 0.9
MAX_GENERATIONS = 500
BREAKPOINT = 100
INITIAL_SELECTION_SIZE = 5

# Socket Parameters
NUM_WORKERS = 2


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

    bestdist=0
    p_counter = 0
    for i in range(0, generations):
        sum_distance = 0
        p_counter += 1

        progress_past = 1 / rankRoutes(pop, home_city)[0][1]
        rankedFitness = rankRoutes(pop, home_city)
        pop = evolvePopulation(pop, rankedFitness, eliteSize, mutationRate, sel_size)
        progress_future = 1 / rankRoutes(pop, home_city)[0][1]
        generation_diff.append(abs(progress_past - progress_future))

        progress.append(1 / rankedFitness[0][1])
        print("Current Distance: " + str(1 / rankedFitness[0][1]) + ",   ", "Generation: " + str(i))

        for f in range(len(rankedFitness)):
            sum_distance += 1/rankedFitness[f][1]
        mean_progress.append(sum_distance/len(rankedFitness))

        # We check the progress over a set number of generations. If progress = 0 we stop the algorithm
        # Might be an alternative just to use breakpoint instead of iteration for a set number of generations
        if bestdist is not (rankedFitness[0][0]):
            bestdist = (rankedFitness[0][0])
            p_counter = 0

        elif p_counter >= breakpoint:
            total_diff = sum(generation_diff)
            generation_diff.clear()

            if total_diff == 0:
                break

    return [pop[rankedFitness[0][0]], 1/rankedFitness[0][1], home_city]


start_time = time.time()

# Do initial clustering
taskList, K_AGENTS = taskGeneratortesting(taskList)
K_AGENTS = 3


# Connect to active clients
create_socket()
bind_socket()
accepting_connections(NUM_WORKERS)

# Start active clients
for conn in all_connections:
    conn.send(str.encode("0"))
    conn.recv(1024)

# Run GA
bestList = []
bestList.append(geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUT_RATE,
                 generations=MAX_GENERATIONS, breakpoint=BREAKPOINT, numAgents=K_AGENTS, sel_size=INITIAL_SELECTION_SIZE))

# Collect the best individuals from each agent in the network
# TODO Compare to message size doing data retrieval to load messages > 4096 bits
for conn in all_connections:
    #full_msg = ''
    while True:
        data = conn.recv(4096)
        #msglen = int(data[:MAX_HEADER_SIZE])

        """
        full_msg += data.decode("utf-8")
        if len(full_msg) - MAX_HEADER_SIZE == msglen:
            bestList.append(eval(full_msg[MAX_HEADER_SIZE:]))
            conn.close()
            break
        """
        bestList.append(pickle.loads(data))
        conn.close()
        break

# Find the best solution among them
bestList = sorted(bestList, key=operator.itemgetter(1), reverse=False)

for i, dist in enumerate(bestList):
    print(f"ID: {i},  Distance: {bestList[i][1]}")

# Draw the best solution
img = city_connect(bestList[0][0], MAP_SIZE, bestList[0][2])
cv2.imshow("Final", img)
cv2.waitKey()

print("--- %s seconds ---" % int((time.time() - start_time)))
