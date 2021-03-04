import matplotlib.pyplot as plt, cv2
import numpy as np
from my_classes import City, Fitness
from my_functions import *
import random

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
    print(np.matrix(matrixmap))

# print(bit)
#                0  1  2  3  4  5
# cityMatrix = [[0, 1, 0, 1, 0, 0],    # 0
#               [1, 0, 0, 1, 0, 0],    # 1
#               [0, 0, 0, 0, 0, 0],    # 2
#               [1, 1, 0, 0, 0, 0],    # 3
#               [0, 0, 0, 0, 0, 1],    # 4
#               [0, 0, 0, 0, 1, 0],    # 5
# ]


matrixmap = []
cityList = []
num_city = 10
map_size = 300

cityList = city_setup(cityList, num_city, map_size)
city_matrix(num_city)



silly_list = []
for j in range(0, num_city):

    silly_list.append(cityList[j])
print(silly_list)


# TODO: make the coordinate work with the real data instead of static
coord = [(274,13), (58,286), (210,111), (151,24), (124,154), (2,82), (168,66), (91,52), (256,0), (213,288)]
xs = [x for x, y in coord]
ys = [y for x, y in coord]


print(coord)
print('x =', xs, 'y =', ys)

map_city = np.ones((map_size, map_size, 3), np.uint8)
map_city.fill(255)

for i, node in enumerate(matrixmap):
    a = []
    for index, edge in enumerate(node):
        if edge != 0:
            x = xs[i] - xs[index]
            y = ys[i] - ys[index]
            distance = np.sqrt((x ** 2) + (y ** 2))
            # print('xc =', xs[i], 'xi =', xs[index], 'xdist =', x)
            # print('yc =', ys[i], 'yi =', ys[index],'ydist =', y)
            # print(str(i), int(distance), index, sep=' -> ')
            matrixmap[i][index] = int(distance)
            cv2.circle(map_city, (xs[i], ys[i]), 3, 0, -1)  # Visualizing the position of city's on map
            cv2.line(map_city, (xs[i], ys[i]), (xs[index], ys[index]), (255, 0, 0), thickness=1, lineType=8)
print(np.matrix(matrixmap))



