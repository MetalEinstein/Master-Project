import socket, pickle
from GA_Functions import *
import sys

# NETWORKING PARAMETERS
CONNECTION_LIST = []
EXPECTED_CONNECTIONS = 1
HOST = socket.gethostname()
PORT = 9998

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


taskList = []
TASK_NUMBER = 25
MAP_SIZE = 500
POP_SIZE = 100
ELITE_SIZE = 5
MUT_RATE = 0.90
MAX_GENERATIONS = 500
BREAKPOINT = 50
INITIAL_SELECTION_SIZE = 15


taskList, K_AGENTS = taskGeneratortesting(taskList)
home_city = taskList.pop(0)
pop = initialPopulation(POP_SIZE, taskList, K_AGENTS)  # Population
temp_rank = rankRoutes(pop, home_city)  # Fitness

# CHECK CONNECTIONS
while len(CONNECTION_LIST) != EXPECTED_CONNECTIONS:
    s.listen(5)
    conn, addr = s.accept()
    s.setblocking(True)
    print('Connected by: ', addr)

    CONNECTION_LIST.append((conn, addr))

print("Connection Overview:")
for i, connections in enumerate(CONNECTION_LIST):
    print(f"Device {i}: {connections[1]}")


# Data
PICKSIZE = 20
SEL_SIZE = 6

data_param = [MUT_RATE, PICKSIZE, SEL_SIZE]

data_fit = temp_rank
data_pop = pop
data_dic = pickle.dumps({0: data_param, 1: data_fit, 2: data_pop})

# Send Data
for conn, _ in CONNECTION_LIST:
    try:
        conn.send(data_dic)
    except:
        print("Error when sending message!")

# Receive result
new_pop = []
for conn, _ in CONNECTION_LIST:
    try:
        data = conn.recv(4096)
        new_pop.extend(pickle.loads(data))

    except:
        continue


for conn, _ in CONNECTION_LIST:
    conn.close()


print(len(new_pop), new_pop)
