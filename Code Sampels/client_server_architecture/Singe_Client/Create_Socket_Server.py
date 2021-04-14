import socket

MAX_HEADER_SIZE = 10


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

        print("Binding the Port: " + str(port))

        soc.bind((host, port))
        soc.listen(5)  # We listen for 5 connection attempts before moving on

    except socket.error as msg:
        print("Socket Binding error: " + str(msg) + "\n" + "Retrying...")
        bind_socket()  # We use recursion to keep on checking for connections


# Establish connection with a client (Socket must be listening)
def socket_accept():
    conn, address = soc.accept()
    print("Connection has been established!  |" + " IP " + address[0] + " | Port: " + str(address[1]))
    send_message(conn)
    conn.close()


# Send a message to client/clients
def send_message(conn):
    while True:
        print("\nType in a message: ")
        message = input()
        if message == "quit":
            conn.close()
            soc.close()

        if len(str.encode(message)) > 0:

            # Inform the client of the incoming message size.
            # First part of message (len(msg):<{MAX_HEADER_LENGTH}) contains size, last part (+ msg) contains message
            message = f'{len(message):<{MAX_HEADER_SIZE}}' + message
            conn.send(str.encode(message))  # We encode the message to bit format

            # Store and print the client response 
            client_response = str(conn.recv(1024), "utf-8")  # We receive the client response in 1024 bit bits at a time
            print("Client Response: ", client_response, end="")
            print("\n")


def main():
    # Create a Socket
    create_socket()

    # Binding the socket and listening for connections from client/clients
    bind_socket()

    # Establish connection with a client
    socket_accept()


main()

