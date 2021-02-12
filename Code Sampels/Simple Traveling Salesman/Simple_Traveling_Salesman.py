import matplotlib.pyplot as plt, cv2
from my_classes import City
from my_functions import*
from typing import*
import time


def city_setup(city_list, num, size):

    # We create a set number of city's each of which is positioned randomly
    for i in range(0, num):
        # Generate a random location for a city
        city_posx = int(random.random() * size)
        city_posy = int(random.random() * size)

        # Add the generated city to the city list and add it to the map
        city_list.append(City(x=city_posx, y=city_posy))  # Creating a list of objects/city's

    return cityList


def city_connect(city_list, final_population, size, best_index):
    map_city = np.ones((size, size, 3), np.uint8)
    map_city.fill(255)

    # We plot the city's on the map and draw the most optimized route between them
    for i in range(0, len(city_list)):
        if i == len(city_list)-1:
            city1_posx, city1_posy = final_population[best_index][i].x, final_population[best_index][i].y
            city2_posx, city2_posy = final_population[best_index][0].x, final_population[best_index][0].y

        else:
            city1_posx, city1_posy = final_population[best_index][i].x, final_population[best_index][i].y
            city2_posx, city2_posy = final_population[best_index][i + 1].x, final_population[best_index][i + 1].y

        if i == 0:
            cv2.circle(map_city, (city1_posx, city1_posy), 3, 0, -1)  # Visualizing the position of city's on map
            cv2.line(map_city, (city1_posx, city1_posy), (city2_posx, city2_posy), (255, 0, 0), thickness=1, lineType=8)
        else:
            cv2.circle(map_city, (city1_posx, city1_posy), 3, (0, 0, 255), -1)  # Visualizing the position of city's on map
            cv2.line(map_city, (city1_posx, city1_posy), (city2_posx, city2_posy), (255, 0, 0), thickness=1, lineType=8)

    return map_city


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, breakpoint, mapSize):
    pop = initialPopulation(popSize, population)
    generation_diff = []
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])  # We track progress according to the best route

    p_counter = 0
    for i in range(0, generations):
        p_counter += 1

        progress_past = 1 / rankRoutes(pop)[0][1]
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress_future = 1 / rankRoutes(pop)[0][1]
        generation_diff.append(abs(progress_past - progress_future))

        progress.append(1 / rankRoutes(pop)[0][1])
        print("Current Distance: " + str(1 / rankRoutes(pop)[0][1]) + ",   ", "Generation: " + str(i))

        # We check the progress over a set number of generations. If progress = 0 we stop the algorithm
        # Might be an alternative just to use breakpoint instead of iteration for a set number of generations
        if p_counter == breakpoint:
            p_counter = 0
            total_diff = sum(generation_diff)
            generation_diff.clear()

            if total_diff == 0:
                break

    best_solution = rankRoutes(pop)[0][0]
    map_connect = city_connect(population, pop, mapSize, best_solution)

    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()
    cv2.imshow("Connected Map", map_connect)
    cv2.waitKey()

cityList = []
num_city = 25
map_size = 300

start_time = time.time()
cityList = city_setup(cityList, num_city, map_size)
geneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=200, breakpoint=20, mapSize=map_size)


