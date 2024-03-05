import socket


class Client:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

    def ping(self):
        print("Ok!")

    def __str__(self):

        return f"Connection to SERVER at {self.IP}, PORT: {self.PORT}"

    def talk(self, msg):
        # -- Create the socket
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # establish the connection to the Server (IP, PORT)
        clientsocket.connect((self.IP, self.PORT))

        # Send data.
        clientsocket.send(str.encode(msg))

        # Receive data
        response = clientsocket.recv(2048).decode("utf-8")

        # Close the socket
        clientsocket.close()

        # Return the response
        return response

