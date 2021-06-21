from GA_Functions import *
import socket
import time
import pickle

taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500
POP_SIZE = 50
ELITE_SIZE = 15
MUT_RATE = 0.9
MAX_GENERATIONS = 500
BREAKPOINT = 100
INITIAL_SELECTION_SIZE = 5

# Socket setup
MAX_HEADER_SIZE = 10

soc = socket.socket()
host = socket.gethostname()  # Server IP
port = 9999  # Should be the same port number as Server

while True:
    try:
        soc.connect((host, port))
        print("Connection Established")
        break

    except:
        print("Waiting for connection...")
        time.sleep(1)


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


while True:
    data = soc.recv(1024)

    # If the server is just pinging client to check connection send back short response
    check = data.decode("utf-8")
    if check == "0":
        soc.send(str.encode("1"))
        break


taskList, K_AGENTS = taskGeneratortesting(taskList)
K_AGENTS = 3

best_individual = geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUT_RATE,
                 generations=MAX_GENERATIONS, breakpoint=BREAKPOINT, numAgents=K_AGENTS, sel_size=INITIAL_SELECTION_SIZE)

# Send the best individual to the server
# TODO Add message size to data for comparison on the server side
#data = str(best_individual)
#data = f'{len(data):<{MAX_HEADER_SIZE}}' + data
#soc.send(str.encode(data))
data = pickle.dumps(best_individual)
soc.send(data)



