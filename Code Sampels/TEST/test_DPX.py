import time
indi1 = [[1, 2, 3, 8, 5], [6, 7, 9, 11]]
indi2 = [[1, 2, 3, 11, 8], [7, 6, 5, 9]]

start_time = time.time()
indi2_comparable = []
for sublist in indi2:
    indi2_comparable.extend(sublist) or indi2_comparable.append(0)

fragments = []
for genome in indi1:
    init_loop = True
    temp = []
    next_index = 0
    pre_index = 0

    for gene in genome:
        next_index = indi2_comparable.index(gene)

        if init_loop:
            temp.append(gene)
            pre_index = next_index
            init_loop = False
            continue

        if next_index == pre_index+1:
            temp.append(gene)
            pre_index = next_index
            continue

        elif next_index == pre_index-1:
            temp.insert(0, gene)
            pre_index = next_index
            continue

        else:
            fragments.append(temp)
            temp = [gene]
            pre_index = next_index

            if genome.index(gene) == len(genome)-1:
                fragments.append(temp)

# TODO create the child by reordering the fragments according to the heuristic

print(fragments)
print(time.time() - start_time)