import cv2
from sklearn.cluster import KMeans
import random, numpy as np
from matplotlib import pyplot as plt
import kneed
import math


def generate_dataset(num_citys, map_size):
    city_list = []

    for i in range(0, num_citys):
        city_posx = int(random.random() * map_size)
        city_posy = int(random.random() * map_size)
        city = (city_posx, city_posy)

        city_list.append(city)

    return city_list

# TODO problem occur when num_salesmen falls below 5 
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
    km = KMeans(n_clusters=kn.elbow)
    y_predicted = km.fit_predict(data)

    plt.xlabel('K')
    plt.ylabel('Sum of squared error')
    plt.plot(k_rng, sse, 'bx-')

    return y_predicted


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


NUMBER_OF_CITYS = 100
MAP_SIZE = 300
NUM_SALESMEN = 10

dataset = generate_dataset(NUMBER_OF_CITYS, MAP_SIZE)
label = perform_k_means(dataset, NUM_SALESMEN)
map, start_individual = get_groups(dataset, label, MAP_SIZE)

cv2.imshow("Map Layout", map)
plt.show()
cv2.waitKey()
