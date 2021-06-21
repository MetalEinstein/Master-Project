import socket
import threading
from queue import Queue

queue = Queue()
all_connections = []
all_address = []

# Socket Parameters
MAX_HEADER_SIZE = 10  # Max message size


# Create a Socket (For connecting two programs/computers)
def create_socket():
    try:
        global host
        host = ""

        global port
        port = 9999

        global soc
        soc = socket.socket()

    except socket.error as msg:
        print("Socket creation Error: " + str(msg))


# Binding the socket and listening for connections from client/clients
def bind_socket():
    try:
        global host
        global port
        global soc

        print("Binding to Port: " + str(port))

        soc.bind((host, port))
        soc.listen(5)  # We listen for 5 connection attempts before moving on

    except socket.error as msg:
        print("Socket Binding error: " + str(msg) + "\n" + "Retrying...")
        bind_socket()  # We use recursion to keep on checking for connections


# Handling connections from multiple clients and saving the connections to a list
# Closing previous connections when server.py file is restarted
def accepting_connections(NUM_WORKERS):

    # Closing previous connections
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = soc.accept()
            soc.setblocking(True)  # Prevents timeout

            # Add connection object and address to list
            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established to: " + address[0])
            if len(all_connections) == NUM_WORKERS:
                break

        except:
            print("Error accepting connections")
