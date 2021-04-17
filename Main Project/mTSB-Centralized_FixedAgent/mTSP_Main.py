from GA_Functions import *
import cv2
import matplotlib.pyplot as plt
import time
import matplotlib
import numpy as np
import wandb

# taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500
POP_SIZE = 50  # skiftes
# ELITE_SIZE = 5 #skiftes
# MUT_RATE = 0.20 # skiftes
MAX_GENERATIONS = 500
BREAKPOINT = 100
K_AGENTS = 3


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, breakpoint, numAgents, id):
    pop = 0
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

    p_counter = 0
    breakcounter = 0
    bestdist = 0
    for i in range(0, generations):
        gen_time = time.time()
        sum_distance = 0
        p_counter += 1
        breakcounter += 1

        progress_past = 1 / rankRoutes(pop, home_city)[0][1]
        rankedFitness = rankRoutes(pop, home_city)
        postMu, postSel, pop = evolvePopulation(pop, rankedFitness, eliteSize, mutationRate, i)
        progress_future = 1 / rankRoutes(pop, home_city)[0][1]
        generation_diff.append(abs(progress_past - progress_future))

        progress.append(1 / rankedFitness[0][1])
        # print("Current Distance: " + str(1 / rankedFitness[0][1]) + ",   ", "Generation: " + str(i))
        wandb.log({"Current Distance": 1 / rankedFitness[0][1]}, step=i)
        wandb.log({"Best Distance": 1 / rankedFitness[0][0]}, step=i)
        wandb.log({"Time sec": (time.time() - gen_time)}, step=i)

        for f in range(len(rankedFitness)):
            sum_distance += 1 / rankedFitness[f][1]
        mean_progress.append(sum_distance / len(rankedFitness))

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
        if bestdist is not (rankedFitness[0][0]):
            bestdist = (rankedFitness[0][0])
            # print('dist', rankedFitness[0][1])
            breakcounter = 0
        elif breakcounter >= BREAKPOINT:
            # if p_counter == breakpoint:
            #     print('breakc: ', breakcounter)
            p_counter = 0
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

    best_indi = rankedFitness[0][0]
    map_city = city_connect(pop, MAP_SIZE, best_indi, home_city)

    # best_indi = pop[best_indi]
    # print("agents: ")
    # for agents in best_indi:
    #     print(agents)
    # print("--- %s seconds ---" % int((time.time() - start_time)))
    # cv2.imshow("Connections", map_city)
    if best_indi < 3500:
        cv2.imwrite('C:/Users/Alexander Staal/Desktop/Robotics/Kandidat (msc in robotics)/10. '
                    'semester/Master-Project/Main Project/mTSB-Centralized_FixedAgent/Map_connections/Map_connection' +
                    str("(" + id + ")") + '.png', map_city)

    # plt.subplot(2, 1, 1)
    # plt.plot(progress)
    # plt.title('Distance for King and Mean distance for Population over the Generations')
    # plt.ylabel('Distance of King')
    #
    # plt.subplot(2, 1, 2)
    # plt.plot(mean_progress)
    # plt.ylabel('Mean distance of Population')
    # plt.xlabel('Generation')

    # plt.savefig('test.png', bbox_inches='tight')
    # plt.show()
    # cv2.waitKey()


#
#
# for i in range(10):
#     start_time = time.time()
#     taskList = taskGeneratortesting(taskList)
#     geneticAlgorithm(population=taskList, popSize=POP_SIZE, eliteSize=ELITE_SIZE, mutationRate=MUT_RATE,
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
    "name": "tcx_test",
    "method": 'grid',  # 'random',
    "parameters": {
        # "POP_SIZE": {"values": [50]},
        "ELITE_SIZE": {"values": [5, 10, 15]},
        "MUT_RATE": {"values": [0.1, 0.2, 0.3, 0.4, 0.5]},
        "LOOP_SIZE": {"values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
    }
}

sweep_id = wandb.sweep(sweep_config, project="crossover")


def train():
    # for x in range(10):
    # run = wandb.init(reinit=True)
    id = wandb.util.generate_id()
    run = wandb.init(id=id, name=("tcx" + str('(' + id + ')')))
    taskList = []
    config = wandb.config
    config.task_number = TASK_NUMBER
    config.map_size = MAP_SIZE
    config.max_generations = MAX_GENERATIONS
    config.breakpoint = BREAKPOINT
    config.k_agents = K_AGENTS
    config.pop_size = POP_SIZE
    start_time = time.time()
    taskList = taskGeneratortesting(taskList)
    geneticAlgorithm(population=taskList,
                     popSize=POP_SIZE,
                     eliteSize=run.config["ELITE_SIZE"],
                     mutationRate=run.config["MUT_RATE"],
                     generations=MAX_GENERATIONS,
                     breakpoint=BREAKPOINT,
                     numAgents=K_AGENTS,
                     id=id)
    wandb.log({"Total time (sec)": int((time.time() - start_time))})

    # run.finish()


wandb.agent(sweep_id, function=train)
