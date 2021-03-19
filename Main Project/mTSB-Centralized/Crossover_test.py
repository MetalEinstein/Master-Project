import random

individual1 = [[(28, 246), (153, 250), (277, 187), (67, 143), (60, 342)],
               [(252, 263), (270, 24), (490, 127), (203, 296), (111, 49)],
               [(433, 195), (391, 466), (187, 164), (490, 30), (316, 394)]]

individual2 = [[(270, 24), (203, 296), (252, 263), (490, 127), (111, 49)],
               [(153, 250), (67, 143), (28, 246), (277, 187), (60, 342)],
               [(391, 466), (490, 30), (433, 195), (187, 164), (316, 394)]]


def parenttrap(individual1, individual2):
    parent1 = []
    parent2 = []
    for i in range(0, len(individual1)):
        parent1.extend(individual1[i])
        parent2.extend(individual2[i])

    return parent1, parent2

def childabuse(child, individual1):
    matrix = []
    h = 0

    for i in range(len(individual1)):
        matrix.append([])
        for j in range(len(individual1[i])):
            matrix[i].append(child[h])
            h += 1
    return matrix

def POS(individual1, individual2):
    # parent1, parent2 = parenttrap(individual1, individual2)
    parent1 = [  (6,6),  (2,2),  (3,3),  (4,4),  (5,5),  (8,8),(7,7),(1,1),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15)]
    parent2 = [(15,15),(14,14),(13,13),(12,12),(11,11),(10,10),(9,9),(8,8),(7,7),  (6,6),  (5,5),  (4,4),  (3,3),  (2,2),  (1,1)]

    index_list = []
    # ---------------------------------------------#
    # k = random.randint(2, len(parent1))         # number of samples to be chosen
    k = 3
    child1 = [0] * (len(parent1)-k)
    child2 = [0] * (len(parent2)-k)
    sequence1 = random.sample(parent1, k)             # random positions
    sequence2 = []
    print(sequence1)

    for i in range(0, len(sequence1)):
        sequence2.append(parent2[parent1.index(sequence1[i])])
        child2.insert(parent1.index(sequence1[i]), sequence1[i])
        child1.insert(parent1.index(sequence1[i]), sequence2[i])
        index_list.append(parent1.index(sequence1[i]))

    print(index_list)
    print(sequence2)
    print(child1, len(child1))
    print(child2, len(child2))

    for i in range(0, len(child2)):
        if parent2[i] in sequence1:
            k = sequence1.index(parent2[i])
            child2[i] = sequence2[k]
            print('inserts', sequence2[k], '->', i)
        elif parent2[i] not in child2:
            child2[i] = parent2[i]


    # for i in range(0, len(child1)):
    #     if (i < start_index or i > end_index - 1) and child2[i] in sequence2:
    #         k = sequence2.index(child1[i])
    #         child1[i] = sequence1[k]

    for k in range(0, len(sequence2)):
        indices = [i for i, x in enumerate(child2) if x == sequence1[k]]
    print('indices1', indices)
    # ---------------------------------------------#
    # print(child1)
    print(child2, len(child2))
    print(parent2)

    # print(childabuse(child1, individual1))
    # print(childabuse(child2, individual2))
    return individual1, individual2


def PMX(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    # parent1 = [6,2,3,4,5,8,7,1,9,10,11,12,13,14,15]
    # parent2 = [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
    sequence1 = []
    sequence2 = []
    child1 = []
    child2 = []
    # ---------------------------------------------#
    start_index = random.randint(0, len(parent2) - 3)
    end_index = random.randint(start_index+2, len(parent2))

    # leftovers = end_index - start_index
    # print(start_index, ':', end_index, '=', leftovers)
    sequence1.extend(parent1[start_index:end_index])
    sequence2.extend(parent2[start_index:end_index])

    j = 0
    child1.extend(parent1)
    child2.extend(parent2)
    for i in range(0, len(child1)):
        if i >= start_index and i <= end_index-1:
            child1[i] = sequence2[j]
            child2[i] = sequence1[j]
            # print(i, child1, 'indsætter sequence', j, '->', sequence2[j])
            j += 1
        else:
            if child1[i] in sequence2:
                k = sequence2.index(child1[i])
                child1[i] = sequence1[k]
                # print(i, child1, 'bytter', sequence2[k], '->', sequence1[k])
            elif child2[i] in sequence1:
                k = sequence1.index(child2[i])
                child2[i] = sequence2[k]
                # print(i, child1, 'bytter', sequence1[k], '->', sequence2[k])

    # ---------double checks for doubles-----------#
        for i in range(0, len(child1)):
            if (i < start_index or i > end_index-1) and child1[i] in sequence2:
                k = sequence2.index(child1[i])
                child1[i] = sequence1[k]
                # print(i, child1, 'bytter anden gang', sequence2[k], '->', sequence1[k])
            elif (i < start_index or i > end_index - 1) and child2[i] in sequence1:
                k = sequence1.index(child2[i])
                child2[i] = sequence2[k]

    # ---------only to proof of no doubles---------#
    # for k in range(0, len(sequence2)):
    #     indices = [i for i, x in enumerate(child1) if x == sequence2[k]]
    #     print('indices1', indices)
    # for k in range(0, len(sequence1)):
    #     indices = [i for i, x in enumerate(child2) if x == sequence1[k]]
    #     print('indices2', indices)

    # ---------------------------------------------#
    # print('s1 ', sequence1)
    # print('s2 ', sequence2)
    # print('c1 ', child1)
    # print('c2 ', child2)
    # print('p1 ', parent1)
    # print('p2 ', parent2)
    print(childabuse(child1, individual1))
    print(childabuse(child2, individual2))
    return individual1, individual2


def DPX(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []
    # ---------------------------------------------#
    # crossover function
    # ---------------------------------------------#
    print(child1)
    print(child2)
    return individual1, individual2


def TCX(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    sequence_index1 = []
    equence_index2 = []
    child1 = []
    listy = [5, 5, 5, 1, 4, ]
    # ---------------------------------------------#
    for i in range(0, len(individual1)):
        start_index = random.randint(0, len(individual1[i]) - 2)
        end_index = random.randint(start_index, len(individual1[i])-1)
        if start_index == end_index:
            end_index += 1
        leftovers = len(individual1[i]) - (end_index - start_index)
        sequence_index1.append(end_index - start_index)
        print(start_index, ':', end_index, '=', leftovers)

        child1.extend(individual1[i][start_index:end_index])
    # print(childabuse(parent1, individual1))
    print(sequence_index1)
    print(individual1)

    # crossover function
    # ---------------------------------------------#
    print(child1)
    return individual1, individual2


def OX1(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []

    # ---------------------------------------------#
    start_index = random.randint(0, len(parent1) - 2)
    end_index = random.randint(start_index + 1, len(parent1) - 1)
    print(start_index, end_index)

    child1 = parent1[start_index:end_index + 1]
    child2 = parent2[start_index:end_index + 1]

    childtemp1 = [task for task in parent2 if task not in child1]
    childtemp2 = [task for task in parent1 if task not in child2]

    child1.extend(childtemp1)
    child2.extend(childtemp2)
    # ---------------------------------------------#

    print(parent1)
    print(parent2)
    print(child1)
    print(child2)
    return individual1, individual2


# TCX(individual1, individual2)
# OX1(individual1, individual2) # done
# PMX(individual1, individual2) # done
# DPX(individual1, individual2)
POS(individual1, individual2)
