import random


def sequence_inversion(individual):
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


# individual = [[1, 2, 3, 4, 5, 6, 7], [8, 9], [10, 11, 12, 13, 14, 15]]
# individual = sequence_inversion(individual)

