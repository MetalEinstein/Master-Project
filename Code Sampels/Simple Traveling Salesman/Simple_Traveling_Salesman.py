import matplotlib.pyplot as plt, cv2
from my_classes import City
from my_functions import*
from typing import*


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


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, mapSize):
    pop = initialPopulation(popSize, population)
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])  # TODO We only keep an eye on the first route, maybe take the mean instead?

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])
        print("Current Distance: " + str(1 / rankRoutes(pop)[0][1]) + ",   ", "Generation: " + str(i))

    best_solution = rankRoutes(pop)[0][0]
    map_connect = city_connect(population, pop, mapSize, best_solution)
    cv2.imshow("Connected Map", map_connect)

    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()
    cv2.waitKey()


cityList = []
num_city = 25
map_size = 300

cityList = city_setup(cityList, num_city, map_size)
geneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=200, mapSize=map_size)
