import socket
from game import Numberguesser

import socket

server_port = 8081
server_ip = "127.0.0.1"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((server_ip, server_port))
    server_socket.listen()

    while True:
        print(f"Waiting for connections at {server_ip}, {server_port} ")
        (client_socket, address) = server_socket.accept()
        msg = client_socket.recv(2048).decode("utf-8")
        print(f"Message from client: {msg}")
        message = "Hello from the teacher's server\n"
        send_bytes = str.encode(message)
        client_socket.send(send_bytes)
        client_socket.close()
except socket.error:
    print(f"Problems using ip {server_ip} port {server_port}. Is the IP correct? Do you have port permission?")
except KeyboardInterrupt:
    print("Server stopped by the user")
    server_socket.close()

