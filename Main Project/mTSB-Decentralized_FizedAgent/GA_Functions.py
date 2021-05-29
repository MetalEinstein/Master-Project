from GA_Classes import *
from sklearn.cluster import KMeans
import kneed
import cv2


def taskGenerator(taskList: List[object], taskNum: int, mapSize: int):
    # We create a set number of city's each of which is positioned randomly
    temp = []
    NUM_SALESMEN = 5
    for i in range(0, taskNum):
        # Generate a random location for a city
        city_posx = int(random.random() * mapSize)
        city_posy = int(random.random() * mapSize)
        temp.append((city_posx, city_posy))  # Creating a list of objects/city's

    label = perform_k_means(temp, NUM_SALESMEN)

    for j in range(0, taskNum):
        taskList.append(City(x=temp[j][0], y=temp[j][1]))

    print("tasklist: ", taskList)
    return taskList, label


def taskGeneratortesting(taskList: List[object]):
    # We create a set number of city's each of which is positioned randomly
    temp = []
    NUM_SALESMEN = 5
    #list = [(67,423), (381,127), (247,224), (325,394), (46,14), (417,216), (381,1), (222,360), (114,472), (450,15), (12,270), (469,190), (108,211), (14,110), (218,247), (116,115), (109,229), (144,10), (418,278), (321,92), (496,429), (60,166), (360,355), (468,211), (415,335)]
    cityx = [67, 381, 247, 325, 46, 417, 381, 222, 114, 450, 12, 469, 108, 14, 218, 116, 109, 144, 418, 321, 496, 60, 360, 468, 415]
    cityy = [423, 127, 224, 394, 14, 216, 1, 360, 472, 15, 270, 190, 211, 110, 247, 115, 229, 10, 278, 92, 429, 166, 355, 211, 335]
    for i in range(len(cityx)):
        city_posx = cityx[i]
        city_posy = cityy[i]
        temp.append((city_posx, city_posy))

    label = perform_k_means(temp, NUM_SALESMEN)

    for j in range(len(cityx)):
        taskList.append(City(x=temp[j][0], y=temp[j][1]))

    print("tasklist: ", taskList)
    return taskList, label


def createRoute(taskList, num_agents):
    temp_taskList = random.sample(taskList, len(taskList))
    individual = []
    tasks_each = int(len(temp_taskList)/num_agents)

    # Distribute the tasks among the agents
    genome = []
    for a in range(num_agents-1):
        for i in range(tasks_each):
            selected_task = random.randint(0, len(temp_taskList)-1)
            genome.append(temp_taskList.pop(selected_task))
        individual.append(genome)
        genome = []

    # Add the remaining tasks in the tasklist to the last agent
    individual.append(temp_taskList)

    return individual


def initialPopulation(popSize, taskList, num_agents):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(taskList, num_agents))

    return population


def rankRoutes(population, homeCity):
    fitnessResults = {}

    # Will fill a dictionary with key-value pairs
    # Key = Population index, value = corresponding fitness score
    fitness = Fitness(population, homeCity).routeFitness()
    for i in range(len(fitness)):
        fitnessResults[i] = fitness[i]

    # key = operator.itemgetter(1) -> Will create a sorted list according to the '1' element, 0 being the population index
    # and 1 being the fitness score. Thus we sort it from highest to lowest score
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)  # Returns sorted list


def city_connect(final_population, size, best_index, home_city):
    map_city = np.ones((size, size, 3), np.uint8)
    map_city.fill(255)
    color_dic = {}

    # Add the home city to the task list of each salesmen
    best_individual = final_population[best_index]
    for genome_index in range(len(best_individual)):
        best_individual[genome_index].insert(0, home_city)

    # Generate unique colors for each salesman
    for i in range(0, len(best_individual)):
        b_val = int(random.random() * 255)
        g_val = int(random.random() * 255)
        r_val = int(random.random() * 255)
        color_dic[i] = (b_val, g_val, r_val)

    # Draw the tasks and their connections on a map
    for genomes in best_individual:
        # We plot the city's on the map and draw the most optimized route between them
        for i in range(0, len(genomes)):
            if i == len(genomes) - 1:
                city1_posx, city1_posy = genomes[i].x, genomes[i].y
                city2_posx, city2_posy = genomes[0].x, genomes[0].y

            else:
                city1_posx, city1_posy = genomes[i].x, genomes[i].y
                city2_posx, city2_posy = genomes[i + 1].x, genomes[i + 1].y

            if i == 0:
                cv2.circle(map_city, (city1_posx, city1_posy), 3, 0, -1)  # Visualizing the position of city's on map
                cv2.line(map_city, (city1_posx, city1_posy), (city2_posx, city2_posy), color_dic[best_individual.index(genomes)], thickness=1, lineType=8)
            else:
                cv2.circle(map_city, (city1_posx, city1_posy), 3, (0, 0, 255),
                           -1)  # Visualizing the position of city's on map
                cv2.line(map_city, (city1_posx, city1_posy), (city2_posx, city2_posy), color_dic[best_individual.index(genomes)], thickness=1, lineType=8)

    return map_city

def perform_k_means(data, num_salesmen):
    sse = []
    k_rng = range(1, num_salesmen+1)

    for k in k_rng:
        km = KMeans(n_clusters=k)
        km.fit(data)
        sse.append(km.inertia_)

    # TODO improve the estimation of the best number of K. Maybe through tracking the slope of the curve
    """
    for i in range(0, len(sse)-1):
        m = 1-((sse[i+1]/sse[i])/1)
        print(m)
    """

    kn = kneed.KneeLocator(k_rng, sse, curve='convex', direction='decreasing', interp_method='interp1d')
    print("Best Estimated K: ", kn.elbow)

    return kn.elbow
