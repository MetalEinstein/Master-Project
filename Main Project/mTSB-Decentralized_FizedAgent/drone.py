from DroneClasses import *
import socket, pickle, sys


# Create the next population
def evolvePopulation(population, popRanked, mutationRate, pickSize, sel_size):
    matingPool = Selection(population, popRanked, pickSize, sel_size).matingPool()
    newCrossoverPopulation = Crossover(matingPool).evolve()
    newPopulation = Mutation(newCrossoverPopulation, mutationRate).mutate()

    return newPopulation


# Socket params
HEADERSIZE = 10
HOST = socket.gethostname()
PORT = 9998

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connection Established!\n")

    # RECEIVE DATA
    data = b''
    new_data = True
    while True:
        packet = s.recv(16)
        if new_data:
            msglen = int(packet[:HEADERSIZE])
            new_data = False

        data += packet

        if len(data)-HEADERSIZE == msglen:
            data_dic = pickle.loads(data[HEADERSIZE:])
            break

    print("Data Received")

    # UNPACK DATA
    MUT_RATE, PICKSIZE, SEL_SIZE = data_dic[0]
    fit = data_dic[1]
    pop = data_dic[2]

    # PROCESS DATA and SEND IT
    new_pop = evolvePopulation(pop, fit, MUT_RATE, PICKSIZE, SEL_SIZE)
    data = pickle.dumps(new_pop)
    s.send(data)

    # TODO Implement a check here for when the server sends a shutdown command
    s.close()
    print("Data Sent")
    break

