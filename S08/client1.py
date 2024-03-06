import socket

SERVER_PORT = 8081
SERVER_IP = "127.0.0.1"

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect((SERVER_IP, SERVER_PORT))

clientsocket.send(str.encode("HELLO FROM THE CLIENT!!!"))

# Close the socket
clientsocket.close()
