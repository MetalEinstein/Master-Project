# TODO Compare a select number of unique pairs from the population to generate an overall similarity score 

# Genomes to compare.
genome1 = [1, 2, 3, 4, 5, 6, 7]
genome2 = [4, 6, 7, 10, 13, 8, 1, 2, 3]

print(f"Genome 1: {genome1}")
print(f"Genome 2: {genome2}")
print("\n")

similarity = 0
match_list = []

# Compare element i in genome 1 with all elements in genome 2
# If element i in genome 1 is found in genome 2 return the index at which the match occurred
for i in range(len(genome1)):
    for k in range(len(genome2)):
        if genome1[i] == genome2[k]:
            match_list.append(k)
            break

print(f"Indexes at which a match between the two Genomes occurred: {match_list}")
# We order the list in ascending order.
match_list = sorted(match_list)
print(f"Now ordered: {match_list}")

# We check for matching task order. If the same order is found we add 1 to the similarity score
for index in range(len(match_list)-1):
    if match_list[index+1] == match_list[index] + 1:
        similarity += 1

print(f"{similarity} pairs of numbers occurred in the same order in both Genomes")





