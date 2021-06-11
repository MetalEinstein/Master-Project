from GA_Functions import *
import cv2
import matplotlib.pyplot as plt
import time
import wandb

# BEST SCORE SO FAR = 3401 IN 199 GENERATIONS

taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500
# POP_SIZE = 50
# ELITE_SIZE = 5
# MUT_RATE = 0.90
MAX_GENERATIONS = 500
BREAKPOINT = 100
K_AGENTS = 3
# INITIAL_SELECTION_SIZE = 15


project_title = "testing"
title = "proportional_selection_testing"
name = "pst"

# taskList, K_AGENTS = taskGeneratortesting(taskList)

#taskList, K_AGENTS = taskGenerator(taskList, TASK_NUMBER, MAP_SIZE)


def geneticAlgorithm(popSize, eliteSize, mutationRate, generations, breakpoint, numAgents, sel_size, id):
    taskList = list()
    population = taskGeneratortesting(taskList)
    home_city = population.pop(0)
    print(home_city)

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
    bestdist = 0
    for i in range(0, generations):
        gen_time = time.time()
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

        wandb.log({"Current Distance": 1 / rankedFitness[0][1]}, step=i)
        wandb.log({"Time sec": (time.time() - gen_time)}, step=i)
        wandb.log({"Mean": sum_distance / len(rankedFitness)}, step=i)

        # We check the progress over a set number of generations. If progress = 0 we stop the algorithm
        # Might be an alternative just to use breakpoint instead of iteration for a set number of generations
        if bestdist is not (rankedFitness[0][0]):
            bestdist = (rankedFitness[0][0])
            p_counter = 0
        elif p_counter >= BREAKPOINT:
            total_diff = sum(generation_diff)
            generation_diff.clear()
            if total_diff == 0:
                break

    if (1 / rankedFitness[0][1]) < 3200:
        best_indi = rankedFitness[0][0]
        map_city = city_connect(pop, MAP_SIZE, best_indi, home_city, rankedFitness[0][1])
        cv2.imwrite('C:/Users/mikkel/PycharmProjects/Master-Project/pictures/' +
                    name + str("(" + id + ")") + '.png', map_city)

    # best_indi = rankedFitness[0][0]
    # map_city = city_connect(pop, MAP_SIZE, best_indi, home_city)
    #
    # best_indi = pop[best_indi]
    # print("agents: ")
    # for agents in best_indi:
    #     print(agents)
    # print("--- %s seconds ---" % int((time.time() - start_time)))
    # cv2.imshow("Connections", map_city)
    #
    # plt.subplot(2, 1, 1)
    # plt.plot(progress)
    # plt.title('Distance for King and Mean distance for Population over the Generations')
    # plt.ylabel('Distance of King')
    #
    # plt.subplot(2, 1, 2)
    # plt.plot(mean_progress)
    # plt.ylabel('Mean distance of Population')
    # plt.xlabel('Generation')
    #
    # plt.show()
    # cv2.waitKey()

sweep_config = {
    "name": title,
    "method": 'grid',  # 'random',
    "parameters": {
        "POP_SIZE": {"values": [50]},
        "ELITE_SIZE": {"values": [5]},
        "MUT_RATE": {"values": [0.9]},
        "INITIAL_SELECTION_SIZE": {"values": [15]},
        "REPEATS": {"values": [1, 2, 3, 4, 5]},
    }
}

sweep_id = wandb.sweep(sweep_config, project=project_title)


def train():
    id = wandb.util.generate_id()
    run = wandb.init(id=id, name=(name + str('(' + id + ')')))
    # taskList = []
    config = wandb.config
    config.task_number = TASK_NUMBER
    config.map_size = MAP_SIZE
    config.max_generations = MAX_GENERATIONS
    config.breakpoint = BREAKPOINT
    config.k_agents = K_AGENTS
    # config.taskList = taskList
    start_time = time.time()
    # taskList = taskGeneratortesting(taskList)
    geneticAlgorithm(popSize=run.config["POP_SIZE"],
                     eliteSize=run.config["ELITE_SIZE"],
                     mutationRate=run.config["MUT_RATE"],
                     generations=MAX_GENERATIONS,
                     breakpoint=BREAKPOINT,
                     numAgents=K_AGENTS,
                     sel_size=run.config["INITIAL_SELECTION_SIZE"],
                     id=id)
    wandb.log({"Total time (sec)": int((time.time() - start_time))})

wandb.agent(sweep_id, function=train)

# start_time = time.time()
# geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUT_RATE,
#                  generations=MAX_GENERATIONS, breakpoint=BREAKPOINT, numAgents=K_AGENTS, sel_size=INITIAL_SELECTION_SIZE)

