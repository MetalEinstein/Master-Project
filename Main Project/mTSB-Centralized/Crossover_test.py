import random


individual1 = [[(28, 246), (153, 250), (277, 187), (67, 143), (60, 342)],
              [(252, 263), (270, 24), (490, 127), (203, 296), (111, 49)],
              [(433, 195), (391, 466), (187, 164), (490, 30), (316, 394)]]

individual2 = [[(153, 250), (67, 143), (28, 246), (277, 187), (60, 342)],
              [(270, 24), (203, 296), (252, 263), (490, 127), (111, 49)],
              [(391, 466), (490, 30), (433, 195), (187, 164), (316, 394)]]

def parenttrap(individual1, individual2):
    parent1 = []
    parent2 = []
    for i in range(0, len(individual1)):
        parent1.extend(individual1[i])
        parent2.extend(individual2[i])

    return parent1, parent2

def POS(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []
    # ---------------------------------------------#
    #crossover function
    # ---------------------------------------------#
    print(child1)
    print(child2)
    return individual1, individual2

def PMX(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []
    # ---------------------------------------------#
    #crossover function
    # ---------------------------------------------#
    print(child1)
    print(child2)
    return individual1, individual2

def ER(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []
    # ---------------------------------------------#
    #crossover function
    # ---------------------------------------------#
    print(child1)
    print(child2)
    return individual1, individual2

def DPX(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []
    # ---------------------------------------------#
    #crossover function
    # ---------------------------------------------#
    print(child1)
    print(child2)
    return individual1, individual2

def TCX(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []
    # ---------------------------------------------#
    #crossover function
    # ---------------------------------------------#
    print(child1)
    print(child2)
    return individual1, individual2

def OX1(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []

# ---------------------------------------------#
    start_index = random.randint(0, len(parent1) - 2)
    end_index = random.randint(start_index+1, len(parent1) - 1)
    print(start_index, end_index)

    child1 = parent1[start_index:end_index + 1]
    child2 = parent2[start_index:end_index + 1]

    childtemp1 = [task for task in parent2 if task not in child1]
    childtemp2 = [task for task in parent1 if task not in child2]

    child1.extend(childtemp1)
    child2.extend(childtemp2)
# ---------------------------------------------#

    # newagent = []
    # for j in range(0, len(individual1)):
    #     # newindividual1.append(child1[h])
    #     # newindividual1.extend(tuple(child1[0:len(individual1[j])]))
    #      # individual1[j].pop(child1.index(child1[0:len(individual1[j])]))
    #
    #     for h in range(0, len(individual1[j])-1):
    #         # if len(child1) <= 2:
    #         #     individual1[j] = child1[0:2]
    #         # else:
    #         newagent[j].append(child1[h])
    #
    #         print(j, h, child1, newagent)
    #
    #     individual1[j]=newagent
    #     print(individual1)


        # individual1[0] = child1[0:len(individual1[0])]
    # individual1[1] = child1[len(individual1[0]):len(individual1[1])+len(individual1[1])]
    # individual1[0] = [child1.pop(0) for idx in range(0:len(individual1[0]))]

    # individual1[j] = child1.pop(range(0, len(individual1[j])))
    print(child1)
    print(child2)
    return individual1, individual2



# TCX(individual1, individual2)
OX1(individual1, individual2)
# PMX(individual1, individual2)
# DPX(individual1, individual2)
# ER(individual1, individual2)
# POS(individual1, individual2)


