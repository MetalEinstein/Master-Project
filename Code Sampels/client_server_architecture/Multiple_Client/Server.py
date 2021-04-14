import socket
import threading
from queue import Queue

MAX_HEADER_SIZE = 10  # Max message size
NUMBER_OF_THREADS = 2  # We want to do two things simultaneously (Listen for new connections and maintain and communicate with existing ones)
JOB_NUMBER = [1, 2]  # Job id's for threads

queue = Queue()
all_connections = []
all_address = []

# Commands
cmd_1 = "'list'  :  Will display all connected clients\n"
cmd_2 = "'select id'  :  Will select a specific client\n"
cmd_3 = "'quit'  : Will disconnect from selected client\n"
print("COMMAND LIST:")
print(f"{cmd_1}{cmd_2}{cmd_3}")


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


# --------- THREAD 1 -------------
# Handling connections from multiple clients and saving the connections to a list
# Closing previous connections when server.py file is restarted '
def accepting_connections():

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

        except:
            print("Error accepting connections")


# --------- THREAD 2 -------------
# 1) See all clients,  2) Select a client,  3) Send commands to the connected client
# Interactive prompt for sending commands
def start_prompt():
    while True:
        cmd = input()

        # 1) For seeing all clients
        if cmd == "list":
            list_connections()

        # 2) For selecting and sending commands to a connected client
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_message(conn)
        else:
            print("Command not recognized")


# Display all current connections with the server
def list_connections():
    results = ""

    # We go through all our connections and check if they are active by sending a dummy string
    # If we receive a feedback from the client we know that the connection is stable
    for i, conn in enumerate(all_connections):
        # Send and receive
        try:
            conn.send(str.encode("0"))
            conn.recv(1024)

        # If no feedback is returned delete the client from the list of connections
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results += str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("---- Clients ----" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace("select ", "")  # Separate string from selection id
        target = int(target)  # Typecast the id to integer
        conn = all_connections[target]  # Retrieve the connection object from the target id

        print("You are connected to: " + str(all_address[target][0]))
        return conn

    # Except will be thrown if the selected id is not in the list of connected clients
    except:
        print("Selection not valid")
        return None


# Send a message to client/clients
def send_target_message(conn):
    while True:
        try:
            print("Type in message/command to connected client: ", end="")
            message = input()
            if message == "quit":
                print("\n")
                break

            if len(str.encode(message)) > 0:

                # Inform the client of the incoming message size.
                # First part of message (len(msg):<{MAX_HEADER_LENGTH}) contains size, last part (+ msg) contains message
                message = f'{len(message):<{MAX_HEADER_SIZE}}' + message
                conn.send(str.encode(message))  # We encode the message to bit format and send it

                # Store and print the client response
                client_response = str(conn.recv(1024), "utf-8")  # We receive the client response in 1024 bit bits at a time
                print("Client Response: ", client_response, end="")
                print("\n")

        except:
            print("Error sending message")
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)  # We create N threads that run in parallel. "work" specifies what the threads should do
        t.daemon = True  # Will release the borrowed memory after server shutdown
        t.start()  # We start the thread


# Do next job in queue
def work():
    while True:
        x = queue.get()

        # Thread 1 - Listen for new connections
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()

        # Thread 2 - Maintain and communicate with existing connections
        if x == 2:
            start_prompt()

        queue.task_done()


# Add the jobs id's to the queue
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()



