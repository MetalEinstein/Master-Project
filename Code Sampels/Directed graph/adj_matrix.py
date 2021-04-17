import matplotlib.pyplot as plt, cv2
import numpy as np
from my_classes import City, Fitness
from my_functions import *
import random

Task_number = 5
agents = 3
def city_connection(Task_number, agents):
    t1 = []
    t2 = []
    for h in range(agents):
        t1.append([])
        for i in range(Task_number):
            t1[h].append([])
            for j in range(0, 4):
                t1[h][i].append(random.randint(0, 500))
            t1[h][i] = tuple(t1[h][i])

    t2 = copy.deepcopy(t1)
    random.shuffle(t2)
    for i in range(agents):
        random.shuffle(t2[i])
    return t1, t2


def city_setup(city_list, num, size):
    # We create a set number of city's each of which is positioned randomly
    for i in range(0, num):
        # Generate a random location for a city
        city_posx = int(random.random() * size)
        city_posy = int(random.random() * size)

        # Add the generated city to the city list and add it to the map
        city_list.append(City(x=city_posx, y=city_posy))  # Creating a list of objects/city's

    return cityList

def city_matrix(num): # makes the city connections
    for i in range(0, num):
        a = []
        for j in range(0, num):
            if i == j:
                a.append(int(0))
            else:
                a.append(int(random.randint(0, 1)))

        matrixmap.append(a)
    #print(np.matrix(matrixmap))


# #           0  1  2  3  4  5
matrixmap = [[0, 0, 0, 1, 0, 0],    # 0
             [1, 0, 0, 0, 0, 0],    # 1
             [0, 0, 0, 0, 0, 0],    # 2
             [1, 1, 0, 0, 0, 0],    # 3
             [1, 0, 0, 0, 0, 1],    # 4
             [0, 0, 0, 0, 1, 0],    # 5
]


# matrixmap = []
cityList = []
num_city = 6
map_size = 500

cityList = city_setup(cityList, num_city, map_size)
# city_matrix(num_city)


xs = []
ys = []
for i in range(0, num_city):
    xs.append(cityList[i].x)
    ys.append(cityList[i].y)
print(f"x = {xs}, y = {ys}")





map_city = np.ones((map_size, map_size, 3), np.uint8)
map_city.fill(255)

for i, node in enumerate(matrixmap):
    a = []
    for index, edge in enumerate(node):
        if edge != 0:
            x = xs[i] - xs[index]
            y = ys[i] - ys[index]
            distance = np.sqrt((x ** 2) + (y ** 2))
            print(str(i), int(distance), index, sep=' -> ')
            matrixmap[i][index] = int(distance)
            cv2.circle(map_city, (xs[i], ys[i]), 3, 0, -1)  # Visualizing the position of city's on map
            cv2.line(map_city, (xs[i], ys[i]), (xs[index], ys[index]), (255, 0, 0), thickness=1, lineType=8)
print(np.matrix(matrixmap))
cv2.imshow('hej', map_city)
cv2.waitKey()


