import random

# individual = [[(28, 246), (153, 250), (277, 187), (67, 143), (60, 342)],
#               [(252, 263), (270, 24), (490, 127), (203, 296), (111, 49)],
#               [(433, 195), (391, 466), (187, 164), (490, 30), (316, 394)]]
#individual = [[(41, 461), (220, 215), (27, 149), (115, 32), (462, 293)],
              # [(171, 217), (385, 64)],
              # [(100, 141), (194, 84), (305, 333)],
              # [(112, 307), (68, 366), (389, 296), (346, 303)]]

# individual = [[(418,278), (415,335), (417,216), (468,211), (360,355), (469,190), (325,394), (381,127), (496,429), (247,224), (218,247), (321,92)],
#               [(222,360), (450,15), (381,1), (109,229), (108,211), (116,115), (114,472), (60,166), (144,10), (12,270), (14,110), (46,14)], [(112, 307), (68, 366), (389, 296), (346, 303)]]

# individual2 = [[(41, 461), (220, 215), (27, 149), (115, 32), (462, 293)],
#               [(171, 217), (385, 64)],
#               [(100, 141), (194, 84), (305, 333)]]

def random_chromosome_contraction(individual):
    # picks two random genomes
    genome1, genome2 = random.sample(individual, 2)
    # deletes the first genome from individual
    individual.pop(individual.index(genome1))
    # inserts the genes from list1 into list2
    genome2.extend(genome1)

    return individual

def chromosome_partition_max(individual):
    listy = []
    for i in range(0, len(individual)):
        listy.append(len(individual[i]))

    k = listy.index(max(listy))
    m_genome = individual.pop(k)

    partition_index = random.randint(1, len(m_genome) - 1)

    # Split the chosen genome in two
    new_genome1 = m_genome[0:partition_index]
    new_genome2 = m_genome[partition_index:len(m_genome)]

    individual.append(new_genome1)
    individual.append(new_genome2)

    return individual

def partition_insertion(individual):
    genome1, genome2 = random.sample(individual, 2)

    if len(genome1) > 1:
        print("Part Inserting ------------------------------")
        start_index = random.randint(0, len(genome1) - 1)

        gene = genome1[start_index]

        genome1.pop(start_index)
        genome2.insert(0, gene)

    return individual

def swap(individual):
    genome1, genome2 = random.sample(individual, 2)

    start_index = random.randint(0, len(genome1) - 1)
    end_index = random.randint(0, len(genome2) - 1)

    newgenome2 = genome2[end_index]

    genome2[end_index] = genome1[start_index]
    genome1[start_index] = newgenome2

    return individual

def chromosome_contraction(individual):
    if len(individual) > 2:
        print("Contraction individual ----------------------")
        agent = [agent for agent in individual]
        s_agent = []
        # creates a list of the different lengths in individual
        for i in range(0, len(individual)):
            s_agent.append(len(agent[i]))
        # sorts the list to find the smallest and then remember the two firsts index
        sort_list = sorted(s_agent)
        first_agent = s_agent.index(sort_list[0])
        second_agent = s_agent.index(sort_list[1])
        if first_agent == second_agent:
            second_agent += 1
        # unpacks each list
        genes = [genes for genes in agent[first_agent]]
        genes2 = [genes2 for genes2 in agent[second_agent]]
        # inserts each gene one by one from back of the first list to the start of the second list
        genes2.extend(genes)
        # for j in range(s_agent[first_agent]-1, -1, -1):
        #     genes2.insert(0, genes[j])
        # The main list is then updated and the smallest agent is deleted

        individual[second_agent] = genes2
        individual.pop(individual.index(agent[first_agent]))

    return individual


def chromosome_partition(individual):
    print("\nPrevious Individual: ", individual)

    # Select a genome from the individual at random and insure that the genome has at least two genes
    k = random.randint(0, len(individual) - 1)
    while len(individual[k]) <= 1:
        k = random.randint(0, len(individual) - 1)
    print("Selected Genome: ", individual[k])

    # Take the genome out of the individual
    genome = individual.pop(k)

    # Randomly choose a breakpoint for splitting the genome in two
    partition_index = random.randint(1, len(genome) - 1)
    print("Partition Index: ", partition_index)

    # Split the chosen genome in two
    new_genome1 = genome[0:partition_index]
    new_genome2 = genome[partition_index:len(genome)]
    print("\nNew Genomes:")
    print(f"Genome 1: {new_genome1}")
    print(f"Genome 2: {new_genome2}")

    # Reinsert the genomes back into the individual
    individual.append(new_genome1)
    individual.append(new_genome2)
    print("\nNew Individual: ", individual)

    return individual


def sequence_inversion(individual):
    # print("\nPrevious Individual: ", individual)

    # Select a genome from the individual at random
    k = random.randint(0, len(individual) - 1)
    genome = individual[k]
    # print("Selected Genome: ", individual[k])

    if len(genome) > 1:
        # Randomly choose a start and end index to specify the gene sequence to be inverted
        start_index = random.randint(0, len(genome) - 2)
        end_index = random.randint(start_index, len(genome) - 1)
        # print(f"Selected Sequence: {start_index} -> {end_index + 1}")

        # Insure that at least two genes are always being inverted
        if start_index == end_index:
            end_index += 1

        # Take out the selected sequence and invert it
        subset = genome[start_index:end_index + 1]
        # print("\nGene subset: ", subset)
        subset.reverse()
        # print("Reversed Gene subset: ", subset)

        # Reinsert the inverted gene sequence into the original genome and insert into the individual
        genome[start_index:end_index + 1] = subset
        individual[k] = genome
        # print("New Individual: ", individual)

    return individual


def insertion(individual):
    #  k saves the random index number for later use
    k = random.randint(0, len(individual) - 1)
    #  Splits a random agent into genes and chooses randomly one
    agent = [gene for gene in individual[k]]
    if len(agent) > 1:
        gene = agent[random.randint(0, len(agent) - 1)]
        #  The gene is then removed from the list
        agent.pop(agent.index(gene))
        #  insert(index, elem) places the gene randomly in the agent and push everything to the right
        agent.insert(random.randint(0, len(agent) - 1), gene)
        #  Inserts the new agent the same place it was taken from
        individual[k] = agent

    return individual


def transposition(individual):
    #  k saves the random index number for later use
    k = random.randint(0, len(individual) - 1)
    while len(individual[k]) <= 1:
        k = random.randint(0, len(individual) - 1)
    #  Splits a random agent into genes and chooses randomly two
    genes = [gene for gene in individual[k]]
    gene1, gene2 = random.sample(genes, 2)
    #  Takes the index positions, to only swap the chosen genes
    a, b = genes.index(gene1), genes.index(gene2)
    genes[b], genes[a] = genes[a], genes[b]
    #  Inserts the new agent the same place it was taken from
    individual[k] = genes

    return individual



# print(individual)
# print(insertion(individual))
# print(transposition(individual))
# print(sequence_inversion(individual))
# print(chromosome_contraction(individual))
# print(random_chromosome_contraction(individual))
# print(chromosome_partition_max(individual))
# print(partition_insertion(individual))
# print(swap(individual))
# print(chromosome_partition(individual2))

