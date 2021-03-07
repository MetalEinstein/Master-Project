import random

# individual = [[(28, 246), (153, 250), (277, 187), (67, 143), (60, 342)],
#               [(252, 263), (270, 24), (490, 127), (203, 296), (111, 49)],
#               [(433, 195), (391, 466), (187, 164), (490, 30), (316, 394)]]
individual = [[(41, 461), (220, 215), (27, 149), (115, 32), (462, 293)],
              [(171, 217), (385, 64)],
              [(100, 141), (194, 84), (305, 333)],
              [(112, 307), (68, 366), (389, 296), (346, 303)]]


# individual = [[1, 2, 3, 4, 5, 6, 7], [8, 9], [10, 11, 12, 13, 14, 15]]

def chromosome_contraction(individual):
    agent = [agent for agent in individual]
    s_agent = []
    # creates a list of the different lengths in individual
    for i in range(0, len(individual)):
        s_agent.append(len(agent[i]))
    # sorts the list to find the smallest and then remember the two firsts index
    sort_list = sorted(s_agent)
    first_agent = s_agent.index(sort_list[0])
    second_agent = s_agent.index(sort_list[1])
    # print(s_agent)
    # unpacks each list
    genes = [genes for genes in agent[first_agent]]
    genes2 = [genes2 for genes2 in agent[second_agent]]
    # inserts each gene one by one from back of the first list to the start of the second list
    for j in range(s_agent[first_agent]-1, -1, -1):
        genes2.insert(0, genes[j])
    # The main list is then updated and the smallest agent is deleted
    individual[second_agent] = genes2
    individual.pop(individual.index(agent[first_agent]))

    return individual


def sequence_inversion2(individual):
    #  k saves the random index number for later use
    k = random.randint(0, len(individual) - 1)
    #  Splits a random agent into genes and chooses randomly two
    agent = [gene for gene in individual[k]]
    #  finds two random index points
    start_index = random.randint(0, len(agent) - 2)
    end_index = random.randint(start_index, len(agent)-1)

    if start_index == end_index:
       end_index = end_index + 1
    # print(gene_a, gene_b)
    # +1 is added as the end_index' gene is on the list
    subset = agent[start_index:end_index + 1]
    subset.reverse()
    #  puts everything back together
    agent[start_index:end_index + 1] = subset

    individual[k] = agent

    return individual

def insertion(individual):
    #  k saves the random index number for later use
    k = random.randint(0, len(individual) - 1)
    #  Splits a random agent into genes and chooses randomly one
    agent = [gene for gene in individual[k]]
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
    #  Splits a random agent into genes and chooses randomly two
    genes = [gene for gene in individual[k]]
    gene1, gene2 = random.sample(genes, 2)
    #  Takes the index positions, to only swap the chosen genes
    a, b = genes.index(gene1), genes.index(gene2)
    genes[b], genes[a] = genes[a], genes[b]
    #  Inserts the new agent the same place it was taken from
    individual[k] = genes

    return individual


def sequence_inversion(individual):
    # TODO FIX code så den virker med det rigtige format - swapper kun to punkter i det rigtige format

    # print("Previous Individual: ", individual)

    # Select a random genome from the individual to mutate
    selected_genome = random.choice(individual)
    genome_index = individual.index(selected_genome)
    # print("Selected Genome: ", selected_genome)

    # Select a random sequence from the genome to be inverted
    gene_a = int(random.random() * len(selected_genome))
    gene_b = int(random.random() * len(selected_genome))
    start_index = min(gene_a, gene_b)
    end_index = max(gene_a, gene_b)
    # print(f"Selected Sequence: {start_index} -> {end_index-1}")

    # Take out the selected sequence out of the genome and reverse it
    gene_subset = selected_genome[start_index:end_index]
    # print("\nGene subset: ", gene_subset)
    gene_subset.reverse()
    # print("Reversed Gene subset: ", gene_subset)

    # Insert the reversed gene subset into the selected genome and thereafter put it back into the individual
    new_gene = [gene for gene in selected_genome if gene not in gene_subset]
    new_gene[start_index:start_index] = gene_subset
    individual[genome_index] = new_gene
    # print("New Individual: ", individual)

    return individual


print(individual)
# print(insertion(individual))
# print(transposition(individual))
# print(sequence_inversion(individual))
print(chromosome_contraction(individual))
# print(sequence_inversion2(individual)) = very much indeed better
# individual = sequence_inversion(individual)
