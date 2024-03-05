import socket  #(module)

# Configure the Server's IP and PORT
PORT = 8081
IP = ""  # it depends on the machine the server is running

MAX_OPEN_REQUESTS = 5

# Counting the number of connections (how many connections connected to the server).
number_con = 0

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #(this is a variable we are creating).
try:
    serversocket.bind((IP, PORT)) #(unir o atar)
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print(f"Waiting for connections at {IP}, {PORT} ")
        (clientsocket, address) = serversocket.accept()

        # Another connection!e
        number_con += 1

        # Print the connection number
        print(f"CONNECTION: {number_con}. From the IP: {address}")

        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")
        print(f"Message from client: {msg}")

        # Send the message
        message = "Hello from the teacher's server\n"
        send_bytes = str.encode(message)
        # We must write bytes, not a string
        clientsocket.send(send_bytes)
        clientsocket.close()
except socket.error:
    print(f"Problems using ip {IP} port {PORT}. Is the IP correct? Do you have port permission?")
except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()