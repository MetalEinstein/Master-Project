import random
import numpy as np
import copy
# individual1 = [[(28, 246, 153, 250), (277, 187, 67, 143), (60, 342, 252, 263)],
#                [(270, 24, 490, 127), (203, 296, 111, 49)],
#                [(433, 195, 391, 466), (187, 164, 490, 30), (316, 394, 60, 67)]]
#
# individual2 = [[(270, 24, 490, 127), (203, 296, 111, 49)],
#                [(28, 246, 153, 250), (277, 187, 67, 143), (60, 342, 252, 263)],
#                [(187, 164, 490, 30), (433, 195, 391, 466), (316, 394, 60, 67)]]
t1 = []

t2 = []

Task_number = 5
agents = 3
def city_connection(Task_number, agents):
    t1 = []
    t2 = []
    for h in range(agents):
        t1.append([])
        for i in range(Task_number):
            t1[h].append([])
            for j in range(0, 4):
                t1[h][i].append(random.randint(0, 500))
            t1[h][i] = tuple(t1[h][i])

    t2 = copy.deepcopy(t1)
    random.shuffle(t2)
    for i in range(agents):
        random.shuffle(t2[i])
    return t1, t2

def city_matrix(num): # makes the city connections with distances
    for i in range(0, num):
        a = []
        for j in range(0, num):
                x = cityList[i].x - cityList[j].x
                y = cityList[i].y - cityList[j].y
                distance = np.sqrt((x ** 2) + (y ** 2))
                a.append(int(distance))

        matrixmap.append(a)
    print(np.matrix(matrixmap))

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
    parent1, parent2 = parenttrap(individual1, individual2)

    # k = 3
    k = random.randint(2, len(parent1))         # number of samples to be chosen
    print('shift points', k)
    child1 = [0] * (len(parent1))
    child2 = [0] * (len(parent2))
    sequence1 = random.sample(parent1, k)             # random positions
    sequence2 = []

    for i in range(k):
        sequence2.append(parent2[parent1.index(sequence1[i])])
        child1[parent1.index(sequence1[i])] = sequence2[i]
        child2[parent1.index(sequence1[i])] = sequence1[i]

    for i in range(len(child2)):
        if parent2[i] in sequence1:
            k = sequence1.index(parent2[i])
            child2[i] = sequence2[k]
            # print('uses', sequence2[k], 'on', i, 'instead of', sequence1[k], 'in c2')
        if parent1[i] in sequence2:
            k = sequence2.index(parent1[i])
            child1[i] = sequence1[k]
            # print('uses', sequence1[k], 'on', i, 'instead of', sequence2[k], 'in c1')

    for i in range(len(child2)):
        if parent2[i] not in child2:
            child2[i] = parent2[i]
        if parent1[i] not in child1:
            child1[i] = parent1[i]

    # print(childabuse(child1, individual1))
    # print(childabuse(child2, individual2))
    return childabuse(child1, individual1), childabuse(child2, individual2)


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

    # print(childabuse(child1, individual1))
    # print(childabuse(child2, individual2))
    return childabuse(child1, individual1), childabuse(child2, individual2)





def OX1(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []

    # ---------------------------------------------#
    start_index = random.randint(0, len(parent1) - 2)
    end_index = random.randint(start_index + 1, len(parent1) - 1)
    # print(start_index, end_index)

    child1 = parent1[start_index:end_index + 1]
    child2 = parent2[start_index:end_index + 1]

    childtemp1 = [task for task in parent2 if task not in child1]
    childtemp2 = [task for task in parent1 if task not in child2]

    child1.extend(childtemp1)
    child2.extend(childtemp2)
    # ---------------------------------------------#

    # print(parent1)
    # print(parent2)
    # print(childabuse(child1, individual1))
    # print(child2)
    return childabuse(child1, individual1), childabuse(child2, individual2)

def distance(x1,y1,x2,y2):
    xDis = abs(x1 - x2)
    yDis = abs(y1 - y2)
    distance = np.sqrt((xDis ** 2) + (yDis ** 2))

    return distance

def DPX(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)
    child1 = []
    child2 = []
    # ---------------------------------------------#
    for i in range(0, len(individual1)):
        for j in range(0, len(individual1[i])):
            dist = distance(individual1[i][j][0], individual1[i][j][1], individual2[i][j][2], individual2[i][j][3])
            print(dist)
    test1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    test2 = [2, 1, 9, 4, 6, 7, 8, 3, 5]

    for i in range(0, len(test1)):
        temp = []
        if test1[i] == test2[i]:
            for j in range(0, len(test1)):
                if test1[j+1] == test2[j+1]:
                    temp.append(test1[j])

    # ---------------------------------------------#
    print(individual1[0])
    print(distance)
    return individual1, individual2

def TCX(individual1, individual2):
    parent1, parent2 = parenttrap(individual1, individual2)

    sequence_index = []
    sequence = []
    rev_seq = []
    child1 = []
    lefty = []

    # ---------------------------------------------#
    for i in range(0, len(individual1)):
        start_index = random.randint(0, len(individual1) - 2)
        end_index = random.randint(start_index, len(individual1[i])-1)
        if start_index == end_index:
            end_index += 1
        # leftovers = len(individual1[i]) - (end_index - start_index)
        sequence_index.append(end_index - start_index)
        # print(start_index, ':', end_index, '=', leftovers)

        child1.extend(individual1[i][start_index:end_index])
        lefty.extend(individual1[i][0:start_index])
        lefty.extend(individual1[i][end_index:len(individual1[i])])
        child1.extend([0])

        sequence.extend(individual1[i][start_index:end_index])

    # print(sequence_index1)
    # print('P1', sequence_index1, parent1)
    # print('sq', sequence)
    # print('c1', child1, len(child1))
    #
    # print('Leftovers \t\t\t', lefty)

    indexList = []
    for i in range(len(parent1)):
        if parent2[i] in lefty:
            rev_seq.append(parent2[i])
            indexList.append(i)

    # print('P2 order Leftovers \t', rev_seq)
    split = np.array_split(indexList, len(individual1))

    counter = []
    sum = []
    for array in split:
        listy = []
        for i in range(len(child1)):
            if child1[i] == 0:
                counter.append(len(list(array)))
                listy = (list(array))
                child1.pop(i)
                for j in range(len(listy)):
                    child1.insert(i+j, parent2[listy[j]])
                break

    for i in range(len(sequence_index)):
        sum.append([0]*(counter[i] + sequence_index[i]))
        counter[i] = counter[i] + sequence_index[i]
    print(counter, childabuse(child1, sum))

    return childabuse(child1, sum)

t1, t2 = city_connection(Task_number, agents)

TCX(t1, t2)  # done
# DPX(t1, t2)
# PMX(t1, t2)  # done
# POS(t1, t2)  # done
# OX1(t1, t2)  # done
