import socket

MAX_HEADER_SIZE = 10
CLIENT_RESPONSE = "Message Received"

soc = socket.socket()
host = socket.gethostname()  # Server IP
port = 9999  # Should be the same port number as Server

# Connect to host IP and Port
soc.connect((host, port))
while True:
    full_msg = ''
    new_msg = True

    while True:
        data = soc.recv(1024)

        if new_msg:
            msglen = int(data[:MAX_HEADER_SIZE])  # We check the fist part of the received message for the message size
            new_msg = False

        full_msg += data.decode("utf-8")

        # We compare the length of the message received so far and the informed message size.
        # If we have reached the informed message size we know that everything is received
        if len(full_msg) - MAX_HEADER_SIZE == msglen:
            print("\nFull message received!")
            print(full_msg[MAX_HEADER_SIZE:])
            new_msg = True
            full_msg = ''

            # Send response
            soc.send(str.encode(CLIENT_RESPONSE))
