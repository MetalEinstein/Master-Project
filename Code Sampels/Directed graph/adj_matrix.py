import cv2
# import numpy as np
from my_classes import City
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


def taskgenerator(cityList):
    cityx = [43, 25, 106, 119, 119, 86, 5, 56, 106, 100, 149, 124, 122, 148, 76]
    cityy = [2, 22, 14, 26, 16, 17, 48, 53, 20, 55, 57, 29, 11, 3, 5]

    for i in range(len(cityx)):
        cityList.append(City(x=cityx[i], y=cityy[i]))

    return cityList


def city_setup(city_list, num, size):
    # We create a set number of city's each of which is positioned randomly
    for i in range(0, num):
        # Generate a random location for a city
        city_posx = int(random.random() * size)
        city_posy = int(random.random() * size)

        # Add the generated city to the city list and add it to the map
        city_list.append(City(x=city_posx, y=city_posy))  # Creating a list of objects/city's

    return cityList


def city_matrix(num):  # makes the city connections
    for i in range(0, num):
        a = []
        for j in range(0, num):
            if i == j:
                a.append(int(0))
            else:
                a.append(int(random.randint(0, 1)))

        matrixmap.append(a)
    print(np.matrix(matrixmap))


# #           0  1  2  3  4  5
# matrixmap = [[0, 0, 0, 1, 0, 0],    # 0
#              [1, 0, 0, 0, 0, 0],    # 1
#              [0, 0, 0, 0, 0, 0],    # 2
#              [1, 1, 0, 0, 0, 0],    # 3
#              [1, 0, 0, 0, 0, 1],    # 4
#              [0, 0, 0, 0, 1, 0],    # 5
# ]

list_con = [(0, 0), (1, 2), (1, 3), (4, 5), (5, 6), (7, 8), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14)]

def connections(list_con, cityList):
    city_list = []
    for i in range(len(list_con)):
        list = []
        for j in range(2):
            list.append(cityList[list_con[i][j]].x)
            list.append(cityList[list_con[i][j]].y)
        city_list.append(list)
        city_list[i] = tuple(city_list[i])
    return city_list

# matrixmap = []
cityList = []
num_city = 15
map_size = 200

# cityList = city_setup(cityList, num_city, map_size)
cityList = taskgenerator(cityList)
cityList2 = connections(list_con, cityList)
print(list_con)
print(cityList2)
# print(cityList2[0][1])
# city_matrix(num_city)
xs = []
ys = []
for i in range(0, num_city):
    xs.append(cityList[i].x)
    ys.append(cityList[i].y)
# print(f"x = {xs}, y = {ys}")

def matrixmap():
    map_city = np.ones((map_size, map_size, 3), np.uint8)
    map_city.fill(255)

    for i, node in enumerate(matrixmap):
        for index, edge in enumerate(node):
            if edge != 0:
                x = xs[i] - xs[index]
                y = ys[i] - ys[index]
                distance = np.sqrt((x ** 2) + (y ** 2))
                # print(str(i), int(distance), index, sep=' -> ')
                print(str(i), index, sep=' , ')
                matrixmap[i][index] = int(distance)
                cv2.line(map_city, (xs[i], ys[i]), (xs[index], ys[index]), (255, 0, 0), thickness=1, lineType=8)
            cv2.circle(map_city, (xs[i], ys[i]), 3, 0, -1)  # Visualizing the position of city's on map
    map_city = cv2.resize(map_city, (2 * map_size, 2 * map_size), interpolation=cv2.INTER_CUBIC)
    print(np.matrix(matrixmap))
    cv2.imshow('hej', map_city)
    cv2.waitKey()

def dependmap(cityList2):
    scale = 4
    map_city = np.ones(((map_size*2), map_size*scale, 3), np.uint8)
    map_city.fill(255)

    txt = 'Distance ='
    for i in range(len(cityList)):
        cv2.circle(map_city, (cityList[i].x*scale, cityList[i].y*scale), 3, 0, -1)  # Visualizing the position of city's on map

    for i in range(len(cityList2)):
        cv2.line(map_city, (cityList2[i][0]*scale, cityList2[i][1]*scale), (cityList2[i][2]*scale, cityList2[i][3]*scale), (0, 0, 255), thickness=1, lineType=cv2.LINE_AA)
        if i < len(cityList2)-1:
            cv2.line(map_city, (cityList2[i][2]*scale, cityList2[i][3]*scale), (cityList2[i+1][0]*scale, cityList2[i+1][1]*scale), (0, 255, 0),
                 thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(map_city, txt, org=(0, map_size*2), fontFace=cv2.FONT_ITALIC, fontScale=0.3, color=(0, 0, 0), thickness=1,
                lineType=8)
    # map_city = cv2.resize(map_city, (2 * map_size, 2 * map_size), interpolation=cv2.INTER_CUBIC)
    #
    print(np.matrix(matrixmap))
    cv2.imshow('Dependent map', map_city)
    cv2.waitKey()
dependmap(cityList2)