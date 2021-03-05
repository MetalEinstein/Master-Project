import random


def sequence_inversion(individual):
    # print("Previous Individual: ", individual)

    # Select a random genome from the individual to mutate
    genome_list = [genomes for genomes in individual]
    selected_genome = random.choice(genome_list)
    genome_index = individual.index(selected_genome)
    # print("Selected Genome: ", selected_genome)

    # Select a random sequence from the genome to be inverted
    gene_a = int(random.random() * len(selected_genome))
    gene_b = int(random.random() * len(selected_genome))
    start_index = min(gene_a, gene_b)
    end_index = max(gene_a, gene_b)
    # print(f"Selected Sequence: {start_index} -> {end_index}")

    # Take out the selected sequence out of the genome and invert it
    gene_subset = []
    for i in range(start_index, end_index):
        gene_subset.append(selected_genome[i])
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

