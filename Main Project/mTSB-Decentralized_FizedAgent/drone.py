from DroneClasses import *
import socket, pickle, sys


# Create the next population
def evolvePopulation(population, popRanked, mutationRate, pickSize, sel_size):
    matingPool = Selection(population, popRanked, pickSize, sel_size).matingPool()
    newCrossoverPopulation = Crossover(matingPool).evolve()
    newPopulation = Mutation(newCrossoverPopulation, mutationRate).mutate()

    return newPopulation


# Socket params
HOST = socket.gethostname()
PORT = 1234

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connection Established!\n")

        # RECEIVE DATA
        data_length = pickle.loads(s.recv(1024))
        data = b""
        while sys.getsizeof(data) != data_length:
            packet = s.recv(4096)
            data += packet
        print("Data Received")

        data_dic = pickle.loads(data)

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

    except:
        print("Attempting Connection")
        continue
