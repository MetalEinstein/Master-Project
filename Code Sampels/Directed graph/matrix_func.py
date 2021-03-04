import cv2
from my_classes import City
import numpy as np
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

def city_matrix(num):  # Makes a random adjancy matrix of city connections with distances between the points
    #              0  1  2  3  4  5
    # sudo_map = [[0, 0, 0, 1, 0, 0],    # 0   0->[3]
    #             [1, 0, 0, 0, 0, 0],    # 1   1->[0]
    #             [0, 0, 0, 0, 0, 0],    # 2
    #             [1, 1, 0, 0, 0, 0],    # 3   3->[0,1]
    #             [1, 0, 0, 0, 0, 1],    # 4   4->[0,5]
    #             [0, 0, 0, 0, 1, 0],]   # 5   5->[4]
    map_city = np.ones((map_size, map_size, 3), np.uint8)
    map_city.fill(255)
    xs = []
    ys = []
    for i in range(0, num):  # Separate x and y from cityList
        xs.append(cityList[i].x)
        ys.append(cityList[i].y)
    for j in range(0, num):
        a = []
        for index in range(0, num):
            if j == index: # Creates a diagonal zero line
                a.append(int(0))
            elif random.randint(0, 1) == 0:  # random generated zero connections
                a.append(int(0))
            else:
                x = xs[j] - xs[index]
                y = ys[j] - ys[index]
                distance = np.sqrt((x ** 2) + (y ** 2))  # calculates the distances
                a.append(int(distance))
                cv2.circle(map_city, (xs[j], ys[j]), 3, 0, -1)  # Visualizing the position of city's on map
                cv2.line(map_city, (xs[j], ys[j]), (xs[index], ys[index]), (255, 0, 0), thickness=1, lineType=8)
        matrixmap.append(a)
    print(np.matrix(matrixmap))
    cv2.imshow('Matrix City', map_city)
    cv2.waitKey()
    return np.matrix(matrixmap)



matrixmap = []
cityList = []
num_city = 25
map_size = 500

cityList = city_setup(cityList, num_city, map_size)
print(cityList)
city_matrix(num_city)
