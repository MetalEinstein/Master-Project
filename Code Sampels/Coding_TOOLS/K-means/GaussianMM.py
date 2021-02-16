import numpy as np
from sklearn.mixture import GaussianMixture
import random
import cv2


def generate_dataset(num_cities, map_size):
    city_list = []

    for i in range(0, num_cities):
        city_posx = int(random.random() * map_size)
        city_posy = int(random.random() * map_size)
        city = (city_posx, city_posy)

        city_list.append(city)

    return city_list


def get_groups(data, grouping, map_size):
    map_city = np.ones((map_size, map_size, 3), np.uint8)
    map_city.fill(255)
    num_groups = len(set(grouping))
    color_dic = {}
    initial_salesman = [[] for _ in range(0, num_groups)]

    # Generate unique colors for each salesman
    for i in range(0, num_groups):
        b_val = int(random.random() * 255)
        g_val = int(random.random() * 255)
        r_val = int(random.random() * 255)
        color_dic[i] = (b_val, g_val, r_val)

    # Visualize groups on a map and distribute the groups between salesmen
    for i in range(0, len(data)):
        x = data[i][0]
        y = data[i][1]
        cv2.circle(map_city, (x, y), 3, color_dic[grouping[i]], -1)
        initial_salesman[grouping[i]].append([x, y])

    return map_city, initial_salesman


def gaussianmm(data, number_salesman):
    gmm = GaussianMixture(n_components=number_salesman)
    gmm.fit(data)
    labels = gmm.predict(data)
    return labels


number_cities = 25
MAP_size = 200
nr_salesman = 4

data_set = generate_dataset(number_cities, MAP_size)
label = gaussianmm(data_set, nr_salesman)
map1, start_individual = get_groups(data_set, label, MAP_size)


for genomes in start_individual:
    print(genomes)


cv2.imshow("Map Layout", map1)
cv2.waitKey()
