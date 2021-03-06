import random

individual = [[(28, 246), (153, 250), (277, 187), (67, 143), (60, 342)],
              [(252, 263), (270, 24), (490, 127), (203, 296), (111, 49)],
              [(433, 195), (391, 466), (187, 164), (490, 30), (316, 394)]]


# individual = [[1, 2, 3, 4, 5, 6, 7], [8, 9], [10, 11, 12, 13, 14, 15]]
def geneSwap(individual):
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
print(geneSwap(individual))
print(sequence_inversion(individual))

# individual = sequence_inversion(individual)
