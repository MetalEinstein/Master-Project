from GA_Functions import *
import cv2
# import matplotlib.pyplot as plt
import time
# import matplotlib
# import numpy as np
import wandb

# taskList = []
TASK_NUMBER = 35
MAP_SIZE = 500
# POP_SIZE = 50  # skiftes
# ELITE_SIZE = 5 #skiftes
# MUT_RATE = 0.20 # skiftes
MAX_GENERATIONS = 500
BREAKPOINT = 100
K_AGENTS = 3
# INITIAL_SELECTION_SIZE = 15

project_title = "testing"
title = "population_deviation_test"
name = "popdev"


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, breakpoint, numAgents, sel_size, id):
    # pop = 0
    home_city = population.pop(0)
    pop = initialPopulation(popSize, population, numAgents)
    generation_diff = []
    progress = []
    mean_progress = []

    temp_rank = rankRoutes(pop, home_city)
    progress.append(1 / temp_rank[0][1])  # We track progress according to the best route

    sum_distance = 0
    for i in range(len(temp_rank)):
        sum_distance += 1 / temp_rank[i][1]
    mean_progress.append(sum_distance / len(temp_rank))

    breakcounter = 0
    bestdist = 0
    for i in range(0, generations):
        gen_time = time.time()
        sum_distance = 0
        breakcounter += 1

        progress_past = 1 / rankRoutes(pop, home_city)[0][1]
        rankedFitness = rankRoutes(pop, home_city)
        pop = evolvePopulation(pop, rankedFitness, eliteSize, mutationRate, sel_size, generations)
        progress_future = 1 / rankRoutes(pop, home_city)[0][1]
        generation_diff.append(abs(progress_past - progress_future))

        progress.append(1 / rankedFitness[0][1])
        # print("Current Distance: " + str(1 / rankedFitness[0][1]) + ",   ", "Generation: " + str(i))

        for f in range(len(rankedFitness)):
            sum_distance += 1 / rankedFitness[f][1]
        mean_progress.append(sum_distance / len(rankedFitness))

        wandb.log({"Current Distance": 1 / rankedFitness[0][1]}, step=i)
        wandb.log({"Time sec": (time.time() - gen_time)}, step=i)
        wandb.log({"Mean": sum_distance / len(rankedFitness)}, step=i)
        # We check the progress over a set number of generations. If progress = 0 we stop the algorithm
        # Might be an alternative just to use breakpoint instead of iteration for a set number of generations
        if bestdist is not (rankedFitness[0][0]):
            bestdist = (rankedFitness[0][0])
            breakcounter = 0
        elif breakcounter >= BREAKPOINT:
            total_diff = sum(generation_diff)
            generation_diff.clear()

            if total_diff == 0:
                break
    # print('---------------------')
    # print("\tCurrent Distance: " + str(1 / rankedFitness[0][1]) + "\tTime sec: ",
    #       + int((time.time() - start_time)), "Generation: " + str(i))
    # print('---------------------')

    # file = open("testfile.txt", "a")
    # D = ['\tCurrent Distance: ', str(1 / rankedFitness[0][1]), '\tTime sec: ', str(int((time.time() - start_time))), '\tGeneration: ', str(i), '\n']
    # file.writelines(D)
    # file.close()
    
    if (1 / rankedFitness[0][1]) < 3600:
        best_indi = rankedFitness[0][0]
        map_city = city_connect(pop, MAP_SIZE, best_indi, home_city, rankedFitness[0][1])
        cv2.imwrite('/Users/Ditte/Desktop/Pictures' +
                    name + str("(" + id + ")") + '.png', map_city)
#
# for i in range(10):
#     start_time = time.time()
# taskList = taskGeneratortesting(taskList)
# geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUT_RATE,
#                      generations=MAX_GENERATIONS, breakpoint=BREAKPOINT, numAgents=K_AGENTS)

# for i in range(4):
#     file = open("testfile.txt", "a")
#
#     POP_SIZE = [50, 100, 150, 200]  # skiftes
#     ELITE_SIZE = [5, 10, 15, 20]  # skiftes
#     MUT_RATE = [0.3, 0.4, 0.5]  # skiftes
#
#     for k in range(4):
#         for l in range(3):
#             print('Test: ', i, 'Parameters: ', POP_SIZE[i], ELITE_SIZE[k], MUT_RATE[l])
#
#             # L = ['Test: ', str(i), '\tParameters: ', str(POP_SIZE[i]), '\t', str(ELITE_SIZE[k]), '\t', str(MUT_RATE[l]), '\n']
#             # file.writelines(L)
#             # file.close()
#
#             for j in range(10):
#                 config = wandb.config
#                 config.pop_size = POP_SIZE[i]
#                 config.elite_size = ELITE_SIZE[k]
#                 config.mut_rate = MUT_RATE[l]
#                 config.task_number = TASK_NUMBER
#                 config.map_size = MAP_SIZE
#                 config.max_generations = MAX_GENERATIONS
#                 config.breakpoint = BREAKPOINT
#                 config.k_agents = K_AGENTS
#
#                 start_time = time.time()
#                 geneticAlgorithm(population=taskList, popSize=POP_SIZE[i], eliteSize=ELITE_SIZE[k], mutationRate=MUT_RATE[l], generations=MAX_GENERATIONS, breakpoint=BREAKPOINT, numAgents=K_AGENTS)


sweep_config = {
    "name": title,
    "method": 'grid',  # 'random',
    "parameters": {
        "POP_SIZE": {"values": [250, 500, 750, 1000]},
        "ELITE_SIZE": {"values": [15]},
        "MUT_RATE": {"values": [0.9]},
        "INITIAL_SELECTION_SIZE": {"values": [50, 100, 150, 200]},
        "REPEATS": {"values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
    }
}

sweep_id = wandb.sweep(sweep_config, project=project_title)


def train():
    id = wandb.util.generate_id()
    run = wandb.init(id=id, name=(name + str('(' + id + ')')))
    taskList = []
    config = wandb.config
    config.task_number = TASK_NUMBER
    config.map_size = MAP_SIZE
    config.max_generations = MAX_GENERATIONS
    config.breakpoint = BREAKPOINT
    config.k_agents = K_AGENTS
    start_time = time.time()
    taskList = taskGeneratortesting(taskList)
    geneticAlgorithm(population=taskList,
                     popSize=run.config["POP_SIZE"],
                     eliteSize=run.config["ELITE_SIZE"],
                     mutationRate=run.config["MUT_RATE"],
                     generations=MAX_GENERATIONS,
                     breakpoint=BREAKPOINT,
                     numAgents=K_AGENTS,
                     sel_size=run.config["INITIAL_SELECTION_SIZE"],
                     id=id)
    wandb.log({"Total time (sec)": int((time.time() - start_time))})

wandb.agent(sweep_id, function=train)
