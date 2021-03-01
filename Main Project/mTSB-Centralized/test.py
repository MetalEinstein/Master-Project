import random

def breed():
    parent1_continuous = [1, 2, 3, 0, 4, 5, 6, 0, 7, 8, 9, 0, 10]
    parent2_continuous = [4, 6, 5, 0, 10, 0, 7, 8, 9, 0, 1, 2, 3]

    # --- CROSSOVER OPERATOR (DPX) ---
    child1 = []
    match_list = []
    fragment = []
    fragment_list = []
    remainder = []
    considerations = []

    # Keeping track of the breakpoints for both parents
    p1_breakpoints = [i for i in range(len(parent1_continuous)) if parent1_continuous[i] == 0]
    p2_breakpoints = [i for i in range(len(parent2_continuous)) if parent2_continuous[i] == 0]

    # Compare element i in gene 1 with all elements in gene 2
    # If element i in gene1 is found in gene 2 return the index at which the match occurred
    for i in range(len(parent1_continuous)):
        for k in range(len(parent2_continuous)):
            if parent1_continuous[i] == parent2_continuous[k] and parent1_continuous[i] != 0:
                match_list.append(k)
                break

    # Check if the matches occurred in sequence and if they did add them as a fragment
    former_match = False
    for i in range(len(match_list)):
        if i < len(match_list)-1:
            if match_list[i+1] == match_list[i]+1 or match_list[i+1] == match_list[i]-1:
                former_match = True
                fragment.append(parent2_continuous[match_list[i]])

            else:
                if former_match:
                    fragment.append(parent2_continuous[match_list[i]])
                    fragment.append(0)
                    former_match = False
        else:
            if former_match:
                fragment.append(parent2_continuous[match_list[i]])

    # Find the tasks that are not part of a common sequence in both parents
    remainder = [task for task in parent2_continuous if task not in fragment]

    # Order the fragments in a nested list for reconstruction
    sub_list = []
    for sub_fragment in fragment:
        if sub_fragment != 0:
            sub_list.append(sub_fragment)
        else:
            fragment_list.append(sub_list)
            sub_list = []

    for sub_fragment in remainder:
        fragment_list.append([sub_fragment])

    # Points to consider for greedy reconstruction
    for points in fragment_list:
        if len(points) == 1:
            considerations.append(points[0])
        else:
            considerations.append(points[0])
            considerations.append(points[-1])

    # The initial fragment is selected and added as the first fragment in the reconstruction list
    initial_task = random.choice(considerations)
    reconstructed = [frag for frag in fragment_list if initial_task in frag]
    initial_endpoint = reconstructed[0][-1]

    fragment_list.remove(reconstructed[0])
    if len(reconstructed[0]) == 1:
        considerations.remove(initial_endpoint)
    else:
        considerations.remove(initial_endpoint)
        considerations.remove(reconstructed[0][0])


    # TODO Find out which task has the smallest distance to endpoint and connect the fragment containing the task
    distance = 0
    for f in range(len(fragment_list)-1):
        if f == 0:
            for tasks in considerations:
                distance =


    # TODO If the endpoint of one fragments has the shortest distance to the endpoint of another, reverse and connect the other
    # TODO Remember to remove the task considerations after connecting their associated fragment

    print("Parent 1: ", parent1_continuous)
    print("Parent 2: ", parent2_continuous)
    print("Match list: ", match_list)
    print("\n")
    print("Fragment List")
    for elements in fragment_list:
        print(elements)
    print("\nPoints for Reconstruction: ", considerations)
    print(initial_task)
    print(reconstructed)




breed()





